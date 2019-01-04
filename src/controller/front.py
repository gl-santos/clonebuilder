# -*- coding: UTF-8 -*-

"""
@author rpereira
Apr 16, 2012

Controller principal
"""

from app.cache import Workspace

import multiprocessing

class Controller(object):
    """
    @author rpereira
    
    Controller genérico
    """
    def __init__(self):
        pass

class FrontController(Controller):
    """
    @author rpereira
    
    FrontController pattern
    """
    __shared_state = {}
    def __init__(self):
        Controller.__init__(self)
        self.__dict__ = self.__shared_state
        if not self.__shared_state:
            self.__version = "1.1.1.1"
            self.__num_threads = multiprocessing.cpu_count()
            
            self.workspace = Workspace()
            self.clear_cache()
            
    def clear_cache(self):
        """
        Limpa o cache da aplicação 
        """
        self.cached = {}
        self.cached['seed'] = dict()
        self.cached['name'] = dict()
        self.__shared_state = self.__dict__
            
    def get_num_threads(self):
        return self.__num_threads
    
    def set_num_threads(self, num_threads):
        self.__num_threads = int(num_threads)
    
    def get_version(self):
        return self.__version
    
    def set_version(self, version):
        self.__version = version
        
