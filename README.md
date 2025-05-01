# archlinux dotfiles
archlinux dotfiles and auto-installer/updater

# ArchManagerPY (auto-installer/updater/system manager)
A Python script with less than 200 lines to manage your Arch Linux dotfiles modules by automating installs, updates, and optional system snapshots.

---

```bash
python3 manager.py --help
```
![image](https://github.com/user-attachments/assets/70353559-d079-45ef-94b2-34b26ed7d34b)


```bash
python3 manager.py -ib --ignore-errors
```
![image](https://github.com/user-attachments/assets/964ec8b6-695e-44a1-a0f5-749859d0fa23)

---

Will also work on most popular linux distros since all instalation logic is implemented per-distro in the module's scripts.

## Top-Level Overview

Core Actions:

- INSTALL: Initialize or symlink new modules

- UPDATE: Apply in-place updates to existing modules

- BACKUP: (optional) Runs your own snapshot script


## Prerequisites
- Python ≥ 3.9

- Your own dependencies pre-module installation

## How to use it
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
- update drivers script and add it to maintenance
- complement_bashrc
- node module
- lazygit module ?
