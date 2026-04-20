"""Create initial tables

Revision ID: 212bfb58a1cd
Revises: 
Create Date: 2026-04-15 20:45:51.723289

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '212bfb58a1cd'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
    -- SQL DDL for the User entity
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(255) UNIQUE NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        status VARCHAR(50) NOT NULL DEFAULT 'Active',
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );

    -- SQL DDL for the Campaign entity
    CREATE TABLE campaigns (
        id SERIAL PRIMARY KEY,
        gm_user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        name VARCHAR(255) NOT NULL,
        description TEXT,
        party_size INTEGER NOT NULL,
        party_level INTEGER NOT NULL,
        share_token VARCHAR(255) UNIQUE,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );

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
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""
    DROP INDEX idx_monsters_rarity;
    DROP INDEX idx_monsters_level;
    DROP INDEX idx_monsters_name;
    DROP TABLE monsters;
    DROP TABLE encounters;
    DROP TABLE assets;
    DROP TABLE ticks;
    DROP TABLE campaigns;
    DROP TABLE users;
    """)

# @trace TASK-006
