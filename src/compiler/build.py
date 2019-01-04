# -*- coding: UTF-8 -*-

"""
@author rpereira
Apr 10, 2012

Controle do build, extract feito de funções do legado.
"""

import legacy.makefile as mkfile
from legacy.compiler_builder import CompilerBuilder
import legacy.futil as futil
import wx 
import string
import re
from controller.front import FrontController
from legacy.file import BuilderFile
import legacy.fileres as fileres
import legacy.makefile as mkfile
import legacy.altver as altver
import multiprocessing

import sys

class Msg:
    SUCCESS = 0
    WARNING = 1
    ERROR = 2
    EOF = 3

class Ctrl(object):
    """
    @author rpereira
    
    Classe de controle do build.
    """
    #Borg Design Pattern
    __shared_state = {}

    def __init__(self):
        self.__threads_spin = None
        self.__console_panel = None
        self.__list_ctrl = None
        
        self.__dict__ = self.__shared_state
        
        self.cancel = False
        self.cmd = False
        
        self.__error = False
        
    def set_cmd(self):
        self.cmd = True
        
    def set_console_panel(self, console_panel):
        self.__console_panel = console_panel
        self.__list_ctrl = console_panel.list_ctrl

    def make(self, path, file, paramExtr = ""):
        """
        Build/make geral do arquivo de makefile indicado 
        @param path do arquivo de makefile
        @param parametro adicional ao comando de build/make 
        """

        fctrl = FrontController()
        self.__error = False

        #TODO: tirar esses returns 100 (mudar para uma mensagem de erro)
        if not self.altera_versao(fctrl.get_version(), path):
            return 100

        #TODO: tirar esses returns 100
        if not self.update_res(path, file):
            return 100
        
        num_threads = fctrl.get_num_threads()
        try:
            if num_threads == 0:
                num_threads = multiprocessing.cpu_count()
        except Exception:
            num_threads = 1

        mkfile.gera_make(path, file, num_threads)
        self.__log("Makefile: " + file + " atualizado")

        #TODO: extract .mak extension
        self.job = CompilerBuilder(
            path,
            file,
            num_threads > 1)
        
        self.job.compile(paramExtr)

        out = " "
        self.__log("make " + file)
        
        #TODO: tirar o while true
        while True:
            out = self.job.readMsg()
            if out == "":
                self.__log("FIM: " + file)
                return self.job.close()
            
            self.__log(out)

            if self.cancel == True or self.__error == True:
                self.job.close()
                self.__log("Cancelado: " + file)
                self.cancel = False
                return 100
        self.job = None
        
        return 0

    def altera_versao(self, version, path):
        """
        Edita o BPK/BPR alterando a versão
        """
        success = True
        out = ""

        try:
            change_version = altver.AlteraVer(version, path)
            out = change_version.run()
            self.__log(out)
        except Exception as e:
            print e
            success = False
            raise e

        return success

    def update_res(self, path, file):
        """
        Edita e gera o arquivo RES do projeto
        """
        success = True
        builder = None
        
        try:
            builder = BuilderFile(path + "\\" + file)
            builder.open()
            versao = builder.getInfo("FileVersion")
            fileDescription = builder.getInfo("FileDescription")
            productName = builder.getInfo("ProductName")
            dataRes = fileres.DataRes();
            dataRes.fileVersion = versao
            dataRes.fileDescription = fileDescription
            dataRes.productName = productName
            fileProject = mkfile.find_type_project_bin(path, file)
            dataRes.internalName = fileProject
            dataRes.originalFileName = fileProject
            self.generate_res_file(path, file, dataRes)
        except:
            self.__log("Nao foi possivel gerar RES para " + file)
            success = False
        finally:
            if builder <> None:
                builder.close()

        return success

    def generate_res_file(self, path, file, dataRes):
        """
        Gera arquivo RES do projeto
        """

        compRes = fileres.FileRes()
        compRes.CriaRes(path, file, dataRes)
        fileRes = futil.change_ext(file, 'res')
        self.__log("Arquivo RES: " + fileRes + " gerado")
        
        
    def __check_msg(self, linha):
        ret = Msg.SUCCESS
        if ((re.match("[E|e]rror", linha) or re.match(".*[E|e]rror [E]\d\d\d\d", linha))and 
            not (string.find(linha, "Error messages:") == 0 and 
            string.find(linha, "None") != -1)):
            ret = Msg.ERROR
            
        elif (re.match("[F|f]atal", linha) and 
              not (string.find(linha, "None") != -1)):
            ret = Msg.ERROR
        elif (re.match("FIM:", linha) and 
              not (string.find(linha, "None") != -1)):
            ret = Msg.EOF
            
        elif (re.match(".*[W|w]arning [W]\d\d\d\d", linha)and 
              not (string.find(linha, "Warning messages:") == 0 and 
              string.find(linha, "None") != -1)):
            ret = Msg.WARNING
            
        return ret

    def __log(self, text):
        """
        Imprime texto, na saída definida
        
        @param text dado a ser impresso
        """
        listVal = futil.trata_texto(text)
        for linha in listVal:
            msg_ret = self.__check_msg(linha)
            
            if self.cmd:
                if (msg_ret == Msg.ERROR):
                    self.__error = True
                print linha
            else:
                index = self.__list_ctrl.GetItemCount()
                self.__list_ctrl.InsertStringItem(index, linha)
                
                self.__list_ctrl.EnsureVisible(self.__list_ctrl.GetItemCount()-1)
                
                color = wx.WHITE
                if (msg_ret == Msg.ERROR):
                    color = wx.RED
                    self.__error = True
                elif (msg_ret == Msg.WARNING):
                    color = wx.NamedColour("yellow")
                elif (msg_ret == Msg.EOF):
                    color = wx.GREEN

                self.__list_ctrl.SetItemBackgroundColour(index, color)
                self.__list_ctrl.SetColumnWidth(0, wx.LIST_AUTOSIZE)

