-- SQL DDL for the Bestiary using a Hybrid Relational/JSONB model

CREATE TABLE monsters (
    -- Relational columns for fast, indexed querying
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    level INTEGER NOT NULL,
    rarity VARCHAR(50),
    size VARCHAR(50),
    
    -- An indexed column to store the unique ID from the source JSON file
    source_id VARCHAR(255) UNIQUE NOT NULL,

    -- JSONB column to store the complete, original monster data
    raw_data JSONB NOT NULL
);

-- Create indexes on frequently queried columns
CREATE INDEX idx_monsters_name ON monsters (name);
CREATE INDEX idx_monsters_level ON monsters (level);
CREATE INDEX idx_monsters_rarity ON monsters (rarity);

-- It can also be beneficial to index specific paths within the JSONB data
-- For example, indexing the traits array
-- CREATE INDEX idx_monsters_traits ON monsters USING GIN ((raw_data -> 'system' -> 'traits' -> 'value'));
