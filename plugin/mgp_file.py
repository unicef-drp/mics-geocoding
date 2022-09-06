## ###########################################################################
##
# Utils.py
##
# Author: Etienne Delclaux
# Created: 17/03/2021 11:15:56 2016 (+0200)
##
# Description:
##
## ###########################################################################

import typing
import platform
import subprocess
import os


def openFile(file: str) -> typing.NoReturn:
    """ add a convenient method that checks if a layer crosses the antimeridian
    """
    if file:
        if platform.system() == 'Darwin':       # macOS
            subprocess.call('open', file)
        elif platform.system() == 'Windows':    # Windows
            os.startfile(file)
        else:                                   # linux variants
            subprocess.call('xdg-open', file)
