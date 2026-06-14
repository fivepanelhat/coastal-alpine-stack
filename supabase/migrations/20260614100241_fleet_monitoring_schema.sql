-- Track node fleet health
CREATE TABLE node_fleet_health (
    node_id VARCHAR(100) PRIMARY KEY,
    status VARCHAR(50) NOT NULL,
    cpu_temp_celsius NUMERIC,
    memory_usage_percent NUMERIC,
    last_ping TIMESTAMPTZ DEFAULT NOW()
);

-- Secure the perimeter
ALTER TABLE node_fleet_health ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Service Role Only" 
ON node_fleet_health FOR ALL 
USING (auth.role() = 'service_role');
