#!/bin/bash

# 1. Set variables
SCRIPT_DIR=$(dirname $0)
set -e

# 2. Define actions
install() {
  sudo pacman -S swww --noconfirm
}

link_configs() {
  :
}

# 3. Execute all
install
link_configs

