import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2.39.0";

const supabase = createClient(
  Deno.env.get("SUPABASE_URL") ?? "",
  Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") ?? ""
);

serve(async (req) => {
  try {
    const { owner, repo, base, compare } = await req.json();
    const githubToken = Deno.env.get("GITHUB_PAT");

    // Ping GitHub API to compare the references
    const response = await fetch(`https://api.github.com/repos/${owner}/${repo}/compare/${base}...${compare}`, {
      headers: {
        "Authorization": `token ${githubToken}`,
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Coastal-Alpine-Agent"
      }
    });

    const data = await response.json();
    let status = 'orphaned';
    let ancestor = null;

    if (response.ok && data.merge_base_commit) {
        status = data.status; // identical, ahead, behind, diverged
        ancestor = data.merge_base_commit.sha;
    } else if (response.status === 404) {
        // 404 on compare usually means no common ancestor found (unrelated histories)
        status = 'orphaned';
    }

    // Upsert the state to Postgres
    await supabase.from('branch_lineage_health').upsert({
      repository: repo,
      base_branch: base,
      compare_branch: compare,
      status: status,
      common_ancestor_sha: ancestor,
      last_checked: new Date().toISOString()
    }, { onConflict: 'repository,base_branch,compare_branch' });

    return new Response(JSON.stringify({ status, ancestor }), {
      headers: { "Content-Type": "application/json" },
    });
  } catch (err) {
    return new Response(JSON.stringify({ error: err.message }), { status: 500 });
  }
});
