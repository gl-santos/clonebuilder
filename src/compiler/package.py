# -*- coding: UTF-8 -*-

"""
@author rpereira
Aug 31, 2011

Modulo que trata o grafo de dependências
"""
import lxml.etree as etree
import borland.vcl as vcl
import os
import compiler.graph as graph
import fnmatch
import re
from app.entity import Package
from borland.file import PACKAGE_EXTS
from borland.file import EXE_EXTS

#TODO: deixar essa classe generica, independente do compilador 
#(utilizando adaptadores/strategies)
class PackageList(object):
    """
    @author rpereira
    
    Classe de geracao de lista de pacotes
    """
    def __init__(self, fctrl):
        self.fctrl = fctrl
        self.__pkg_exts = PACKAGE_EXTS + EXE_EXTS
        #passar esses paths para o pacote da borland (modulo gemini/gdis)
        self.workspace = fctrl.workspace
        
    def generate_group_list(self, grp):
        groupname = os.path.basename(grp.file_path)
        groupname = os.path.splitext(groupname)[0].lower()
        groupname = "_".join(groupname.split())
        
        if groupname not in self.fctrl.cached['seed']:
            seeds = grp.find_list()
            self.fctrl.cached['seed'][groupname] = dict()
            change_ext = lambda seed: (os.path.splitext(seed)[0] + '.' + EXE_EXTS[0])
            for seed in seeds:
                seed = change_ext(seed)
                seed_low = seed.lower()
                self.__generate_graph(seed, seed_low)
                
                self.fctrl.cached['seed'][groupname].update(self.fctrl.cached['seed'][seed_low])
            
        glist = self.fctrl.cached['seed'][groupname]
        glist = graph.robust_topological_sort(glist)
        glist = map(lambda item: item[0], glist)
        
        glist.reverse()
        
        return glist
            
    def generate_package_list(self, seed_package):
        """
        Gera a lista de pacotes a partir de/ um pacote semente
        """
        try:
            seed_low = seed_package.lower()
            self.__generate_graph(seed_package, seed_low)
            
            list = graph.robust_topological_sort(self.fctrl.cached['seed'][seed_low])
            list = map(lambda item: item[0], list)
            
            list.reverse()
        except Exception, e:
            raise e
        
        return list
        
        
    def __generate_graph(self, seed_package, parent):
        """
        chamada recursiva para pegar todos os pacotes da dependencia
        """
        change_ext = lambda package: (os.path.splitext(package)[0] + '.' + PACKAGE_EXTS[0])
        
        if parent not in self.fctrl.cached['seed']:
            self.fctrl.cached['seed'][parent] = dict()
        
        #TODO: colocar as keys como lower case soh para windows
        seed_package_low = seed_package.lower()
        if seed_package_low in self.fctrl.cached['seed'][parent]:
            list_packages = self.fctrl.cached['seed'][parent][seed_package_low]
        else:  
            pkg, list_packages = self.__get_dependency_list(seed_package)
            
            list_packages = map(change_ext, list_packages)
            
            self.fctrl.cached['name'][seed_package_low] = pkg
            self.fctrl.cached['seed'][parent][seed_package_low] = list_packages
            
            for package in list_packages:
                pkg_low = package.lower()
                cur_pkg = self.fctrl.cached['seed'][parent].get(pkg_low)
                if cur_pkg is None:
                    self.fctrl.cached['seed'][parent][pkg_low] = self.__generate_graph(package, parent)
                
        return list_packages
    
        
    def __get_dependency_list(self, filename):
        """
        Pega a lista de dependecia do pacote passado por parametro
        """
        pkg = self.find_pkg_file(filename)
        
        xml = pkg.path + pkg.filename
        xml = etree.parse(xml)
        
        #TODO: externalizar essas strings, nao deve ser hardcoded 
        #(passar para o pacote borland)
        macros = xml.find("MACROS")
        xml_packages = macros.find("PACKAGES")
        values = xml_packages.get("value")
        
        #pega a lista de pacotes retirando os pacotes ignorados
        packages = values.split()
        set_pkgs = set(packages)
        set_ignore = set(vcl.ignore_packages)
        set_pkgs = set_pkgs.difference(set_ignore)
        
        list_packages = list(set_pkgs)
            
        return pkg, list_packages
   
    #TODO: juntas essas funcoes de achar arquivo com as do modulo da borland 
    def find_pkg_file(self, filename):
        """
        Acha o arquivo do nome do pacote indicado
        """
        split_filename = os.path.splitext(filename)[0]
        matches = []
        for path in self.workspace.data['include_path']:
            search_path = path + split_filename + os.sep
            #NAO RETIRAR A VARIAVEL dirnames e root, elas são utilizadas 
            #intrinsicamente
            for root, dirnames, filenames in os.walk(search_path):
                for filename in fnmatch.filter(filenames, filename):
                    matches.append(Package(split_filename, 
                                           filename, search_path))
                    break
                    
        if not matches:
            # Caso o package que venha no filename não corresponda ao bpk ou bpr
            # existentes
            matches = self.__full_find_pkg(filename)
            
        if not matches:
            paths = reduce(lambda x, y: x + ", " + y, self.workspace.data['include_path'])
            raise Exception(filename + ": file not found in " + paths)
        
        #TODO: tratar quando achar mais de um pacote nos includes
        return matches[0]
    
    def __full_find_pkg(self, filename):
        """
        Busca em todos os diretorios do include_path para encontrar o path
        do arquivo e gerar o Package dele 
        """
        matches = []
        for path in self.workspace.data['include_path']:
            for root, dirnames, filenames in os.walk(path):
                # Retira os diretórios ocultos da lista de diretórios
                dirnames = filter(lambda x: not re.search(r"\.", x), dirnames)
                file_filter = fnmatch.filter(filenames, filename)
                for filename in file_filter:
                    matches.append(Package(os.path.splitext(filename)[0], 
                                   filename, root+os.sep))                            
                    break
        return matches

