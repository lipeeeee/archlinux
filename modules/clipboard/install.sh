#!/bin/bash

# 1. Set variables
SCRIPT_DIR=$(dirname $0)
set -e

# 2. Define actions
install() {
  sudo pacman -S wl-clipboard cliphist --noconfirm
}

# 3. Execute all
install
