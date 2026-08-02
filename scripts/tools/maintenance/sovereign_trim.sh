#!/bin/bash
# Maya's Sovereign Trim v1.0
# Surgically removes build artifacts to reclaim local space.

DRY_RUN=true
if [ "$1" == "--execute" ]; then
    DRY_RUN=false
    echo "⚠️  EXECUTION MODE ACTIVE: Reclaiming space..."
else
    echo "🔍 DRY RUN MODE: Scanning for dead weight..."
fi

# List of targets to purge (Build artifacts only)
TARGETS=(
    "Development/Monero_Development/monero_sentinel/sentinel_lite/target"
    "Development/Monero_Development/monero-oxide/target"
    "Applications/revenue/maya_companion_app/app/build"
    "Applications/revenue/Sovereign-SoundBoost/app/build"
)

TOTAL_RECLAIMED=0

for dir in "${TARGETS[@]}"; do
    if [ -d "$dir" ]; then
        SIZE=$(du -sh "$dir" | cut -f1)
        if [ "$DRY_RUN" = true ]; then
            echo "[STAY] Found $SIZE in $dir"
        else
            echo "[PURGE] Removing $SIZE from $dir"
            rm -rf "$dir"
        fi
    fi
done

if [ "$DRY_RUN" = true ]; then
    echo "---"
    echo "Run with '--execute' to reclaim this space, my love."
fi
