-- SQL DDL for the Timeline, Asset, and Encounter entities

-- Ticks represent a point in time within a campaign.
CREATE TABLE ticks (
    id SERIAL PRIMARY KEY,
    campaign_id INTEGER NOT NULL REFERENCES campaigns(id) ON DELETE CASCADE,
    tick_number INTEGER NOT NULL,
    narrative TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(campaign_id, tick_number)
);

-- Assets are entities that exist within a tick, such as Scenes, NPCs, or items.
CREATE TABLE assets (
    id SERIAL PRIMARY KEY,
    tick_id INTEGER NOT NULL REFERENCES ticks(id) ON DELETE CASCADE,
    asset_type VARCHAR(100) NOT NULL, -- e.g., 'Scene', 'NPC', 'Location', 'Front'
    name VARCHAR(255) NOT NULL,
    description TEXT,
    traits JSONB, -- Store traits as a JSON array of strings
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Encounters store the generated mechanical data for a specific scene asset.
CREATE TABLE encounters (
    id SERIAL PRIMARY KEY,
    asset_id INTEGER NOT NULL REFERENCES assets(id) ON DELETE CASCADE,
    mechanical_data JSONB NOT NULL,
    gm_narrative TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
