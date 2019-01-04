# -*- coding: UTF-8 -*-

"""
@author rpereira
Aug 19, 2011

Frame principal da aplicação
"""    

import wx
import wx.lib.agw.aui as aui

#import panel
#import view.menu as menu
from view.menu import MainMenuBar


from view.clone_icon import clone_jango_32_icon


class MainFrame(wx.Frame):
    """
    @author rpereira
    
    Frame principal da aplicacao, controla o AUI Manager
    (componente de docking)
    """
    def __init__(self, controller):
        self.controller = controller
        wx.Frame.__init__(self, None, wx.ID_ANY, title="Clone", size=(1024,768))

        self.SetIcon(clone_jango_32_icon())
        
        self.menu = MainMenuBar(self)
        self.SetMenuBar(self.menu.menu_bar)
        
###############################################################################

class CloneAui(aui.AuiManager):
    def setup(self, fctrl):
        info = aui.AuiPaneInfo().CloseButton(visible=False).MaximizeButton().MinimizeButton()
        info.Left().Name("Seeds").MinSize(160, 0)
        self.AddPane(fctrl.list_seed, info)
        
        info = aui.AuiPaneInfo().CloseButton(visible=False).MaximizeButton().MinimizeButton()
        info.Center().Name("Packages")
        self.AddPane(fctrl.list_panel, info)
        
        info = aui.AuiPaneInfo().CloseButton(visible=False).MaximizeButton().MinimizeButton()
        info.Bottom().Name("Console").BestSize(0,250)
        self.AddPane(fctrl.console_panel, info)
        
        info = aui.AuiPaneInfo().CloseButton(visible=False).MinimizeButton()
        info.Right().Name("Toolbar")
        self.AddPane(fctrl.tool_panel, info)
        
        self.Update()
    
    
