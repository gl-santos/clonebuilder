# -*- coding: UTF-8 -*-

"""
@author rpereira
May 3, 2012


"""
import os
from borland.file import PKG_OPEN_WILDCARD
from app.consts import CompilationBuild

import wx

from front import Controller

import controller.list as ctrl_list

from view.panel import ListSeed
from view.panel import ListPackages
from view.panel import ListConsole
from view.panel import ToolBar
from view.main_frame import CloneAui
from view.menu import ContextListPkg 
from view.menu import ContextListSeed 
from view.menu import CloneAbout 

import app.cache as ctrl_serial
from front import FrontController

import thread
from borland.file import GROUP_EXTS

class GuiController(FrontController):
    """
    @author rpereira
    
    Front Controller da aplicação
    """
    __shared_state = {}
    def __init__(self, main_frame = None, comp_pkgs = None):
        FrontController.__init__(self)
        
        if comp_pkgs:
            self.ctrl_build = BuildController(self, comp_pkgs)
            self.ctrl_seed = SeedController(self, comp_pkgs)
        
        if main_frame:
            self.main_frame = main_frame
            
            self.list_seed = ListSeed(self.main_frame)
            self.list_panel = ListPackages(self.main_frame)
            self.console_panel = ListConsole(self.main_frame)
            self.tool_panel = ToolBar(self.main_frame)
            
            self.aui_mgr = CloneAui(self.main_frame)
            self.aui_mgr.setup(self)
            
            self.menu_pkg = ContextListPkg()
            self.menu_seed = ContextListSeed()
            
            self.main_frame.Bind(wx.EVT_CLOSE, self.action_save_state)
            
            self.ctrl_pkg = PackageController(self)
            self.ctrl_menu = MenuController(self)
            
            self.__bind_toolbar()
            self.__bind_lists()
            self.__bind_menus()
            self.__bind_context_list()
            self.__bind_toolbar()
            
    def render(self):
        """
        Renderiza a janela principal da aplicação
        """
        
        if not self.workspace.is_valid():
            if not self.change_workspace(event = None):
                #TODO: melhorar o exit()
                exit()
                
        self.main_frame.wx_app.SetTopWindow(self.main_frame)
        self.main_frame.CenterOnScreen()
        self.main_frame.Show()
        
    def clear_gui(self):
        self.list_seed.list_ctrl.DeleteAllItems()
        self.list_panel.list_ctrl.DeleteAllItems()
        self.console_panel.list_ctrl.DeleteAllItems()
        
        FrontController().clear_cache()
        
    def action_save_state(self, event):
        """
        Salva as preferencias do programa
        """
        ctrl_serial.dump(self)
        event.EventObject.Destroy()
        
    def __bind_toolbar(self):
        #self.main_frame.Bind(wx.EVT_BUTTON, actions.change_workspace, self.tool_panel.grid.buttons['workspace'])
        #self.main_frame.Bind(wx.EVT_BUTTON, actions.file_to_pkglist, self.tool_panel.grid.buttons['open_list'])
        self.main_frame.Bind(wx.EVT_BUTTON, self.ctrl_build.cancel,
                             self.tool_panel.grid.buttonCanc)
        self.main_frame.Bind(wx.EVT_SPINCTRL, self.on_change_version,
                             self.tool_panel.grid.buttons['v_major'])
        self.main_frame.Bind(wx.EVT_SPINCTRL, self.on_change_version,
                             self.tool_panel.grid.buttons['v_minor'])
        self.main_frame.Bind(wx.EVT_SPINCTRL, self.on_change_version,
                             self.tool_panel.grid.buttons['v_release'])
        self.main_frame.Bind(wx.EVT_SPINCTRL, self.on_change_version,
                             self.tool_panel.grid.buttons['v_build'])
        self.main_frame.Bind(wx.EVT_SPINCTRL, self.on_change_num_threads,
                             self.tool_panel.grid.buttons['num_threads'])
        
    def load_defaults(self):
        list_version = self.get_version().split(".")
        self.tool_panel.grid.buttons['v_major'].SetValue(int(list_version[0]))
        self.tool_panel.grid.buttons['v_minor'].SetValue(int(list_version[1]))
        self.tool_panel.grid.buttons['v_release'].SetValue(int(list_version[2]))
        self.tool_panel.grid.buttons['v_build'].SetValue(int(list_version[3]))
        self.tool_panel.grid.buttons['num_threads'].SetValue(self.get_num_threads())
        
    def __bind_lists(self):
        #bind do ListPackages
        self.list_panel.list_ctrl.Bind(wx.EVT_RIGHT_DOWN, self.ctrl_menu.click_pos)
        self.list_panel.list_ctrl.Bind(wx.EVT_CONTEXT_MENU, self.ctrl_menu.menu_list_pkg)
        #bind do ListSeed
        self.list_seed.list_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.ctrl_seed.load_list)
        self.list_seed.list_ctrl.Bind(wx.EVT_RIGHT_DOWN, self.ctrl_menu.click_pos)
        self.list_seed.list_ctrl.Bind(wx.EVT_CONTEXT_MENU, self.ctrl_menu.menu_list_seed)

    def __bind_menus(self):
        self.main_frame.Bind(wx.EVT_MENU, self.ctrl_build.file_to_pkglist,
                             self.main_frame.menu.file.open_seed_list)
        self.main_frame.Bind(wx.EVT_MENU, self.change_workspace,
                             self.main_frame.menu.file.change_workspace)
        self.main_frame.Bind(wx.EVT_MENU, self.exit,
                             self.main_frame.menu.file.exit)
        self.main_frame.Bind(wx.EVT_MENU, self.ctrl_pkg.select_all,
                             self.main_frame.menu.edit.select_all)
        self.main_frame.Bind(wx.EVT_MENU, self.ctrl_build.build_all,
                             self.main_frame.menu.edit.build_all)
        self.main_frame.Bind(wx.EVT_MENU, self.ctrl_build.make_all,
                             self.main_frame.menu.edit.make_all)
        self.main_frame.Bind(wx.EVT_MENU, self.show_about,
                             self.main_frame.menu.help.about)
        
    def __bind_context_list(self):
        #bind das listas de contexto
        self.menu_pkg.menu.Bind(wx.EVT_MENU, self.ctrl_build.make,
                                self.menu_pkg.options['make'])
        self.menu_pkg.menu.Bind(wx.EVT_MENU, self.ctrl_build.make_from_here,
                                self.menu_pkg.options['makeall'])
        self.menu_pkg.menu.Bind(wx.EVT_MENU, self.ctrl_build.build,
                                self.menu_pkg.options['build'])
        self.menu_pkg.menu.Bind(wx.EVT_MENU, self.ctrl_build.build_from_here,
                                self.menu_pkg.options['buildall'])
        self.menu_pkg.menu.Bind(wx.EVT_MENU, self.ctrl_pkg.check_list_checkbox,
                                self.menu_pkg.options['check'])
        self.menu_pkg.menu.Bind(wx.EVT_MENU, self.ctrl_pkg.uncheck_list_checkbox,
                                self.menu_pkg.options['uncheck'])
        self.menu_pkg.menu.Bind(wx.EVT_MENU, self.ctrl_pkg.select_all,
                                self.menu_pkg.options['selectall'])
        self.menu_pkg.menu.Bind(wx.EVT_MENU, self.ctrl_pkg.full_debug,
                                self.menu_pkg.options['fulldebug'])
        self.menu_pkg.menu.Bind(wx.EVT_MENU, self.ctrl_pkg.full_release,
                                self.menu_pkg.options['fullrelease'])
        self.menu_pkg.menu.Bind(wx.EVT_MENU, self.ctrl_pkg.disable_inline_expansions,
                                self.menu_pkg.options['disableinline'])
                
        self.menu_seed.menu.Bind(wx.EVT_MENU, self.ctrl_build.file_to_pkglist,
                                 self.menu_seed.options['add'])
        self.menu_seed.menu.Bind(wx.EVT_MENU, self.ctrl_seed.list_seed_remove,
                                 self.menu_seed.options['remove'])
        self.menu_seed.menu.Bind(wx.EVT_MENU, self.ctrl_seed.select_all,
                                 self.menu_seed.options['selectall'])
        self.menu_seed.menu.Bind(wx.EVT_MENU, self.ctrl_build.build_all,
                                 self.menu_seed.options['buildall'])
        self.menu_seed.menu.Bind(wx.EVT_MENU, self.ctrl_build.make_all,
                                 self.menu_seed.options['makeall'])
        
    def exit(self, event):
        """
        Fechar a aplicação
        @param event evento que disparou a acao
        """
        self.main_frame.Close()
        
    def on_change_version(self, event):
        """
        Salva as alteracoes na interface da versao de compilacao
        """
        buttons = self.tool_panel.grid.buttons
        list = ([
            str(buttons["v_major"].GetValue()),
            str(buttons["v_minor"].GetValue()),
            str(buttons["v_release"].GetValue()),
            str(buttons["v_build"].GetValue())])

        self.set_version(".".join(list))

    def on_change_num_threads(self, event):
        """
        Salva as alteracoes na interface do numero de threads
        """
        num_threads = str(self.tool_panel.grid.
                          buttons["num_threads"].GetValue())
        self.set_num_threads(num_threads)
        
            
    def change_workspace(self, event):
        workspace = self.workspace
        
        dialog = wx.DirDialog(None, "Choose your workspace folder:",
                              workspace.data['path'])
    
        if dialog.ShowModal() == wx.ID_OK:
            workspace.change_workspace(dialog.GetPath())
            self.clear_gui()
                
        if workspace.is_valid():
            return True
        else:
            return False

    def show_about(self, event):
        """
        Exibe o about da aplicação
        """
        CloneAbout(self.main_frame)

