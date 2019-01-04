# -*- coding: UTF-8 -*-
"""
Created on ???

@author: Cleber Camilo
"""

import os
from mpbuild import MultiProcBuilder

class CompilerBuilder :
    def __init__(self, path, file, multiproc):
        self.path = path
        self.file = file
        self.openFile = None
        self.multiproc = multiproc
        self.builder = None
    
    def compile(self, paramExtr = ""):        
        os.chdir(self.path)
        if self.multiproc:
            self.builder = MultiProcBuilder(self.file, paramExtr)
            self.builder.start()            
        else:
            cmd = "make -f " + self.file + " " + paramExtr
            self.openFile = os.popen(cmd,'r')

    def readMsg(self):
        if self.multiproc:
            return self.builder.readMsg()
        elif not self.openFile.closed: 
            return self.openFile.readline()
        else: return ""

    def close(self):
        if self.multiproc:
            self.builder.group.stop_all()
            return self.builder.getResult()
        while True:
            try:
                return self.openFile.close()
            except:
                pass
