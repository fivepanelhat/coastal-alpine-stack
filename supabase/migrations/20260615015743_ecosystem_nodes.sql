-- Create ecosystem nodes table
CREATE TABLE IF NOT EXISTS public.ecosystem_nodes (
    node_id VARCHAR(100) PRIMARY KEY,
    node_type VARCHAR(100) NOT NULL,
    beachhead_tag VARCHAR(100) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Secure ecosystem nodes table
ALTER TABLE public.ecosystem_nodes ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Service Role Only" 
ON public.ecosystem_nodes FOR ALL 
USING (auth.role() = 'service_role');

-- Seed a default node for the synthetic strike test
INSERT INTO public.ecosystem_nodes (node_id, node_type, beachhead_tag)
VALUES ('rpi-01', 'Raspberry Pi 4', 'microgreen-greenhouse-01')
ON CONFLICT (node_id) DO NOTHING;