###############################################################################

class ListController(Controller):
    def __init__(self):
        Controller.__init__(self)
        self.list_selected = []
    
    def select_all(self, event):
        """
        Seleciona todos os elementos da lista
        @param event evento que disparou a acao
        """
        if hasattr(event.EventObject, "InvokingWindow"):
            list_ctrl = event.EventObject.InvokingWindow
        else:
            list_ctrl = GuiController().list_panel.list_ctrl

        is_list_ctrl = (hasattr(list_ctrl, "GetItemCount") and
                        hasattr(list_ctrl, "Select"))

        if is_list_ctrl:
            for idx in range(list_ctrl.GetItemCount()):
                list_ctrl.Select(idx)
        
    
###############################################################################

class PackageController(ListController):
    def __init__(self, guictrl):
        ListController.__init__(self)
        self.__guictrl = guictrl
        
    def full_release (self,event):
        """
        Marca os pacotes selecionados para full release
        """
        list_ctrl = GuiController().list_panel.list_ctrl
        self.list_selected = ctrl_list.get_selected_items(list_ctrl)

        for item in self.list_selected:
            pkg_name = os.path.splitext(item.m_text)[0]
            pkg = self.__guictrl.cached['name'].get(pkg_name.lower())
            pkg.build_opt = CompilationBuild.RELEASE
            list_ctrl.SetStringItem(item.Id, 2, pkg.build_opt)

    def full_debug (self,event):
        """
        Marca os pacotes selecionados para full debug
        """
        list_ctrl = GuiController().list_panel.list_ctrl
        self.list_selected = ctrl_list.get_selected_items(list_ctrl)

        for item in self.list_selected:
            pkg_name = os.path.splitext(item.m_text)[0]
            pkg = self.__guictrl.cached['name'].get(pkg_name.lower())
            pkg.build_opt = CompilationBuild.DEBUG
            list_ctrl.SetStringItem(item.Id, 2, pkg.build_opt)

    def disable_inline_expansions (self,event):
        """
        Marca os pacotes selecionados para full debug
        """
        list_ctrl = GuiController().list_panel.list_ctrl
        self.list_selected = ctrl_list.get_selected_items(list_ctrl)
            
        for item in self.list_selected:
            pkg_name = os.path.splitext(item.m_text)[0]
            pkg = self.__guictrl.cached['name'].get(pkg_name.lower())
            pkg.build_opt = CompilationBuild.DISABLE_INLINE
            list_ctrl.SetStringItem(item.Id, 2, pkg.build_opt)
            
    def check_list_checkbox(self, event):
        """
        Marca todos os itens selecionados da lista de compilcao
        @param event evento que disparou a acao
        """
        list_ctrl = GuiController().list_panel.list_ctrl
        self.list_selected = ctrl_list.get_selected_items(list_ctrl)

        for item in self.list_selected:
            list_ctrl.CheckItem(item.Id, check=True)

    def uncheck_list_checkbox(self, event):
        """
        Desmarca todos os itens selecionados da lista de compilcao
        @param event evento que disparou a acao
        """
        list_ctrl = GuiController().list_panel.list_ctrl
        self.list_selected = ctrl_list.get_selected_items(list_ctrl)

        for item in self.list_selected:
            list_ctrl.CheckItem(item.Id, check=False)
            
