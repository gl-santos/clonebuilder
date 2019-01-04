# -*- coding: UTF-8 -*-

"""
@author rpereira
Sep 22, 2011

Modulo de constantes mais frequentes
"""

import os

APP_PATH = os.path.realpath("./") + "/../"

LIST_IDX_NAME = 0
LIST_IDX_PATH = 1
LIST_IDX_OPTION = 2
LIST_IDX_TIME = 3

###############################################################################

class CompilationBuild:
    RELEASE = 'Full Release'
    DEBUG = 'Full Debug'
    DISABLE_INLINE = 'Disable Inline Expansions'

###############################################################################
      
class CompilationType:      
    MAKE = 'M'
    BUILD = 'B'

###############################################################################