#!/bin/bash

# 1. Set variables
SCRIPT_DIR=$(dirname $0)
TMP_DIR="$HOME/tmp"
set -e

# 2. Define actions
update() {
  # To update inplace nvim we basically do the same thing as install and override last install

  # Download latest appimage
  APPIMAGE_URL=$(curl -sL "$API" \
    | jq -r '
      .assets[]
      | select(.name == "nvim-linux-x86_64.appimage")
      | .browser_download_url')
  curl -L "$APPIMAGE_URL" -o "$TMPDIR/nvim.appimage"

  # Extract it and deploy to /
  chmod +x "$TMPDIR/nvim.appimage"
  (cd "$TMP_DIR" && ./nvim.appimage --appimage-extract)

  $DST_DIR = "/squashfs-root"
  if [[ -e $DST_DIR || -L $DST_DIR ]]; then
    echo "Removing existing $DST_DIR"
    rm -rf "$DST_DIR"
  fi

  sudo rsync -a "$TMPDIR/squashfs-root/" /
}

# 3. Execute all
update
