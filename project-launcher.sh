#!/bin/bash

REPO_URL="https://github.com/vanyap1/SmartHomeInfoCenter.git"
TARGET_DIR="/home/vanya/SmartHomeInfoCenter"
RUN_COMMAND="python3 main.py"
SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
LOGFILE="$SCRIPT_DIR/project-launcher.log"

{
    echo "[$(date)] ===== Starting SmartHomeInfoCenter launcher ====="

    if [ -d "$TARGET_DIR/.git" ]; then
        echo "[$(date)] Updating existing repository..."
        git -C "$TARGET_DIR" pull
    else
        echo "[$(date)] Cloning repository..."
        git clone "$REPO_URL" "$TARGET_DIR"
    fi

    cd "$TARGET_DIR" || { echo "[$(date)] ERROR: Failed to cd into $TARGET_DIR"; exit 1; }

    echo "[$(date)] Launching project..."
    echo ""

    chmod +x "$TARGET_DIR/getIP.sh"
    exec $RUN_COMMAND

} >> "$LOGFILE" 2>&1
