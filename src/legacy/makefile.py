# -*- coding: UTF-8 -*-
"""
Created on ???

@author: Cléber Camilo

"""

#TODO: refactory

import legacy.futil as futil
import os
import legacy.mpbuild as mpbuild
import fnmatch
from app.cache import Workspace

# Gera Make file de todos os arquivos BPRs e BPKs a partir de um diretorio

def find_type_project_path(path):
    """
    Verifica qual tipo projeto deve ser convertido
    BPK ou BPR
    """

    fileProject = futil.change_ext(path, 'bpk')
    if os.path.exists(fileProject) is False:
        fileProject = futil.change_ext(path, 'bpr')
    
    return fileProject

def find_type_project_bin(path, fileMake):
    """
    Converte a extensao do arquivo de make para EXE ou BPK
    baseado no na extensao do arquivo de projeto (BPK ou BPR).
    """

    FileProject = futil.change_ext(fileMake, 'bpk')
    if os.path.exists(path + '\\' + FileProject) is False:
        FileProject = futil.change_ext(fileMake, 'exe')
    else:
        FileProject = futil.change_ext(fileMake, 'bpl')
    
    return FileProject

def find_type_project(d, fileMake):
    """
    Verifica qual tipo projeto deve ser convertido BPK ou BPR
    """

    #TODO: colocar as extensoes definidas no pacote borland
    FileProject = futil.change_ext(fileMake, 'bpk')
    if os.path.exists(d + '\\' + FileProject) is False:
        FileProject = futil.change_ext(fileMake, 'bpr')
    
    return FileProject

def create_env_dir(d, fileMake):
    """
    Cria variavel de ambiente GmDir
    """

    f = open(d + '\\' + fileMake, 'a')
    #TODO: fazer o build nao depender disso? todos os bpks acessam $(GmDir)...
    f.write('GmDir = ' + Workspace().data['path'] +'packages\n')
    f.close()     


def gera_make(d, fileMake, numThreads):
    """
    Converte um projeto em makefile
    """

    for file in os.listdir(d):
        #TODO:externalizar a extensao do .mak para o pacote da borland
        if fnmatch.fnmatch(file, '*.mak'):
            os.remove(d + '\\' + file)

    FileProject = find_type_project(d, fileMake)
    
    # Converte projeto em makefile
    cmd = "bpr2mak.exe" + " -q " + "\"" + d + "\"" + "\\" + FileProject
    a = os.popen(cmd, 'r')
    a.close()
    
    create_env_dir(d, fileMake)

    mpbuild.gera_make_mp(d, fileMake, numThreads)

def proc_dir(dirs) :
    """
    Converte todos os projetos em dirs.
    Para ser usado em prompt
    """

    for d, file in dirs :        
        FileMake = futil.change_ext(file, 'mak')
        print 'Gerando ' + FileMake        
        gera_make(d, FileMake)
        #retcod = subprocess.call('bpr2mak.exe' + ' -q ' + d + '\\' + file, shell=True, stdout=subprocess.PIPE)        


def get_all_projects(path):
    tipos = ['*.bpk', '*.bpr']
    dirs = futil.get_dirs(path, tipos)    
    return dirs