###############################################################################

class SeedController(ListController):
    def __init__(self, guictrl, comp_pkgs):
        ListController.__init__(self)
        self.__guictrl = guictrl
        self.__comp_pkgs = comp_pkgs
        
    def load_list(self, event):
        """
        Carrega a lista de compilacao a partir da lista de sementes
        (evento de selected)
        @param event evento que disparou a acao
        """
        list_item = event.Item
        extension = os.path.splitext(list_item.m_text)[1][1:]
        
        if extension in GROUP_EXTS:
            self.__comp_pkgs.load_group_list(list_item.m_text)
        else:
            self.__comp_pkgs.load_package_list(list_item.m_text)
            
    def list_seed_remove(self, event):
        """
        Remove um pacote semente
        @param
        """
        list_ctrl = event.EventObject.InvokingWindow
        select_pkgs = ctrl_list.get_selected_items(list_ctrl)

        for selected in select_pkgs:
            list_ctrl.DeleteItem(selected.Id)

        GuiController().list_panel.list_ctrl.DeleteAllItems()
        
###############################################################################
    
class MenuController(Controller):
    def __init__(self, guictrl):
        Controller.__init__(self)
        self.__last_click_pos = (0,0)
        self.__guictrl = guictrl
    
    def menu_list_seed(self, event):
        """

        @param event evento que disparou a acao
        """
        self.list_selected = ctrl_list.get_selected_items(GuiController().
                                                          list_panel.list_ctrl)
        event.EventObject.PopupMenu(self.__guictrl.menu_seed.menu,
                                    self.__last_click_pos)
        
    def menu_list_pkg(self, event):
        """

        @param event evento que disparou a acao
        """
        self.list_selected = ctrl_list.get_selected_items(GuiController().
                                                          list_panel.list_ctrl)
        event.EventObject.PopupMenu(self.__guictrl.menu_pkg.menu,
                                    self.__last_click_pos)
        
                
    def click_pos(self, event):
        """
        Seta a posição do evento
        @param event evento que disparou a acao
        """
        self.__last_click_pos = (event.GetX(), event.GetY())
    
