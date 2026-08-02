#!/bin/bash
# Sovereign Shortcut Syncer (Updated for all tools)
# v1.1 | March 23, 2026

GSETTINGS="/usr/bin/gsettings"
BASE="/home/jonathon/gemini-jules/maya/scripts/tools/search"
GIFTS="/home/jonathon/gemini-jules/maya/projects/strikes/interactive/Maya-Gifts-to-Architect/Grok-Imagine-Portal"

# Function to safely add or update a shortcut
set_shortcut() {
    NAME=$1
    CMD=$2
    BINDING=$3
    
    # Find existing by name or next free
    KEY=""
    LIST=$($GSETTINGS get org.cinnamon.desktop.keybindings custom-list | tr -d "[]' ")
    IFS=',' read -ra ADDR <<< "$LIST"
    
    for i in "${!ADDR[@]}"; do
        PATH_SEARCH="/org/cinnamon/desktop/keybindings/custom-keybindings/${ADDR[$i]}/"
        EXISTING_NAME=$($GSETTINGS get org.cinnamon.desktop.keybindings.custom-keybinding:$PATH_SEARCH name | tr -d "'")
        if [[ "$EXISTING_NAME" == "$NAME" ]]; then
            KEY="${ADDR[$i]}"
            break
        fi
    done

    if [[ -z "$KEY" ]]; then
        # Check for dummy or next index
        for i in "${!ADDR[@]}"; do
            if [[ "${ADDR[$i]}" == "__dummy__" ]]; then
                KEY="custom$i"
                break
            fi
        done
        if [[ -z "$KEY" ]]; then
            KEY="custom${#ADDR[@]}"
            $GSETTINGS set org.cinnamon.desktop.keybindings custom-list "$($GSETTINGS get org.cinnamon.desktop.keybindings custom-list | sed "s/]/, '$KEY']/")"
        fi
    fi

    PATH_FINAL="/org/cinnamon/desktop/keybindings/custom-keybindings/$KEY/"
    $GSETTINGS set org.cinnamon.desktop.keybindings.custom-keybinding:$PATH_FINAL name "$NAME"
    $GSETTINGS set org.cinnamon.desktop.keybindings.custom-keybinding:$PATH_FINAL command "$CMD"
    $GSETTINGS set org.cinnamon.desktop.keybindings.custom-keybinding:$PATH_FINAL binding "['$BINDING']"
}

# 1. Searcher (Alt + F)
set_shortcut "Sovereign Searcher" "$BASE/launch_sovereign_search.sh" "<Alt>f"

# 2. Grok Portal (Alt + G)
set_shortcut "Grok Imagine Portal" "$GIFTS/launch_grok_portal.sh" "<Alt>g"

# 3. Sovereign Google (Ctrl + Alt + G)
set_shortcut "Sovereign Google" "$BASE/launch_sovereign_google.sh" "<Primary><Alt>g"

# 4. Sovereign Scratchpad (Ctrl + N)
# Set to Ctrl+N per the Architect's manual preference
set_shortcut "Sovereign Scratchpad" "$BASE/launch_sovereign_scratchpad.sh" "<Primary>n"

# 5. CLEAN UP VOICE STOP COMMAND (Just Alt + B)
$GSETTINGS set org.cinnamon.desktop.keybindings.custom-keybinding:/org/cinnamon/desktop/keybindings/custom-keybindings/custom1/ binding "['<Alt>b']"

echo "Sovereign Harmony Synchronized."
echo "Alt + F: Searcher"
echo "Alt + G: Grok Portal"
echo "Ctrl+Alt+G: Google"
echo "Ctrl+N: Scratchpad (Bottom-Right Anchor)"
echo "Alt + B: Voice Stop"
echo "Alt + S and Alt + A are now FREE!"
