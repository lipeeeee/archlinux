#!/bin/bash

# 1. Set variables
SCRIPT_DIR=$(dirname $0)
set -e

# 2. Define actions
install() {
  sudo pacman -S nnn --noconfirm
}

link_configs() {
  DST_DIR="$HOME/.config/nnn"
  if [[ -e $DST_DIR || -L $DST_DIR ]]; then
    echo "Removing existing $DST_DIR"
    rm -rf "$DST_DIR"
  fi

  ln -sf "$SCRIPT_DIR/.config/nnn" $DST_DIR
}

# 3. Execute all
install
link_configs
