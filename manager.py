__doc__ = """
    Manager for my archlinux instalation
    
    - Handles installing new instances, updating modules & system maintenance.

    - This script revolves around 2 actions(INSTALL and UPDATE) and adapting to arguments given
    INSTALL: will setup modules for the first time and symlink 
    UPDATE:  handle updates inplace for modules

    - How to run:
    python3 manager.py -{i/u} -bf

    - Requirements:
    python3.8+
    ssh git setup
"""

# Warning: On git clone, files might not have the permissions set correctly

# 1. USE ONLY CORE PYTHON MODULES
# 2. HANDLES MODULE ERRORS (-s TO STOP ON FIRST ERROR)
# 3. -200 lines
# 4. ignored_modules as arg? -y as do it anyway flag?

# if its a new instance and timeshift is not installed, it should just ignore

# ! research bash script base skeleton for scripts (scripts/ and install.sh, update.sh in each module) !
# make backup/snapshot script that takes $1 arg as --comment $2 as stop flag

# make __doc__ better

import sys, os
import itertools
import subprocess
import logging
from typing import Iterator
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(funcName)s - %(message)s')

from argparse import ArgumentParser
from enum import Enum

# globals
ignored_modules = []
parser = ArgumentParser(prog="ArchManagerPY")
logger = logging.getLogger(__name__)
managerpy_directory = os.path.realpath(os.curdir)
managerpy_modules_path = os.path.join(managerpy_directory, "modules/")
managerpy_scripts_path = os.path.join(managerpy_directory, "scripts/")

# Class to handle script args
class ScriptParams:
    class Action(Enum): # Listed in priority order
        INSTALL = 1
        UPDATE = 2

    def __init__(self, actions:list[Action], ignore_errors:bool = False, backup:bool = False) -> None:
        self.actions = actions
        if len(self.actions) == 0:
            raise Exception("No actions were provided")
        self.ignore_errors = ignore_errors 
        self.backup = backup

    def __repr__(self) -> str: # DEBUG
        return f"<ScriptParams actions={self.actions} ignore_errors={self.ignore_errors} backup={self.backup}>"

def parse_args() -> ScriptParams:
    parser.add_argument("-i", "--install", help="install action flag", action="store_true")
    parser.add_argument("-u", "--update", help="update action flag", action="store_true")
    parser.add_argument("-b", "--backup", help="backup flag", action="store_true")
    parser.add_argument("--ignore-errors", help="force, ignoring errors flag", action="store_true")
    args = parser.parse_args()

    # Processing should be done in the priority order(FIFO).
    actions = list[ScriptParams.Action]()
    if args.install: actions.append(ScriptParams.Action.INSTALL)
    if args.update: actions.append(ScriptParams.Action.UPDATE)

    return ScriptParams(actions, args.ignore_errors, args.backup)

def do_action(sp: ScriptParams, module_generator:Iterator, ignored_modules: list[str], file_to_execute: str) -> int:
    modules_affected = 0
    for root, dirs, files, rootfd in module_generator:
        module_name = root.split('/')[-1]
        if module_name in ignored_modules:
            logger.warning(f"Ignoring {module_name}. Present in ignore list")
            continue
        file_path = os.path.join(root, file_to_execute)
        if not os.path.isfile(file_path):
            logger.warning(f"Ignoring {module_name}. Does not have {file_to_execute}")
            continue

        # If we reached this line it means all is ok to run the `file_to_execute` script
        subprocess.run([file_path], shell=True, check=not sp.ignore_errors)

    return modules_affected

def make_backup(message: str) -> bool:
    return True

def ask_yes_no(prompt: str) -> bool:
    return input(prompt + " (y/n): ").strip().lower() in ("y", "yes")

def print_separator(message: str, width: int = 60, sep: str = '=') -> None:
    logger.info(f" {message} ".center(width, sep))

if __name__ == "__main__":
    assert os.path.isdir(managerpy_modules_path), f"Could not find modules folder in {managerpy_directory}"
    assert os.path.isdir(managerpy_scripts_path), f"Could not find scripts folder in {managerpy_directory}"
    logger.info("Initializing ArchManagerPY...")

    # Get modules generator(modules_gen) and script params(sp)
    modules_gen = os.fwalk(managerpy_modules_path)
    install_gen, update_gen = itertools.tee(modules_gen) # We have to make copies of the original generator
    found_modules:list[str] = modules_gen.__next__()[1]
    try:
        sp = parse_args()
    except Exception as e: 
        logger.error(e) # There can exist multiple failing logic so we just print the Exception 
        parser.print_help()
        sys.exit(1)
    
    print_separator("Parsed Arguments Summary")
    logger.info(f"Actions received\t: {sp.actions}")
    logger.info(f"Ignoring errors\t? {sp.ignore_errors}")
    logger.info(f"Backing up     \t? {sp.backup}")
    print_separator("Modules Summary")
    logger.info(f"Found modules \t: {found_modules}")
    logger.info(f"Ignored modules\t: {ignored_modules}")
    logger.info("-"*(28))
    if not ask_yes_no("Do you agree with the shown information?"):
        sys.exit(0)
    subprocess.call("clear")

    # Begin actual process
    # 1. Initial backup
    if sp.backup:
        print_separator("Making Pre-Actions Backup")
        logger.info(f"Backup made? {make_backup(f'PRE-ACTIONS: Backup made by ArchManagerPY')}")

    # 2. Instalation
    if ScriptParams.Action.INSTALL in sp.actions:
        print_separator("Running INSTALL Action")
        do_action(sp, install_gen, ignored_modules, "install.sh")

    # 3. Update
    if ScriptParams.Action.UPDATE in sp.actions:
        print_separator("Running UPDATE Action")
        do_action(sp, update_gen, ignored_modules, "update.sh")

    # 4. Final backup
    if sp.backup:
        print_separator("Making Post-Actions Backup")
        logger.info(f"Backup made? {make_backup(f'POST-ACTIONS: Backup made by ArchManagerPY')}")

