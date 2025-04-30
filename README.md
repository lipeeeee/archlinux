# archlinux dotfiles
archlinux dotfiles and auto-installer/updater

# ArchManagerPY (auto-installer/updater/system manager)
A simple Python script with less than 200 lines to manage your Arch Linux dotfiles modules by automating installs, updates, and optional system snapshots.

# Top-Level Overview
1. Core Actions

- INSTALL: Initialize or symlink new modules

- UPDATE: Apply in-place updates to existing modules

- BACKUP: (optional) Runs your own snapshot script

2. Interactive Confirmation

- Displays parsed arguments and discovered modules

- Prompts “y/n” before proceeding

# Prerequisites
- Python ≥ 3.9

- Your own dependencies pre-module installation

# How to use it
1. **Directory Layout**
Modularize dotfiles like such:
```bash
.
├── manager.py         # This core script
├── modules/
│   ├── module1/       # that contains install.sh and/or update.sh
│   ├── module2/       # that contains install.sh and/or update.sh
│   └── moduleN/       # that contains install.sh and/or update.sh
└── scripts/
    └── backup.sh      # customized script invoked for system snapshots
```

Ensure folders exist:
- modules/ — each subfolder is a standalone module with install.sh &/or update.sh
- scripts/backup.sh — your custom backup routine

2. **Run the manager:**
```bash
python3 manager.py [options]
```
- -i, --install Run INSTALL actions

- -u, --update Run UPDATE actions

- -b, --backup Make Timeshift backups before & after

- --ignore-errors Continue on any module script failures

# TODO
update drivers script and add it to maintenance
make github actions archlinux jobs that runs manager with all flags
