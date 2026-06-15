import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

serve(async (req) => {
  // 1. Verify Authorization (Security perimeter)
  const authHeader = req.headers.get('Authorization')
  if (authHeader !== `Bearer ${Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')}`) {
    return new Response(JSON.stringify({ error: "Unauthorized access attempt" }), { status: 401 })
  }

  try {
    const payload = await req.json()
    // Extract pg_net webhook payload
    const { node_id, metrics, event_type } = payload.record 

    console.log(`[WEAVER ORCHESTRATOR] Autonomous wake event triggered by Node: ${node_id}`)

    const supabase = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? ''
    )

    // 2. Fetch Node Hardware Context
    const { data: nodeCtx, error } = await supabase
      .from('ecosystem_nodes')
      .select('node_type, beachhead_tag')
      .eq('node_id', node_id)
      .single()

    if (error) throw new Error("Hardware node identity not found in registry.")

    // 3. Construct the State Vector for the LLM Agent
    const agentState = {
      role: "Weaver Orchestrator",
      beachhead: nodeCtx?.beachhead_tag,
      hardware_type: nodeCtx?.node_type,
      critical_metrics: metrics,
      action_required: true,
      timestamp: new Date().toISOString()
    }

    // [Future Execution: Dispatch to local LangGraph Python endpoint here]
    
    return new Response(JSON.stringify({ 
      status: "Orchestrator Woken successfully", 
      context: agentState 
    }), { status: 200 })

  } catch (error) {
    console.error(`[SYSTEM FAULT] ${error.message}`)
    return new Response(JSON.stringify({ error: error.message }), { status: 500 })
  }
})
