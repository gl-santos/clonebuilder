# -*- coding: UTF-8 -*-

"""
@author rpereira
May 3, 2012


"""
from front import FrontController
from app.consts import CompilationType
from compiler.package import PackageList
import compiler.build as build
import datetime
from app.consts import CompilationBuild
import xml.dom.minidom
import legacy.comp_option as legopt
import os
from borland.file import ProjectGroup
from borland.file import GROUP_EXTS

class CmdLineController(FrontController):
    """
    @author: Rodrigo Muzzi
    
    Front controller da linha de comando
    """
    def __init__(self, is_build, is_make, version, threads, workspace_path):
        FrontController.__init__(self)
        if is_make:
            self.compilation_type = CompilationType.MAKE
        elif is_build:
            self.compilation_type = CompilationType.BUILD
        else:
            raise Exception("Opção de CompilationType não existente")
            
        self.set_version(version)
        self.set_num_threads(threads)
        self.ex_debug = None
        self.ex_inline = None
        self.ex_release = None
        
        self.workspace.change_workspace(workspace_path)
        
        self.packageList = PackageList(self)
        self.comp_build = build.Ctrl()
        self.comp_build.set_cmd()
    
    def set_excludes(self, exclude_debug, exclude_inline, exclude_release):
        self.ex_debug = exclude_debug
        self.ex_inline = exclude_inline
        self.ex_release = exclude_release
        
    def run_seeds(self, compilation_build, list_seeds):
        """
        Roda o algoritmo SEEDS
        @param compilation_build opcao de build (debug/release/inline)
        @param list_seeds 
        """
        t1 = datetime.datetime.today()
        for seed in list_seeds:
            ext = os.path.splitext(seed)[1][1:]
            
            if ext in GROUP_EXTS:
                group = self.packageList.find_pkg_file(seed)
                full_list = self.packageList.generate_group_list(ProjectGroup(group.path + group.filename))
            else:
                full_list = self.packageList.generate_package_list(seed)
                
            for item in full_list:
                package = self.cached['name'][item]
                
                if self.ex_debug != None and self.ex_debug.count(package.name) > 0:
                    package.build_opt = CompilationBuild.DEBUG
                elif self.ex_release != None and self.ex_release.count(package.name) > 0:
                    package.build_opt = CompilationBuild.RELEASE
                elif self.ex_inline != None and self.ex_inline.count(package.name) > 0:
                    package.build_opt = CompilationBuild.DISABLE_INLINE
                else:
                    package.build_opt = compilation_build
                    
                ret = self.__make(package)
                #FIXME retorno de legado, deve ser refatorado
                if (ret == 100):
                    break
                
        t2 = datetime.datetime.today()
        print "Tempo Total:" + str(t2-t1)
                
    def run_packages(self, list_release, list_debug, list_inline):
        ret = 0
        t1 = datetime.datetime.today()
        if list_release != None :
            for release in list_release:
                #FIXME retorno de legado, deve ser refatorado
                if (ret == 100):
                    break
                package = self.packageList.find_pkg_file(release)
                package.build_opt = CompilationBuild.RELEASE
                ret = self.__make(package)

        if list_debug != None :
            for debug in list_debug:
                #FIXME retorno de legado, deve ser refatorado
                if (ret == 100):
                    break
                package = self.packageList.find_pkg_file(debug)
                package.build_opt = CompilationBuild.DEBUG
                ret = self.__make(package)

        if list_inline != None :
            for inline in list_inline:
                #FIXME retorno de legado, deve ser refatorado
                if (ret == 100):
                    break
                package = self.packageList.find_pkg_file(inline)
                package.build_opt = CompilationBuild.DISABLE_INLINE
                ret = self.__make(package)

        
        t2 = datetime.datetime.today()
        print "Tempo Total:" + str(t2-t1)
                
    def __make(self, package):
        dom = xml.dom.minidom.parse(package.path + package.filename)
        if package.build_opt == CompilationBuild.DEBUG:
            legopt.change_to_debug(dom)
        elif package.build_opt == CompilationBuild.DISABLE_INLINE:
            legopt.change_to_release(dom, disableInlineExpansion=True)
        else:
            legopt.change_to_release(dom, disableInlineExpansion=False)
        
        t1 = datetime.datetime.today()
        file = package.name 
        file += ".mak"
        
        build_param = " "
         
        if self.compilation_type == CompilationType.BUILD:
            build_param = "-B"
        
        ret = self.comp_build.make(package.path, file, build_param)
        
        t2 = datetime.datetime.today()
        print "Tempo Pacote "+package.name+":"+str(t2-t1)
        
        return ret