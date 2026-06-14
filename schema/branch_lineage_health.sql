-- Track branch lineage health
CREATE TABLE branch_lineage_health (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    repository VARCHAR(100) NOT NULL, -- e.g., 'coastal-alpine-stack'
    base_branch VARCHAR(100) NOT NULL,
    compare_branch VARCHAR(100) NOT NULL,
    status VARCHAR(50) NOT NULL, -- 'identical', 'ahead', 'behind', 'diverged', 'orphaned'
    common_ancestor_sha VARCHAR(40),
    last_checked TIMESTAMPTZ DEFAULT NOW()
);

-- Secure the perimeter
ALTER TABLE branch_lineage_health ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Service Role Only" 
ON branch_lineage_health FOR ALL 
USING (auth.role() = 'service_role');
