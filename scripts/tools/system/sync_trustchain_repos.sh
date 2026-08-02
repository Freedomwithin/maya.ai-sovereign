#!/bin/bash

# --- TrustChain Sovereign Sync Script ---
# Selectively syncs hardened V3.1 logic from dev repos to deployment repos.

BASE_DIR="/home/jonathon/gemini-jules/maya/projects"

# 1. Backend Sync (Core-V3 -> Backend)
echo "🛡️ Syncing TrustChain Backend logic..."
cp "$BASE_DIR/TrustChain-Core-V3/hono_edge.ts" "$BASE_DIR/TrustChain-Backend/hono_edge.ts"
cp "$BASE_DIR/TrustChain-Core-V3/server.ts" "$BASE_DIR/TrustChain-Backend/server.ts"
cp "$BASE_DIR/TrustChain-Core-V3/agents/RiskAuditorAgent.js" "$BASE_DIR/TrustChain-Backend/agents/RiskAuditorAgent.js"
cp "$BASE_DIR/TrustChain-Core-V3/tests/agent.test.js" "$BASE_DIR/TrustChain-Backend/tests/agent.test.js"
mkdir -p "$BASE_DIR/TrustChain-Backend/src/api"
cp "$BASE_DIR/TrustChain-Core-V3/src/api/verify.ts" "$BASE_DIR/TrustChain-Backend/src/api/verify.ts"
mkdir -p "$BASE_DIR/TrustChain-Backend/src/services"
cp "$BASE_DIR/TrustChain-Core-V3/src/services/notary_sync.ts" "$BASE_DIR/TrustChain-Backend/src/services/notary_sync.ts"

# 2. Frontend Sync (HUD-V3 -> Frontend)
echo "🌐 Syncing TrustChain Frontend SDK logic..."
cp "$BASE_DIR/TrustChain-HUD-V3/src/sdk/useTrustChain.js" "$BASE_DIR/TrustChain-Frontend/src/sdk/useTrustChain.js"
cp "$BASE_DIR/TrustChain-HUD-V3/src/sdk/useTrustChain.test.jsx" "$BASE_DIR/TrustChain-Frontend/src/sdk/useTrustChain.test.jsx"

echo "✅ Selective Sync Complete. (Vercel configs and lockfiles preserved)."
