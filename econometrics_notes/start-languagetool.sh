#!/bin/bash

# LanguageTool Server Startup Script
# Starts grammar/spell check server on port 8081

TOOLS_DIR="$(cd "$(dirname "$0")" && pwd)/tools"
mkdir -p "$TOOLS_DIR"

cd "$TOOLS_DIR"

# Check if LanguageTool is already downloaded
if [ ! -d "LanguageTool-"* ]; then
    echo "Downloading LanguageTool..."
    
    # Direct download of latest release (v6.5 as of Mar 2026)
    LATEST="https://github.com/languagetool-org/languagetool/releases/download/v6.5/LanguageTool-6.5.zip"
    
    echo "Downloading from: $LATEST"
    curl -L "$LATEST" -o languagetool.zip
    
    if [ ! -f languagetool.zip ]; then
        echo "Error: Download failed"
        exit 1
    fi
    
    echo "Extracting..."
    unzip -q languagetool.zip
    rm -f languagetool.zip
fi

# Find and start the server
LT_DIR=$(ls -d LanguageTool-* 2>/dev/null | head -1)

if [ -z "$LT_DIR" ]; then
    echo "Error: LanguageTool directory not found"
    exit 1
fi

cd "$LT_DIR"

echo "Starting LanguageTool server on port 8081..."
echo "Server will be available at: http://localhost:8081"
echo "Press Ctrl+C to stop"
echo ""

java -jar languagetool-server.jar --port 8081
