# -*- coding: UTF-8 -*-

"""
@author rpereira
Sep 1, 2011

Módulo de tratamento das listas de pacotes
"""
#TODO: refatorar este modulo para seguir a linha dos ultimos Controllers

import wx
import compiler.package as cpkg
import datetime
import compiler.build as build
import app.consts as c
import os
from front import FrontController
from borland.file import ProjectGroup
import xml.dom.minidom
import legacy.comp_option as legopt
from string import split
from app.consts import CompilationBuild

class Packages(object):
    """
    @author rpereira
    
    Classe de controle da lista de pacotes
    Borg design pattern
    """
    __shared_state = {}
    def __init__(self):
        self.__dict__ = self.__shared_state
        
        self.__list_seed = None
        self.__list_panel = None
        self.__console_panel = None
        
        self.comp_build = build.Ctrl()
        self.pkg_list = cpkg.PackageList(FrontController())
        
    def set_console_panel(self, console_panel):
        self.__console_panel = console_panel
        self.comp_build.set_console_panel(console_panel)
        
    def set_list_panel(self, list_panel):
        self.__list_panel = list_panel

    def set_list_seed(self, list_seed):
        self.__list_seed = list_seed
                
    def set_tool_panel(self, tool_panel):
        self.__tool_panel = tool_panel   
        
    def load_group_list(self, group_path):
        list_panel = self.__list_panel.list_ctrl
        list_seed = self.__list_seed.list_ctrl
        
        grp = ProjectGroup(group_path)
        groupname = os.path.basename(group_path)
        
        found_at = list_seed.FindItem(-1, groupname)
        if found_at == -1:
            index = list_seed.GetItemCount()+1
            list_seed.InsertStringItem(index, groupname)
        
        list_pkg = self.pkg_list.generate_group_list(grp)
        list_panel.DeleteAllItems()
        try:
            i = 0
            for pkg in list_pkg:
                pkg = FrontController().cached['name'].get(pkg)
                idx = list_panel.InsertStringItem(i, pkg.filename)
                list_panel.CheckItem(idx)
                list_panel.SetStringItem(idx, c.LIST_IDX_PATH, pkg.path)
                list_panel.SetStringItem(idx, c.LIST_IDX_OPTION, pkg.build_opt)
                i += 1
        except Exception, e:
            raise e
        
    def load_package_list(self, seed):
        """
        Carrega a lista de pacoes de acordo com a dependencia e a semente
        @param seed pacote semente
        """
        list_pkg = self.pkg_list.generate_package_list(seed)
        
        list_seed = self.__list_seed.list_ctrl
        list_panel = self.__list_panel.list_ctrl
        
        #load seed list
        found_at = list_seed.FindItem(-1, seed)
        if found_at == -1:
            index = list_seed.GetItemCount()+1
            list_seed.InsertStringItem(index, seed)
        
        #load panel list 
        list_panel.DeleteAllItems()
        try:
            i = 0
            for pkg in list_pkg:
                pkg = FrontController().cached['name'].get(pkg)
                idx = list_panel.InsertStringItem(i, pkg.filename)
                #TODO: externalizar a extensao .mak para parametros de config
#                makepath = pkg.path + pkg.name + ".mak"
                list_panel.CheckItem(idx)
                list_panel.SetStringItem(idx, c.LIST_IDX_PATH, pkg.path)
                list_panel.SetStringItem(idx, c.LIST_IDX_OPTION, pkg.build_opt)
                i += 1
        except Exception, e:
            raise e
    

#TODO: refatorar pra ser uma funcao do modulo compilar.build
    def make(self, list_selected, grid, is_make = True):
        """
        Começa o processo de make, gerando os arquibos .mak
        @param list_selected lista de pacotes selecionados 
        @param is_make Make ou Build?
        """
        list_ctrl = self.__list_panel.list_ctrl
        
        if is_make:
            build_param = " "
        else:
            build_param = "-B" 

        grid.clear_progress_value()
        initial_time = datetime.datetime.today()
        selected_itens = self.__num_selected_items(list_selected, list_ctrl)
        processed_items = 0
        
        for selected in list_selected:
            if list_ctrl.IsChecked(selected.Id):
                list_ctrl.Select(selected.Id)
                file = list_ctrl.GetItem(selected.Id, c.LIST_IDX_NAME).GetText()
                path = list_ctrl.GetItem(selected.Id, c.LIST_IDX_PATH).GetText()
                compilation_build = list_ctrl.GetItem(selected.Id, c.LIST_IDX_OPTION).GetText()
                
                t1 = datetime.datetime.today()

                dom = xml.dom.minidom.parse(path + file)
                if compilation_build == CompilationBuild.DEBUG:
                    legopt.change_to_debug(dom)
                elif compilation_build == CompilationBuild.DISABLE_INLINE:
                    legopt.change_to_release(dom, disableInlineExpansion=True)
                else:
                    legopt.change_to_release(dom, disableInlineExpansion=False)
                    
                f = open(path + file, 'w')
                f.write(dom.toxml('UTF-8'))
                f.close()
                    
                
                #TODO: externalizar os .mak
                file = split(file, '.', 1)[0]
                file += ".mak"

                if self.comp_build.make(path, file, build_param) > 0:
                    break

                t2 = datetime.datetime.today()
                processed_items += 1
                total_time, elapsed_time = self.__time_calc(t2, initial_time ,processed_items, 
                                                  selected_itens)
                grid.set_progress_value(total_time.total_seconds(),
                                                     elapsed_time.total_seconds())
                
                list_ctrl.SetStringItem(selected.Id, c.LIST_IDX_TIME, str(t2-t1))
        
        grid.set_total_time(str(datetime.datetime.today()-initial_time))        
    
    def __time_calc(self, now, initial_time,  processed_items, selected_itens):
        """
        @todo: documentar este metodo
        """ 
        partial_time = now-initial_time
        average_time = partial_time/processed_items
        return (selected_itens*average_time), (processed_items*average_time) 
    
    def __num_selected_items(self, list_selected, list_ctrl):
        selected_itens = 0
        for selected in list_selected:
            if list_ctrl.IsChecked(selected.Id):
                selected_itens += 1
        return selected_itens 
        
###############################################################################

#TODO: refatorar pra ser um metodo da wxlistctrl (classe de interface grafica)
def get_selected_items(list_ctrl, column=0):
    """
    Pega os itens selecionados na lista da interface grafica
    @param list_ctrl componente da interface grafica
    @param column qual coluna
    """
    select_pkgs = []
    item = list_ctrl.GetFirstSelected()
    while item is not -1:
        if item is not -1:
            select_pkgs.append(list_ctrl.GetItem(item, column))
            
        item = list_ctrl.GetNextItem(item, wx.LIST_NEXT_ALL, 
                                     wx.LIST_STATE_SELECTED)
        
    return select_pkgs

#TODO: refatorar pra ser um metodo da wxlistctrl (classe de interface grafica)
def get_selected_from_here(list_ctrl, first_selected, column=0):
    """
    Pega os itens selecionados na lista da interface grafica
    @param list_ctrl componente da interface grafica
    @param first_selected primeiro listitem
    """
    select_pkgs = []
    item = first_selected.Id
    while item is not -1:
        if item is not -1:
            select_pkgs.append(list_ctrl.GetItem(item, column))
            
        item = list_ctrl.GetNextItem(item, wx.LIST_NEXT_ALL, 
                                     wx.LIST_STATE_DONTCARE)
        
    return select_pkgs        

###############################################################################        
