# -*- coding: UTF-8 -*-

"""
@author rpereira
Aug 19, 2011

Modulo da aplicação
"""

import argparse
from controller.cmdline import CmdLineController
from app.consts import CompilationBuild
from types import *

class CmdApp(object):
    """
    @author rpereira
    
    Borg Design Pattern
    Aplicação com interface de linha de comando
    """
    __shared_state = {}
    def __init__(self, args):
        self.__dict__ = self.__shared_state
        
        self.cmd = args[0]
        self.args = args[1:]
        
    def run(self):
        parsed_args = self.parse()
     
        threads = getattr(parsed_args, 'thread')
        if type(threads) is ListType:
            threads = threads[0]
        
        cmd_ctrl = CmdLineController(getattr(parsed_args, 'build'),
                                     getattr(parsed_args, 'make'),
                                     getattr(parsed_args, 'versao_build')[0],
                                     threads,
                                     getattr(parsed_args, 'work_space')[0])
                
        if getattr(parsed_args, 'subparser_name') == "packages" :
            cmd_ctrl.run_packages(getattr(parsed_args, 'full_release'),
                                  getattr(parsed_args, 'full_debug'),
                                  getattr(parsed_args, 'inline_expansions'))
        elif getattr(parsed_args, 'subparser_name') == "seeds" :
            cmd_ctrl.set_excludes(getattr(parsed_args, 'exclude_debug'),
                                  getattr(parsed_args, 'exclude_inline'),
                                  getattr(parsed_args, 'exlude_release'))

            list_release = getattr(parsed_args, 'full_release')
            list_debug = getattr(parsed_args, 'full_debug')
            list_inline = getattr(parsed_args, 'inline_expansions')
                        
            if list_release != None :
                cmd_ctrl.run_seeds(CompilationBuild.RELEASE,list_release)
            elif list_debug != None :
                cmd_ctrl.run_seeds(CompilationBuild.DEBUG,list_debug)
            elif list_inline != None :
                cmd_ctrl.run_seeds(CompilationBuild.DISABLE_INLINE,list_inline)                

        
    def parse(self):    
        parser = argparse.ArgumentParser(description="Compile your seeds or packages")
                                
        subparsers = parser.add_subparsers(help='Compile a list of packages or package and its dependencies', dest='subparser_name')
        
        parser_seeds = subparsers.add_parser('seeds', help='Compile a package and its dependencies')

        group1 = parser_seeds.add_mutually_exclusive_group(required=True)
        group1.add_argument("-m","--make", action='store_true')
        group1.add_argument("-b","--build", action='store_true')
        
        group2 = parser_seeds.add_mutually_exclusive_group(required=True)
        group2.add_argument("-d","--full-debug", nargs='*')
        group2.add_argument("-r","--full-release", nargs='*')
        group2.add_argument("-i","--inline-expansions", nargs='*')
        
        group3 = parser_seeds.add_argument_group()     
        group3.add_argument("-ed","--exclude-debug", nargs='*')
        group3.add_argument("-ei","--exclude-inline", nargs='*')
        group3.add_argument("-er","--exlude-release", nargs='*')
        
        parser_seeds.add_argument("-th","--thread", nargs=1, type=int, default=4)
        parser_seeds.add_argument("-vb","--versao-build", nargs=1, required=True)
        parser_seeds.add_argument("-ws","--work-space", nargs=1, required=True)
        
        parser_packages = subparsers.add_parser('packages', help='Compile lists of packages')

        group4 = parser_packages.add_mutually_exclusive_group(required=True)
        group4.add_argument("-m","--make", action='store_true')
        group4.add_argument("-b","--build", action='store_true')
        
        group5 = parser_packages.add_argument_group()
        group5.add_argument("-d","--full-debug", nargs='*')
        group5.add_argument("-r","--full-release", nargs='*')
        group5.add_argument("-i","--inline-expansions", nargs='*')        

        parser_packages.add_argument("-th","--thread", nargs=1, type=int, default=4)
        parser_packages.add_argument("-vb","--versao-build", nargs=1, required=True)
        parser_packages.add_argument("-ws","--work-space", nargs=1, required=True)
        
        return parser.parse_args(self.args)
    
     

