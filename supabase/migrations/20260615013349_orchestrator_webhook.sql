-- Enable the pg_net extension for asynchronous outbound HTTP requests
CREATE EXTENSION IF NOT EXISTS pg_net WITH SCHEMA extensions;

-- Create unified edge telemetry table if it doesn't exist
CREATE TABLE IF NOT EXISTS public.unified_edge_telemetry (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    node_id VARCHAR(100) NOT NULL,
    anomaly_flag BOOLEAN DEFAULT FALSE,
    metrics JSONB,
    recorded_at TIMESTAMPTZ DEFAULT NOW()
);

-- Secure the telemetry table
ALTER TABLE public.unified_edge_telemetry ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Service Role Only" 
ON public.unified_edge_telemetry FOR ALL 
USING (auth.role() = 'service_role');

-- Define the trigger function
CREATE OR REPLACE FUNCTION public.wake_weaver_orchestrator()
RETURNS TRIGGER AS $$
BEGIN
  -- We only wake the AI if the telemetry payload flagged an anomaly
  IF NEW.anomaly_flag = TRUE THEN
    PERFORM net.http_post(
      url := 'https://qipvfvrjpvqtnccbjyfy.supabase.co/functions/v1/weaver-orchestrator',
      headers := jsonb_build_object(
        'Content-Type', 'application/json',
        'Authorization', 'Bearer <YOUR_SERVICE_ROLE_KEY>' 
      ),
      body := jsonb_build_object(
        'event_type', 'ANOMALY_DETECTED',
        'node_id', NEW.node_id,
        'metrics', NEW.metrics,
        'timestamp', NEW.recorded_at
      )
    );
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Attach the trigger to our unified telemetry table
CREATE TRIGGER trigger_wake_weaver
  AFTER INSERT ON public.unified_edge_telemetry
  FOR EACH ROW
  EXECUTE FUNCTION public.wake_weaver_orchestrator();
