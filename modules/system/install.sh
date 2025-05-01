#!/bin/bash
# This is not a regular module. This is meant to initialize the arch instance
# It will take care if initial setup on a fresh install

# This can be redundant but we just make sure we use bash
chsh -s $(which bash)

# Constants
TMP_DIR="$HOME/tmp"

# Make base directories
# this should be pointing to env$TMP_DIR or env$TMP but since this module must come first
# i havent figured out a better way
mkdir -p $TMP_DIR

# Again, this can be redundant but we just make the OS acknowledge we want
# the latest version even if some of these come pre-installed
sudo pacman -Syu
sudo pacman -S --needed git base-devel --noconfirm
sudo pacman -S sudo python clang openssh wget fzf rsync --noconfirm
sudo pacman -S unzip npm man htop --noconfirm
sudo pacman -S pacman-contrib timeshift --noconfirm # snapshots & system things
sudo pacman -S brightnessctl jq --noconfirm

# Install an AUR helper
if ! command -v yay &> /dev/null; then
  cd $TMP_DIR
  git clone https://aur.archlinux.org/yay.git
  cd yay
  mkpkg -si
fi
