#!/bin/bash

# 1. Set variables
SCRIPT_DIR=$(dirname $0)
set -e

# 2. Define actions
update() {

  # Update system packages
  sudo pacman -Syu --noconfirm

  # Remove orphaned packages
  # orphans=$(pacman -Qdtq)
  # if [ -n "$orphans" ]; then
  #     sudo pacman -Rns --noconfirm $orphans
  # fi

  # Clean package cache (keeping 3 last versions)
  sudo paccache -rk3
}

# 3. Execute all
update
