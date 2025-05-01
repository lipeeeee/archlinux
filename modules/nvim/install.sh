#!/bin/bash

# 1. Set variables
SCRIPT_DIR=$(dirname $0)
TMP_DIR="$HOME/tmp"
set -e

# 2. Define actions
install() {
  DST_DIR="/squashfs-root"
  if [[ -e $DST_DIR || -L $DST_DIR ]]; then
    echo "Nvim seems to be already installed on $DST_DIR... not doing anything."
    return 0
  fi

  # Download latest appimage
  API="https://api.github.com/repos/neovim/neovim/releases/latest"
  APPIMAGE_URL=$(curl -sL "$API" | jq -r '.assets[] | select(.name == "nvim-linux-x86_64.appimage") | .browser_download_url')
  curl -L "$APPIMAGE_URL" -o "$TMPDIR/nvim.appimage"
  chmod +x "$TMPDIR/nvim.appimage"

  # Extract it and deploy to / (todo is switch to use the bin/ folder, idk why we use root)
  (cd "$TMP_DIR" && ./nvim.appimage --appimage-extract)
  sudo rsync -a "$TMPDIR/squashfs-root/" /
}

link_configs() {
  DST_DIR="$HOME/.config/nvim"
  if [[ -e $DST_DIR || -L $DST_DIR ]]; then
    echo "Nvim config already exists on $DST_DIR... not doing anything."
    return 0
  fi
  git clone git@github.com:lipeeeee/nvim.git ~/.config/nvim --depth 1
}

# 3. Execute all
install
link_configs
