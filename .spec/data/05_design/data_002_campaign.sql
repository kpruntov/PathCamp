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
