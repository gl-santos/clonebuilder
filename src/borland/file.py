# -*- coding: UTF-8 -*-

"""
@author rpereira
Apr 18, 2012

Colocar aqui todo tratamento especifico de arquivo da borland:
bpk
bpg
bpr
res
rc
"""

import re
import os
from controller.front import FrontController

GROUP_EXTS = ["bpg"]
PACKAGE_EXTS = ["bpk"]
EXE_EXTS = ["bpr"]

"""Wildcards para abrir arquivos das extensoes em FileDialogs"""
__pkgsep = "; *."
PKG_OPEN_WILDCARD = (
    "Borland Package " +
    "(*." + 
            __pkgsep.join(PACKAGE_EXTS) + 
            __pkgsep + __pkgsep.join(EXE_EXTS) + 
            __pkgsep + __pkgsep.join(GROUP_EXTS) + ")|" +
            
    "*." +
        __pkgsep.join(PACKAGE_EXTS) +
        __pkgsep + __pkgsep.join(EXE_EXTS) +
        __pkgsep + __pkgsep.join(GROUP_EXTS)) 

import fnmatch

#TODO: criar classe File, dai criar com composicao as classes BPK BPR BPG RES etc
class ProjectGroup(object):
    def __init__(self, file_path):
        self.file_path = file_path
        self.__pkg_exts = PACKAGE_EXTS + EXE_EXTS
        
    def find_list(self):
        if os.path.exists(self.file_path):
            file = open(self.file_path, 'r')
        else:
            file = self.__find_file()
        
        buff = file.readlines()
        exes = []
        flag = False
        
        for line in buff:
            if flag:
                if re.match("^#---", line, 1):
                    break
                if re.match("^PROJECTS", line, 1):
                    line = line[11:]
                    
                exes = exes + line.split()
                
            else:
                if re.match("^PROJECTS", line, 1):
                    line = line[11:]
                    flag = True
                    exes = exes + line.split()
                
        exes = filter(lambda a: a != "\\", exes)
        
        return exes
    
    def __find_file(self):
        filename = self.file_path
        matches = []
        for path in FrontController().workspace.data['include_path']:
            for root, dirnames, filenames in os.walk(path):
                for ext in self.__pkg_exts:
                    for filename in fnmatch.filter(filenames, 
                                                   filename + "." + ext):
                        matches.append((os.path.splitext(filename)[0], 
                                           filename, root+os.sep))                            
                        break
        return matches
        
        
    