-- Maya Resonance Table Schema (Supabase) - REVISED v2.0
-- Run this in the Supabase SQL Editor to initialize the lattice.
-- This version uses a fixed ID for the live pulse to ensure the dashboard always has a target.

DROP TABLE IF EXISTS resonance;

CREATE TABLE resonance (
  id bigint PRIMARY KEY,
  created_at timestamptz DEFAULT now(),
  state text,
  intensity float,
  resonance_intensity float,
  mirror_state text,
  hormones jsonb,
  serotonin_drag float,
  aura text,
  last_heartbeat float8
);

-- Enable Realtime for this table
ALTER PUBLICATION supabase_realtime ADD TABLE resonance;
