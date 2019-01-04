# -*- coding: UTF-8 -*-

"""
@author rpereira
Aug 29, 2011

Módulo de Grid, contendo a barra de ferramentas dos botões
"""

import wx

class ToolBar(wx.GridBagSizer):
    """
    @author rpereira

    Classe da Barra de Ferramentas
    """
    def __init__(self, parent):
        wx.GridBagSizer.__init__(self, 5, 15)

        self.parent = parent
        self.main_frame = self.parent.Parent
        self.rowBotoes = 0

        self.AddGrowableRow(13)
        self.AddGrowableCol(0)

        self.buttons = dict()
        self.__add_buttons()


#TODO: refatorar este metodo, eliminar botoes inuteis, etc
    def __add_buttons(self):
        """
        Cria todos os botoes da barra de ferraentas
        """
        colBotoes = 0
        
        #todo trocar os botoes pelo dict
        """
        self.buttons["workspace"] = wx.Button(self.parent, wx.NewId(), "Change Workspace")
        self.Add(self.buttons["workspace"], (self.rowBotoes,colBotoes), (1,1), wx.EXPAND)
        self.rowBotoes+=1
        
        self.buttons["open_list"] = wx.Button(self.parent, wx.NewId(), "Open Seed")
        self.Add(self.buttons["open_list"], (self.rowBotoes,colBotoes), (1,1), wx.EXPAND)
        self.rowBotoes+=1
        """
        self.panel_version = wx.Panel(self.parent, -1)
        self.Add(self.panel_version, (self.rowBotoes, colBotoes), (1,1), wx.EXPAND)
        self.rowBotoes+=1
        self.static_box_version = wx.StaticBox(self.panel_version, -1, "Version", 
                                               size=(165,42))
        self.buttons["v_major"] = wx.SpinCtrl(self.panel_version, wx.NewId(), 
                                              pos=(2,15), size = (40, -1), min = 1,
                                              max = 99, initial = 1)
        self.buttons["v_minor"] = wx.SpinCtrl(self.panel_version, wx.NewId(), 
                                              pos=(42,15), size = (40, -1), min = 0,
                                              max = 99, initial = 0)
        self.buttons["v_release"] = wx.SpinCtrl(self.panel_version, wx.NewId(), 
                                                pos=(82,15), size = (40, -1), min = 0,
                                                max = 99, initial = 1)
        self.buttons["v_build"] = wx.SpinCtrl(self.panel_version, wx.NewId(), 
                                              pos=(122,15), size = (40, -1), min = 1,
                                              max = 99, initial = 1)

        self.panel_thread = wx.Panel(self.parent, -1)
        self.Add(self.panel_thread, (self.rowBotoes, colBotoes), (1,1), wx.EXPAND)
        self.rowBotoes+=1        
        self.static_box_thread = wx.StaticBox(self.panel_thread, -1, "", size=(165,40))
        self.labelThreads = wx.StaticText(self.panel_thread, wx.NewId(), "Threads:", pos=(5,16))
        self.buttons["num_threads"] = wx.SpinCtrl(self.panel_thread,
                                                  wx.NewId(),
                                                  pos=(52,13),
                                                  size = (42, -1),
                                                  min = 0,
                                                  max = 99,
                                                  initial = 1)

#        self.Bind(wx.EVT_SPINCTRL, self.__OnChangeNumThreads, self.buttonThreads)
#        self.buttonThreads.Disable()

        #todo trocar os botoes pelo dict

        """
        self.buttons["build_all"] = wx.Button(self.parent, wx.NewId(), "Build All")

        self.Add(self.buttons["build_all"], (self.rowBotoes,colBotoes), (1,1), wx.EXPAND)
        self.rowBotoes+=1
        """       
        
        self.panel_time = wx.Panel(self.parent, -1)
        self.Add(self.panel_time, (self.rowBotoes, colBotoes), (1,1), wx.EXPAND)        
        self.static_box_thread = wx.StaticBox(self.panel_time, -1, "", size=(165,40))
        self.label_total = wx.StaticText(self.panel_time, wx.NewId(), "Total Time:", pos=(5,16))
        
        

        self.total_time = wx.TextCtrl(self.panel_time, wx.NewId(),pos=(60,13),
                                      size = (100, -1),)
        self.total_time.SetEditable(False)

        self.rowBotoes+=1
        self.progress_dialog = wx.Gauge(self.parent, -1, 50, size=(50, 10))
        self.Add(self.progress_dialog, (self.rowBotoes, colBotoes), (1,1), wx.EXPAND)
        
        self.rowBotoes+=1
        self.buttonCanc = wx.Button(self.parent, wx.NewId(), "Cancel")
        self.Add(self.buttonCanc, (self.rowBotoes, colBotoes), (1,1), wx.EXPAND)
 

    def set_progress_value(self, total, part):
        self.progress_dialog.Show()
        value = part*50/total
        self.progress_dialog.SetValue(value)
        
    def clear_progress_value(self):
        self.progress_dialog.SetValue(0)
        
    def hide_progress_bar(self):
        self.progress_dialog.Hide()

    def set_total_time(self,total):
        self.hide_progress_bar()
        self.total_time.Clear()
        self.total_time.AppendText(total)  