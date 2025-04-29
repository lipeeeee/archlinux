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

# 1. USE ONLY CORE PYTHON MODULES
# 2. HANDLES MODULE ERRORS (-s TO STOP ON FIRST ERROR)
# 3. -200 lines
# 4. ignored_modules as arg? -y as do it anyway flag?

# if its a new instance and timeshift is not installed, it should just ignore

# ! research bash script base skeleton for scripts (scripts/ and install.sh, update.sh in each module) !
# make backup/snapshot script that takes $1 arg as --comment $2 as stop flag

# make __doc__ better

import sys, os
import copy, subprocess
import logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(funcName)s - %(message)s')

from argparse import ArgumentParser
from datetime import datetime
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
    parser.add_argument("-f", "--force", help="force, ignoring errors flag", action="store_true")
    args = parser.parse_args()

    # Processing should be done in the priority order(FIFO).
    actions = list[ScriptParams.Action]()
    if args.install: actions.append(ScriptParams.Action.INSTALL)
    if args.update: actions.append(ScriptParams.Action.UPDATE)

    return ScriptParams(actions, args.force, args.backup)

# Override of List.__subt__ (returns list1 - list2)
# List.__subt__ (On), without __contains__ that would make algorithm (On^2)
def list_subt_override(list1: list, list2: list) -> list:
    flist = copy.copy(list1)
    for x in list2:
        try:
            flist.remove(x)
        except ValueError: # Means value didnt exist in list1
            continue
    return flist

def do_action(sp: ScriptParams, original_module_generator, file_to_execute: str) -> int:
    ...

def action_install(sp: ScriptParams, original_module_generator) -> int:
    # module_generator = copy.copy(original_module_generator) # keep original intact

    # for root, dirs, 
    ...

def action_update(sp: ScriptParams, original_module_generator) -> int:
    ...

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
    try:
        sp = parse_args()
    except Exception as e: 
        logger.error(e) # There can exist multiple failing logic so we just print the Exception 
        parser.print_help()
        sys.exit(1)

    found_modules:list[str] = modules_gen.__next__()[1]
    affected_modules:list[str] = list_subt_override(found_modules, ignored_modules)
    
    print_separator("Parsed Arguments Summary")
    logger.info(f"Actions received\t: {sp.actions}")
    logger.info(f"Ignoring errors\t? {sp.ignore_errors}")
    logger.info(f"Backing up     \t? {sp.backup}")
    print_separator("Modules Summary")
    logger.info(f"Found modules\t: {found_modules}")
    logger.info(f"Ignored modules\t: {ignored_modules}")
    logger.info(f"Will be affected\t: {affected_modules}")
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
        ...

    # 3. Update
    if ScriptParams.Action.UPDATE in sp.actions:
        print_separator("Running UPDATE Action")
        ...

    # 4. Final backup
    if sp.backup:
        print_separator("Making Post-Actions Backup")
        logger.info(f"Backup made? {make_backup(f'POST-ACTIONS: Backup made by ArchManagerPY')}")

