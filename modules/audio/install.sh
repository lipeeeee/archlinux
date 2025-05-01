#!/bin/bash

# 1. Set variables
SCRIPT_DIR=$(dirname $0)
set -e

# 2. Define actions
install() {
  sudo pacman -S pipewire wireplumber pipewire-pulse --noconfirm

  # Handle services
  systemctl --user enable wireplumber
  systemctl --user enable pipewire 
}

link_configs() {
  :
}

# 3. Execute all
install
link_configs
