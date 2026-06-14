import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2.39.0";

const supabase = createClient(
  Deno.env.get("SUPABASE_URL") ?? "",
  Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") ?? ""
);

serve(async (req) => {
  try {
    const { node_id, status, cpu_temp_celsius, memory_usage_percent } = await req.json();

    // Upsert the telemetry data
    const { error } = await supabase
      .from('node_fleet_health')
      .upsert({
        node_id,
        status,
        cpu_temp_celsius,
        memory_usage_percent,
        last_ping: new Date().toISOString()
      }, { onConflict: 'node_id' });

    if (error) throw error;

    return new Response(
      JSON.stringify({ message: `Node ${node_id} telemetry logged successfully.` }),
      { headers: { "Content-Type": "application/json" } }
    );
  } catch (err) {
    return new Response(JSON.stringify({ error: err.message }), { status: 500 });
  }
});
