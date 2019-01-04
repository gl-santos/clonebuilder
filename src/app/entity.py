# -*- coding: UTF-8 -*-

"""
@author rpereira
Apr 17, 2012


"""

from consts import CompilationBuild

class Package(object):
    """
    @author rpereira
    
    Entitidade do pacote
    """
    def __init__(self, name = "", filename = "", path = "", 
            build=CompilationBuild.DEBUG):
        self.checked = True
        self.name = name
        self.filename = filename
        self.path = path
        self.build_opt = build