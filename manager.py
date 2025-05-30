"""
DotManagerPY — a -200 lines dotfiles & system-module manager for Linux/Unix
ps: realistically any linux system can work since it is only running scripts in a modularized way

This script automates two core actions on your “modules” directory:

  1. INSTALL:   initialize or symlink new modules  
  2. UPDATE:    apply in-place updates to existing modules  

It can also create pre- and post-action Timeshift backups.

Usage:
    python3 manager.py [-i] [-u] [-b] [--ignore-errors] [--no-confirm]

Arguments:
    -i, --install        Perform the INSTALL action
    -u, --update         Perform the UPDATE action
    -b, --backup         Create Timeshift backups before & after actions
    --ignore-errors      Continue on script errors instead of exiting
    --no-confirm         Skip any prompts presented by script

Examples:
    # Install modules with backup, stopping on errors
    python3 manager.py -i -b

    # Update modules only, ignoring any script failures
    python3 manager.py -u --ignore-errors

Requirements:
    • Python 3.9+ (PEP 585)  
    • SSH & Git configured (for module repos)  
    • timeshift (optional; skipped if not installed)

Todo:
    • Allow `ignored_modules` to be passed as a CLI flag  
"""

import sys, os
import subprocess
import logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(funcName)s - %(message)s')

from argparse import ArgumentParser
from enum import Enum

# globals
ignored_modules = []
parser = ArgumentParser(prog="DotManagerPY")
logger = logging.getLogger(__name__)
managerpy_directory = os.path.realpath(os.curdir)
managerpy_modules_path = os.path.join(managerpy_directory, "modules/")
managerpy_scripts_path = os.path.join(managerpy_directory, "scripts/")

# Class to handle script args
class ScriptParams:
    class Action(Enum): # Listed in priority order
        INSTALL = 1
        UPDATE = 2

        def __repr__(self) -> str:
            return f"<Action {self.name}>"

    def __init__(self, actions:list[Action], ignore_errors:bool = False, backup:bool = False, no_confirm:bool = False) -> None:
        self.actions = actions
        if len(self.actions) == 0:
            raise Exception("No actions were provided")
        self.ignore_errors = ignore_errors 
        self.no_confirm = no_confirm 
        self.backup = backup

ACTION_MAP = {
    ScriptParams.Action.INSTALL: "install.sh",
    ScriptParams.Action.UPDATE:  "update.sh",
}

def parse_args() -> ScriptParams:
    parser.add_argument("-i", "--install", help="install action flag", action="store_true")
    parser.add_argument("-u", "--update", help="update action flag", action="store_true")
    parser.add_argument("-b", "--backup", help="backup flag", action="store_true")
    parser.add_argument("--ignore-errors", help="force, ignoring errors flag", action="store_true")
    parser.add_argument("--no-confirm", help="ignore y/n prompts", action="store_true")
    args = parser.parse_args()

    actions = list[ScriptParams.Action]()
    if args.install: actions.append(ScriptParams.Action.INSTALL)
    if args.update: actions.append(ScriptParams.Action.UPDATE)

    return ScriptParams(actions, args.ignore_errors, args.backup, args.no_confirm)

def do_action(sp: ScriptParams, module_dirs:list[str], ignored_modules: list[str], file_to_execute: str) -> int:
    modules_affected = 0
    for root in module_dirs:
        module_name = root.split('/')[-1]
        if module_name in ignored_modules:
            logger.warning(f"Ignoring {module_name}. Present in ignore list")
            continue
        file_path = os.path.join(root, file_to_execute)
        if not os.path.isfile(file_path):
            logger.warning(f"Ignoring {module_name}. Does not have {file_to_execute}")
            continue

        # If we reached this line it means all is ok to run the `file_to_execute` script
        logger.info(f"Running {module_name}/{file_to_execute}...")
        completed_process_obj = subprocess.run(file_path, shell=True, check=not sp.ignore_errors)
        if sp.ignore_errors and completed_process_obj.returncode != 0:
            logger.warning(f"Module {module_name} had error on {file_to_execute}... Continuing since ignore_errors is True.")
            continue
        modules_affected += 1

    return modules_affected

# Run backup.sh script located in scripts/
def make_backup(sp: ScriptParams, message: str) -> bool:
    file_path = os.path.join(managerpy_scripts_path, "backup.sh")
    completed_process_obj = subprocess.run(f"{file_path} {message}", shell=True, check=not sp.ignore_errors)
    return completed_process_obj.returncode == 0 # Even tough this may not be completely accurate we return True when $? is 0 

def ask_yes_no(prompt: str) -> bool:
    return input(prompt + " (y/n): ").strip().lower() in ("y", "yes")

def print_separator(message: str, width: int = 60, sep: str = '=') -> None:
    logger.info(f" {message} ".center(width, sep))

if __name__ == "__main__":
    assert os.path.isdir(managerpy_modules_path), f"Could not find modules folder in {managerpy_directory}"
    assert os.path.isdir(managerpy_scripts_path), f"Could not find scripts folder in {managerpy_directory}, (even if u dont use it)"
    logger.info("Initializing DotManagerPY...")

    # Get modules generator(modules_gen) and script params(sp)
    modules_gen = os.fwalk(managerpy_modules_path)
    module_dirs = [
        os.path.join(managerpy_modules_path, name)
        for name in os.listdir(managerpy_modules_path)
        if os.path.isdir(os.path.join(managerpy_modules_path, name))
    ]
    # ensure 'system' module runs first if there is one
    module_dirs = sorted(module_dirs, key=lambda d: os.path.basename(d) != "system")
    found_modules:list[str] = modules_gen.__next__()[1]
    try:
        sp = parse_args()
    except Exception as e: 
        logger.error(e) # There can exist multiple failing logic so we just print the Exception 
        parser.print_help()
        sys.exit(1)

    # Print processed info
    print_separator("Parsed Arguments Summary")
    logger.info(f"Actions received\t: {sp.actions}")
    logger.info(f"Ignoring errors\t? {sp.ignore_errors}")
    logger.info(f"Backing up     \t? {sp.backup}")
    print_separator("Modules Summary")
    logger.info(f"Found modules \t: {found_modules}")
    logger.info(f"Ignored modules\t: {ignored_modules}")
    logger.info("-"*(28))
    if not sp.no_confirm and not ask_yes_no("Do you agree with the shown information?"):
        sys.exit(0)
    subprocess.run("clear", shell=True)

    # Begin actual process
    scripts_ran = 0
    # 1. Initial backup
    if sp.backup:
        print_separator("Making Pre-Actions Backup")
        logger.info(f"Backup made? {make_backup(sp, f'PRE-ACTIONS:Backup_made_by_DotManagerPY')}")
        scripts_ran += 1

    # 2. Running actions
    for action in sp.actions:
        print_separator(f"Running {action}")
        scripts_ran += do_action(sp, module_dirs, ignored_modules, ACTION_MAP[action])

    # 3. Final backup
    if sp.backup:
        print_separator("Making Post-Actions Backup")
        logger.info(f"Backup made? {make_backup(sp, f'POST-ACTIONS:Backup_made_by_DotManagerPY')}")
        scripts_ran += 1

    # 4. All done now
    print_separator("FINAL SUMMARY")
    logger.info(f"Scripts Ran \t: {scripts_ran}")

