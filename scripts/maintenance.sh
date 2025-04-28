#!/bin/bash
# arch system maintenance script

# Step 1: Create a Timeshift backup
echo "==> Creating a Timeshift snapshot..."
sudo timeshift --create --comments "Automatic pre-update backup" --tags D

# Step 2: Update system packages
echo "==> Updating system packages..."
sudo pacman -Syu --noconfirm

# Step 3: Remove orphaned packages
echo "==> Cleaning orphaned packages..."
orphans=$(pacman -Qdtq)
if [ -n "$orphans" ]; then
    sudo pacman -Rns --noconfirm $orphans
else
    echo "No orphans to remove."
fi

# Step 4: Clean package cache (keep last 3 versions)
echo "==> Cleaning package cache..."
sudo paccache -rk3

echo "==> System maintenance complete. Backup created and system updated."
