__doc__ = """
    Manager for my archlinux instalation
    
    - Handles installing new instances, updating modules & system maintenance.

    - How to run:
    python3 manager.py -{i/u} -s

    - Requirements:
    python3.13
    ssh git setup
"""

import logging

# 1. USE ONLY CORE PYTHON MODULES
# 2. HANDLES *ONLY* -i and -u FLAGS INDEPENDENTLY
# 3. HANDLES MODULE ERRORS (-s TO STOP ON FIRST ERROR)
# 4. IMPORTANT! PROPPER LOGGING OF DATA
# 5. IF PATH IS IMPORTANT MAKE SURE TO VERIFY(FOR EXAMPLE MUST BE IN $HOME/archlinux)
# 6. --help flag
# 7. VERIFICATION BEFORE DOING TASKS(summary of flags passed and y/n question)
# 8. -200 lines

# d1. Python 3.13+ full support

