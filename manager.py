__doc__ = """
    Manager for my archlinux instalation
    
    - Handles installing new instances, updating modules & system maintenance.

    - How to run:
    python3 manager.py -{i/u} -s

    - Requirements:
    python3.8+
    ssh git setup
"""
# 1. USE ONLY CORE PYTHON MODULES
# 3. HANDLES MODULE ERRORS (-s TO STOP ON FIRST ERROR)
# 4. IMPORTANT! PROPPER LOGGING OF DATA
# 5. IF PATH IS IMPORTANT MAKE SURE TO VERIFY(FOR EXAMPLE MUST BE IN $HOME/archlinux)
# 7. IMPORTANT! PRESENTS SUMMARY BEFORE EXECUTING TASKS AND ASKS Y/N TO CONTINUE
# 8. -200 lines
# 9. ignored_modules as arg? -y as do it anyway flag?

# - os.path.realpath(os.curdir) -> gives current script path
# - os.fwalk(path) -> gives a list of dirs and files of path
# however the first instnace is always a "summary" of the root folder
# can hack this in a way where we skip summary by doing x.__next__() befor iter
# To make a quick summary of found modules we can do x.__next__()[1] on first iter
# and that would make use of the summary AND get rid of the summary at the same time

# BACKUP = if backup flag passed, a backup should be done before & after runtime
# Backup saves should be saved like 'PRE/POST-MANAGER:$date'
# however if its a new instance and timeshift is not installed, it should just ignore

import sys, os
import copy
import logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(funcName)s:%(lineno)s - %(message)s')

from argparse import ArgumentParser
from enum import Enum

# globals
ignored_modules = []
parser = ArgumentParser(prog="ArchManagerPY")
logger = logging.getLogger(__name__)
managerpy_directory = os.path.realpath(os.curdir)
managerpy_modules_path = os.path.join(managerpy_directory, "modules/")

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
    parser.add_argument("-b", "--backup", help="backup action flag", action="store_true")
    parser.add_argument("-f", "--force", help="force, ignoring errors flag", action="store_true")
    args = parser.parse_args()

    # Processing should be done in the priority order(FIFO).
    actions = list[ScriptParams.Action]()
    if args.install: actions.append(ScriptParams.Action.INSTALL)
    if args.update: actions.append(ScriptParams.Action.UPDATE)

    return ScriptParams(actions, args.force, args.backup)

# Override of List.__subt__
# TODO: If .__contains__ does a full loop through the list(On) this will be On^2
# To make this func On, use exception based removal
def list_subt_override(list1: list, list2: list) -> list:
    flist = copy.copy(list1)
    for x in flist:
        if list2.__contains__(x): flist.remove(x)
    return flist

def ask_yes_no(prompt: str) -> bool:
    return input(prompt + " (y/n): ").strip().lower() in ("y", "yes")

if __name__ == "__main__":
    logger.info("Initializing ArchManagerPY...")

    # Modules directory gen
    assert os.path.isdir(managerpy_modules_path), f"Could not find modules folder in {managerpy_directory}"
    modules_gen = os.fwalk(managerpy_modules_path)

    # Script params
    try:
        sp = parse_args()
    except Exception as e:
        logger.error(e)
        parser.print_help()
        sys.exit(1)

    found_modules:list[str] = modules_gen.__next__()[1]
    affected_modules:list[str] = list_subt_override(found_modules, ignored_modules)
    
    # TODO: get all modules and then list everything (with `ignored_modules`) and ask_yes_no
    logger.info("------ Parsed Arguments Summary " + "-"*32)
    logger.info(f"Actions received\t: {sp.actions}")
    logger.info(f"Ignoring errors\t? {sp.ignore_errors}")
    logger.info(f"Backing up     \t? {sp.backup}")
    logger.info("------ Modules Summary " + "-"*(64-23))
    logger.info(f"Found modules\t: {found_modules}")
    logger.info(f"Ignored modules\t: {ignored_modules}")
    logger.info(f"Will be affected\t: {affected_modules}")
    logger.info("-"*(32+32))
    if not ask_yes_no("Do you agree with the shown information?"):
        sys.exit(0)

