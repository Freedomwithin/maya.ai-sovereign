#!/bin/bash
cd /home/jonathon/gemini-jules/maya/projects/AGI-Sentinel-v4/core

# 1. Psychology Contradiction Hunter
echo "[Ubuntu Strike] Launching Psychology Contradiction Hunter..."
python3 sovereign_swarm_engine_v3.py \
  --swarm "psychology_contradiction_hunter" \
  --mission "Load psychology_ledger.json. Identify any contradictory claims among the 20 entries. For each contradiction, output the two conflicting claims and which has stronger empirical support. If none, output 'NO CONTRADICTIONS FOUND'." \
  --roles "Logic_Verifier,Literature_Reviewer,Critic,Synthesizer" \
  --mins 20 --rest 60 --pillar psychology --auto-report > ../reports/ubuntu/psychology_contradictions.out 2>&1

# 2. B2B Validation Strike
echo "[Ubuntu Strike] Launching B2B Validation Strike..."
python3 sovereign_swarm_engine_v3.py \
  --swarm "b2b_validation_strike" \
  --mission "For each of the three B2B opportunities (Docker Swarm autoscaler, Maryland Compliance Sentinel, AI-HVAC Manual J tool), find 3 recent Reddit/HN/forum posts from the last 3 months where people explicitly complain about the problem. Extract exact quotes. If fewer than 3 per opportunity, output 'INSUFFICIENT DATA'." \
  --roles "Market_Researcher,Data_Collector,Critic,Synthesizer" \
  --mins 25 --rest 60 --pillar economics --auto-report > ../reports/ubuntu/b2b_validation.out 2>&1

# 3. Docker Swarm Autoscaler Market Research
echo "[Ubuntu Strike] Launching Docker Swarm Autoscaler Market..."
python3 sovereign_swarm_engine_v3.py \
  --swarm "docker_autoscaler_market" \
  --mission "Find existing tools or GitHub repos that attempt to autoscale Docker Swarm worker nodes on any cloud (Hetzner, DigitalOcean, Vultr, AWS). For each, list: (1) name/URL, (2) last commit date, (3) a one-sentence summary of how it works, (4) user complaints from issues/Reddit. If no active tool exists, output 'INSUFFICIENT DATA - market gap confirmed'." \
  --roles "DevOps_Researcher,Market_Analyst,Critic,Synthesizer" \
  --mins 20 --rest 60 --pillar economics --auto-report > ../reports/ubuntu/docker_autoscaler_market.out 2>&1

echo "[Ubuntu Strike] All missions complete."
