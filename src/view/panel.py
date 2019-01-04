# -*- coding: UTF-8 -*-

"""
@author rpereira
Aug 30, 2011

Modulo dos panels da aplicação
""" 

import wx
import grid

class ListSeed(wx.Panel):
    """
    @author rpereira
    
    Panel da lista de seed de pacotes
    """
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, style = (wx.CLIP_CHILDREN | wx.TAB_TRAVERSAL | wx.FULL_REPAINT_ON_RESIZE))
        
        self.list_ctrl = wx.ListCtrl(self, wx.NewId(), (0,0), (0,0), wx.LC_REPORT)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.list_ctrl, 5, wx.EXPAND, 5)
        
        self.SetSizer(sizer)
#        self.SetSize(size=(0,0))

        self.__buildColumn()
        
    def __buildColumn(self):
        """
        Cria as colunas existentes
        """
        info = wx.ListItem()
        info.m_mask = wx.LIST_MASK_TEXT | wx.LIST_MASK_FORMAT
        info.m_format = 0
        info.m_text = "Seed Package"
        self.list_ctrl.InsertColumnInfo(0, info)
        self.list_ctrl.SetColumnWidth(0, 150)

#        info.m_text = "Path"
#        self.list_ctrl.InsertColumnInfo(1, info)
#        self.list_ctrl.SetColumnWidth(1, 230)

    def from_list(self, list_pkg):
        """
        Carrega a lista gráfica a partir de uma lista de pacotes
        @param list_pkg lista de pacotes
        """
        i = 0
        for pkg in list_pkg:
            self.list_ctrl.InsertStringItem(i, pkg)
            i += 1
        
        
        
###############################################################################

import wx.lib.mixins.listctrl as listmix

class CheckboxListCtrl(wx.ListCtrl, listmix.CheckListCtrlMixin):
    """
    @author rpereira
    
    Checkbox modificado para ser colocado dentro da coluna de uma wx.ListCtrl
    """
    def __init__(self, *args, **kwargs):
        wx.ListCtrl.__init__(self, *args, **kwargs)
        listmix.CheckListCtrlMixin.__init__(self)

#    def OnCheckItem(self, index, flag):
#        print(index, flag)

class ListPackages(wx.Panel):
    """
    @author rpereira
    
    Panel da lista de pacotes
    """
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, style = (wx.CLIP_CHILDREN | wx.TAB_TRAVERSAL | wx.FULL_REPAINT_ON_RESIZE))
        
        self.list_ctrl = CheckboxListCtrl(self, wx.NewId(), (0,0), (0,0), wx.LC_REPORT)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.list_ctrl, 5, wx.EXPAND, 5)
        
        self.SetSizer(sizer)
#        self.SetSize(size=(0,0))

        self.__buildColumn()
        
    def __buildColumn(self):
        """
        Cria as colunas existentes
        """
        info = wx.ListItem()
        info.m_mask = wx.LIST_MASK_TEXT | wx.LIST_MASK_FORMAT
        info.m_format = 0
        info.m_text = "Package"
#        info.m_text = _("Package")
        self.list_ctrl.InsertColumnInfo(0, info)
        self.list_ctrl.SetColumnWidth(0, 150)

        info.m_text = "Path"
        self.list_ctrl.InsertColumnInfo(1, info)
        self.list_ctrl.SetColumnWidth(1, 300)

        info.m_text = "Build Option"
        self.list_ctrl.InsertColumnInfo(2, info)
        self.list_ctrl.SetColumnWidth(2, 100)
        
        info.m_text = "Time Elapsed"
        self.list_ctrl.InsertColumnInfo(3, info)
        self.list_ctrl.SetColumnWidth(3, 100)
        
    def from_list(self, list_pkg):
        """
        Carrega a lista gráfica a partir de uma lista de pacotes
        @param list_pkg lista de pacotes
        """
        i = 0
        for pkg in list_pkg:
#            pkg = self.pkg_list.dict_name.get(pkg)
            idx = self.list_ctrl.InsertStringItem(i, pkg[0])
            if pkg[3]:
                self.list_ctrl.CheckItem(idx)
            self.list_ctrl.SetStringItem(idx, 1, pkg[1])
            
            self.list_ctrl.SetStringItem(idx, 2, pkg[2])
            i += 1
        

###############################################################################
        
class ListConsole(wx.Panel):
    """
    @author rpereira
    
    Panel do console de compilacao
    """
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, style = (wx.CLIP_CHILDREN | wx.TAB_TRAVERSAL | wx.FULL_REPAINT_ON_RESIZE))

        self.list_ctrl = wx.ListCtrl(self, wx.NewId(), (0,0), (0,0), wx.LC_REPORT | wx.LC_NO_HEADER)
        self.list_ctrl.InsertColumn(0, "Mensagens", wx.LIST_FORMAT_LEFT, wx.LIST_AUTOSIZE)
        
#        self.list_ctrl.SetColumnWidth(0, wx.LIST_AUTOSIZE)
#        self.list_ctrl.SetColumnWidth(1, wx.LIST_AUTOSIZE)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.list_ctrl, 5, wx.EXPAND, 5)
        
        self.SetSizer(sizer)
#        self.SetSize((0, 222))
        
###############################################################################
        
class ToolBar(wx.Panel):
    """
    @author rpereira
    
    Toolbar com botoes de opcoes
    """
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, style = (wx.CLIP_CHILDREN | wx.TAB_TRAVERSAL | wx.FULL_REPAINT_ON_RESIZE))

        self.grid = grid.ToolBar(self) 
        
        self.SetSizerAndFit(self.grid)
#        self.SetSize(size=(100,500))
        
###############################################################################

