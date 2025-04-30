#!/bin/bash
# Takes in a string as $arg1 and creates timeshift backup with $arg1 as comment
# Exits with 0 if timeshift not installed and ignores backup

# Leave on error
set -euo pipefail

# Check if a comment was provided
if [[ $# -lt 1 ]]; then
  echo "Usage: $0 \"Snapshot comment\""
  exit 1
fi

COMMENT="$1"

# Check if timeshift is installed
if ! command -v timeshift &> /dev/null; then
  echo "Timeshift is not installed. Skipping snapshot."
  exit 0
fi

# Create snapshot with daily tag
sudo timeshift --create --comments "$COMMENT" --tags D

echo "Snapshot created with comment: $COMMENT"

