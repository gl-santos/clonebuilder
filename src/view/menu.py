# -*- coding: UTF-8 -*-

"""
@author rpereira
Sep 9, 2011

Modulo dos menus da aplicação
"""    

import wx
from wx.lib.wordwrap import wordwrap

class MainMenuBar(object):
    """
    @author rpereira
    
    Menu principal da aplicação
    """
    def __init__(self, frame):
        self.file = File(frame)
        self.edit = Edit(frame)
        self.help = Help(frame)
        
        self.menu_bar = wx.MenuBar()
        self.menu_bar.Append(self.file.menu, "File")
        self.menu_bar.Append(self.edit.menu, "Edit")
        self.menu_bar.Append(self.help.menu, "Help")
#        self.Append(HelpMenu(), "Help")
        
###############################################################################

class File(object):
    """
    @author rpereira
    
    Opção "File" do menu
    """
    def __init__(self, frame):
        self.menu = wx.Menu()
        self.open_seed_list = self.menu.Append(wx.ID_ANY, "Open Seed List...", 
                                  "Open Seed List")
        self.change_workspace = self.menu.Append(wx.ID_ANY, "Change Workspace...", 
                                  "Change Workspace")
        
        self.exit = self.menu.Append(wx.ID_ANY, "&Exit\tAlt+F4", "Exit Program")
    
###############################################################################

class Edit(object):
    """
    @author rpereira
    
    Opção "Edit" do menu
    """
    def __init__(self, frame):
        self.menu = wx.Menu()
        self.select_all = self.menu.Append(wx.ID_ANY, "Select All", "")
        self.build_all = self.menu.Append(wx.ID_ANY, "Build All", "")
        self.make_all = self.menu.Append(wx.ID_ANY, "Make All", "")
        
    
###############################################################################

class Help(object):
    """
    @author rpereira
    
    Opção "Help" do menu
    """
    def __init__(self, frame):
        self.menu = wx.Menu()
        self.about = self.menu.Append(wx.ID_ANY, "About", "")   
             
###############################################################################

class ContextListPkg(object):
    """
    @author rpereira
    
    Caixa de opções de contexto do click na lista de pacotes de compilação
    """
    def __init__(self):
        self.menu = wx.Menu()

        self.options = {}

        self.options['make'] = self.menu.Append(wx.ID_ANY, "Make", "")
        self.options['makeall'] = self.menu.Append(wx.ID_ANY, "Make All From Here", "")
        self.options['build'] = self.menu.Append(wx.ID_ANY, "Build", "")
        self.options['buildall'] = self.menu.Append(wx.ID_ANY, "Build All From Here", "")
        self.options['check'] = self.menu.Append(wx.ID_ANY, "Check", "")
        self.options['uncheck'] = self.menu.Append(wx.ID_ANY, "Uncheck", "")
        self.options['selectall'] = self.menu.Append(wx.ID_ANY, "Select All", "")
        self.options['fulldebug'] = self.menu.Append(wx.ID_ANY, "Full Debug", "")
        self.options['fullrelease'] = self.menu.Append(wx.ID_ANY, "Full Release", "")
        self.options['disableinline'] = self.menu.Append(wx.ID_ANY, "Disable Inline Expansions", "")
        

###############################################################################        

class ContextListSeed(object):
    """
    @author rpereira
    
    Caixa de opções de contexto do click na lista de pacotes sementes
    """
    def __init__(self):
        self.menu = wx.Menu()

        self.options = {}
        self.options['add'] = self.menu.Append(wx.ID_ANY, "Add", "")
        self.options['remove'] = self.menu.Append(wx.ID_ANY, "Remove", "")
        self.options['selectall'] = self.menu.Append(wx.ID_ANY, "Select All", "")
        self.options['buildall'] = self.menu.Append(wx.ID_ANY, "Build All", "")
        self.options['makeall'] = self.menu.Append(wx.ID_ANY, "Make All", "")
        
        
###############################################################################

class CloneAbout(object):
    def __init__(self, main_frame):
        info = wx.AboutDialogInfo()
#        info.Icon = wx.Icon("../resources/clone.ico", wx.BITMAP_TYPE_ICO)
        info.Name = "Clone"
        info.Version = "2.0.6"
        info.Copyright = "2012 - Axxiom Solucoes Tecnologicas SA"
        info.License = "GNU General Public License"
        info.Description = wordwrap(
            "The Clone utility was developed using the programming language "
            "Python and wxPython GUI library.\n\n Clone's initial proposal was "
            "to work as an utility to compile Borland's C++Builder programs, "
            "but the architecture has been generalized to allow some "
            "development team to \"plug\" the Clone in any compiler, allowing "
            "parallelization capability and all other features of the Clone.",
            450, wx.ClientDC(main_frame))
        info.WebSite = ("192.168.46.31:8181/wiki/Wiki.jsp?page=CloneBuilder",
                        "Clone's Website")
        info.Developers = ["Cleber Gomes", 
                           "Gustavo Santos",
                           "Rafael Campos",
                           "Rodrigo Muzzi"]
        
        wx.AboutBox(info)