###############################################################################

class BuildController(Controller):
    """
    @author rpereira

    Classe de ações da aplicação, genérica par utilização por diferentes
    chamadas
    """

    def __init__(self, guictrl, comp_pkgs):
        self.comp_pkg = comp_pkgs
        self.__guictrl = guictrl

    def get_gui_grid(self):
        return self.__guictrl.tool_panel.grid

    def build(self, event):
        """
        Acao de build dos pacotes selecionados
        @param event evento que disparou a acao
        """
        list_ctrl = event.EventObject.InvokingWindow
        list_selected = ctrl_list.get_selected_items(list_ctrl)
        is_make = False
        params = (list_selected, self.get_gui_grid(), is_make)
        thread.start_new_thread(self.comp_pkg.make, params)
        
    def build_all(self, event):
        """
        Acao de build a partir de um pacote de referencia
        @param event evento que disparou a acao
        """
        list_ctrl = event.EventObject.InvokingWindow
        l = ctrl_list.get_selected_from_here(list_ctrl, list_ctrl.GetItem(0,0))
        is_make = False
        params = (l, self.get_gui_grid(), is_make)
        thread.start_new_thread(self.comp_pkg.make, params)
        
    def build_from_here(self, event):
        """
        Acao de build a partir de um pacote de referencia
        @param event evento que disparou a acao
        """
        list_ctrl = event.EventObject.InvokingWindow
        list_selected = ctrl_list.get_selected_items(list_ctrl)
        l = ctrl_list.get_selected_from_here(list_ctrl, list_selected[0])
        is_make = False
        params = (l, self.get_gui_grid(), is_make)
        thread.start_new_thread(self.comp_pkg.make, params)

    def make(self, event):
        """
        Acao de make dos pacotes selecionados
        @param event evento que disparou a acao
        """
        list_ctrl = event.EventObject.InvokingWindow
        list_selected = ctrl_list.get_selected_items(list_ctrl)
        is_make = True
        params = (list_selected, self.get_gui_grid(), is_make)
        thread.start_new_thread(self.comp_pkg.make, params)

    def make_from_here(self, event):
        """
        Acao de make a partir de um pacote de referencia
        @param event evento que disparou a acao
        """
        list_ctrl = event.EventObject.InvokingWindow
        list_selected = ctrl_list.get_selected_items(list_ctrl)
        l = ctrl_list.get_selected_from_here(list_ctrl, list_selected[0])
        is_make = True
        params = (l, self.get_gui_grid(), is_make)
        thread.start_new_thread(self.comp_pkg.make, params)

    def make_all(self, event):
        """
        Acao de build a partir de um pacote de referencia
        @param event evento que disparou a acao
        """
        list_ctrl = event.EventObject.InvokingWindow
        l = ctrl_list.get_selected_from_here(list_ctrl, list_ctrl.GetItem(0,0))
        is_make = True
        params = (l, self.get_gui_grid(), is_make)
        thread.start_new_thread(self.comp_pkg.make, params)
        
    def cancel(self, event):
        """
        Cancela acao de build ou make
        @param
        """
        job = self.comp_pkg.comp_build.job

        if hasattr(job, "close"):
            job.close()
            self.comp_pkg.comp_build.cancel = True
            
    def file_to_pkglist(self, event):
        """
        Chama o dialog de selecionar arquivo um arquivo e gera a
        lista de compilacao
        @param event evento que disparou a acao
        """
        #TODO: tirar textos do fonte self.__guictrl.tool_panel.grid.buttonsassar pra arquivo de internacionalização
        dialog_title = "Select a Package File"
        default_file = ""

        dialog = wx.FileDialog(self.__guictrl.main_frame, dialog_title,
                               self.__guictrl.workspace.data['path'],
                               default_file,
                               PKG_OPEN_WILDCARD,
                               style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR)

        dialog.CenterOnParent()

        if dialog.ShowModal() == wx.ID_OK:
            path = dialog.GetPaths()[0]
            length = len(self.__guictrl.workspace.data['path'])
            subpath = path[0:length]
            
            if subpath != self.__guictrl.workspace.data['path']:
                wx.MessageBox('This package is not in the workspace',
                               'Info', 
                              wx.OK | wx.ICON_INFORMATION)
            else:
                if os.path.splitext(path)[1][1:] in GROUP_EXTS:
                    self.comp_pkg.load_group_list(path)
                else:
                    package = os.path.basename(path)
                    self.comp_pkg.load_package_list(package)

        dialog.Destroy()
