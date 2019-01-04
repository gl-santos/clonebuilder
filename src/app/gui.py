# -*- coding: UTF-8 -*-

"""
@author rpereira
Aug 19, 2011

Modulo da aplicação
"""

import wx
import traceback
from controller.graphical import GuiController
import controller.list as ctrl
from view.main_frame import MainFrame
import app.cache as ctrl_serial

APP_NAME = "CloneBuilder"

class GuiApp(object):
    """
    @author rpereira
    
    Borg Design Pattern
    Aplicação com interface gráfica
    """
    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state
        
        if not self.__shared_state:
            """
            Borg Design Pattern: inicia o estado apenas uma vez
            """
            self.__wx_app = wx.App(False)
            self.main_frame = MainFrame(self)
            self.main_frame.wx_app = self.__wx_app
            
            self.comp_pkgs = ctrl.Packages()
            self.__guictrl = GuiController(self.main_frame, self.comp_pkgs)
            
            ctrl_serial.load(self.__guictrl)
            
            
    def run(self):
        """
        inicia os componentes dos borgs de controle
        """
        try:
            self.comp_pkgs.set_list_seed(self.__guictrl.list_seed)
            self.comp_pkgs.set_list_panel(self.__guictrl.list_panel)
            self.comp_pkgs.set_console_panel(self.__guictrl.console_panel)
            self.comp_pkgs.set_tool_panel(self.__guictrl.tool_panel)
            
            self.__guictrl.render()
            self.__wx_app.MainLoop()
        except Exception, e:
            print traceback.format_exc()
            raise e;
        
