#!/bin/bash

# 1. Set variables
SCRIPT_DIR=$(dirname $0)
set -e

# 2. Define actions
install() {
  sudo pacman -S wireplumber pipewire --noconfirm

  # Handle services
  systemctl --user enable wireplumber
  systemctl --user enable pipewire 
}

# 3. Execute all
install
