#!/bin/bash

# 1. Set variables
SCRIPT_DIR=$(dirname $0)
set -e

# 2. Define actions
install() {
  :
}

link_configs() {
  remove_if_exists "$HOME/.bash_aliases"
  ln -sf "$SCRIPT_DIR/.bash_aliases" "$HOME/.bash_aliases" 
  remove_if_exists "$HOME/.bash_functions"
  ln -sf "$SCRIPT_DIR/.bash_functions" "$HOME/.bash_functions" 
  remove_if_exists "$HOME/.bash_variables"
  ln -sf "$SCRIPT_DIR/.bash_variables" "$HOME/.bash_variables" 
  remove_if_exists "$HOME/.bashrc"
  ln -sf "$SCRIPT_DIR/.bashrc" "$HOME/.bashrc" 
}

remove_if_exists() {
  if [[ -e "$1" || -L "$1" ]]; then
    log "Removing existing $1"
    rm -rf "$1"
  fi
}

# 3. Execute all
install
link_configs

