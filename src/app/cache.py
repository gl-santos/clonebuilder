# -*- coding: UTF-8 -*-

"""
@author rpereira
Sep 23, 2011

Modulo de caching da aplicação
"""
import pickle
from app.consts import APP_PATH
import os
import copy

"""Path e filename de onde serao salvos as preferencias"""
CACHE_PATH = APP_PATH + "data/"
SETTINGS_FILE = "cache_settings.data"
WORKSPACE_FILE = "workspace.data"

class Workspace(object):
    """
    @author rpereira
    
    Area de trabalho de onde os pacotes a serem compilados estão
    """
    __shared_state = {}
    def __init__(self):
        self.__dict__ = self.__shared_state
        
        if not self.__shared_state:
            self.data = {}
            """path da workspace"""
            self.data['path'] = ""
            
            """
            paths internos da workspace
            @TODO: parametrizar os include paths para fora da aplicacao
            """
            #TODO: resolver a busca de pacotes com mesmo nome independente da ordem dos include paths
            self.data['include_base'] = ([
                "\\Packages\\",
                "\\Executaveis\\Administracao\\",
                "\\Executaveis\\Aplicativos\\",
                "\\Executaveis\\Desenv\\",
                "\\Executaveis\\Servidores\\",
                "\\Executaveis\\Testes\\",
                "\\Executaveis\\",
                "\\"])
            
            self.data['include_path'] = copy.deepcopy(self.data['include_base'])
            self.load()
        
    def save(self):
        """
        Salva os dados da workspace no arquivo
        """
        pickle.dump(self.data, open(CACHE_PATH + WORKSPACE_FILE, "wb"))
        
    def load(self):
        """
        Carrega os dados do arquivo
        """
        if os.path.exists(CACHE_PATH + WORKSPACE_FILE):
            self.data = pickle.load(open(CACHE_PATH + WORKSPACE_FILE, "rb"))
            
    def exists(self):
        """
        Verifica a existência da workspace
        """
        if os.path.exists(self.data['path']):
            ret = True
        else:
            ret = False
        return ret
    
    def is_valid(self):
        """
        Verifica a validade do path da workspace
        """
        if self.data['path'] != "":
            ret = True
        else:
            ret = False
        return ret
    
    def change_workspace(self, path):
        """
        Muda o path da workspace
        @param path novo path
        """
        if os.path.exists(path):
            self.data['path'] = path + "\\"
            self.data['include_path'] = map(lambda x: path + x,
                                            self.data['include_base'])
        else:
            raise Exception("Workspace path doesnt exist: " + path)
    
###############################################################################

def dump(guictrl):
    """
    Descarregar as informações de preferencias da interface grafica para um
    arquivo
    @param guictrl janela da aplicacao
    """
    guictrl.workspace.save()
    
    settings = {}

    list_ctrl = guictrl.list_panel.list_ctrl
    package_list = []
    for idx in range(list_ctrl.GetItemCount()):
        checked = list_ctrl.IsChecked(idx)
        package_list.append((list_ctrl.GetItem(idx, 0).m_text,
                     list_ctrl.GetItem(idx, 1).m_text,
                     list_ctrl.GetItem(idx, 2).m_text,
                     checked))

    list_ctrl = guictrl.list_seed.list_ctrl
    seed_list = []
    for idx in range(list_ctrl.GetItemCount()):
        seed_list.append(list_ctrl.GetItem(idx, 0).m_text)

    settings['packages'] = guictrl.cached

    settings['threads'] = guictrl.get_num_threads()
    settings['version'] = guictrl.get_version()

    settings['main_frame'] = {}
    settings['main_frame']['is_maximized'] = guictrl.main_frame.IsMaximized()
    settings['main_frame']['size'] = (guictrl.main_frame.GetSize().x,
                                      guictrl.main_frame.GetSize().y)

    settings['seed_list'] = seed_list
    settings['package_list'] = package_list
    settings['perspective'] = guictrl.aui_mgr.SavePerspective()

    pickle.dump(settings, open(CACHE_PATH + SETTINGS_FILE, "wb"))

def load(guictrl):
    """
    Recupera as informações de preferencias do arquivo .data
    @param guictrl janela da aplicacao
    """
    #TODO: tratar erro na hora de carregar um .data
    if os.path.exists(CACHE_PATH + SETTINGS_FILE):
        try:
            settings = pickle.load(open(CACHE_PATH + SETTINGS_FILE, "rb"))

            guictrl.aui_mgr.LoadPerspective(settings['perspective'])

            guictrl.list_seed.from_list(settings['seed_list'])
            guictrl.list_panel.from_list(settings['package_list'])

            if settings['main_frame']['is_maximized']:
                guictrl.main_frame.Maximize()
            else:
                guictrl.main_frame.SetSize(settings['main_frame']['size'])

            if settings['threads'] == None:
                guictrl.set_num_threads(1)
            else:
                guictrl.set_num_threads(settings['threads'])
                
            guictrl.set_version(settings['version'])

            guictrl.cached = settings['packages']
            
            guictrl.tool_panel.grid.buttons["num_threads"].SetValue(guictrl.get_num_threads())

        except Exception, e:
            #TODO: mensagem pro usuario informando que o cache ta corrompido e sera recriado
            os.remove(CACHE_PATH + SETTINGS_FILE)
            raise e
        
    guictrl.load_defaults()
        
