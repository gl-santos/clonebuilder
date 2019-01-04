# -*- coding: UTF-8 -*-

"""
@author ?
?

tratamentos variados
"""

import os
import glob

def change_ext(file, ext) :
    """
    altera a extensao do arquivo file para ext
    """
    return file[0:len(file)-4] + '.' + ext

''
def get_dirs(raiz, tipos) :
    """
    Retorna todos os diretorios a partir do diretorio raiz e arquivos com as
    extensoes indicadas por tipos retorna no formato [path, file]
    """

    lista = []

    for root, dirs, files in os.walk(raiz) :
        os.chdir(root)
        for t in tipos :
            file = glob.glob(t)
            if file :
                l = []
                l.append(root)
                l.append(file[0])
                lista.append(l)
    return lista

def trata_texto(text):
        textList = text.split('\n')
        while textList.count('') > 0:
                textList.remove('')
        for i in range(len(textList)):
                textList[i] = textList[i].strip()

        return textList

def elimina_enter_line(line):
    return line[0:len(line)-1]

def elimina_enter(lines):
    """
    Elimina CR/LF do final de cada linha. Todas as linhas da lista deve possuir
    o caracter CR/LF
    """

    newLines = []
    for line in lines:
        newLines.append(line[0:len(line)-1])

    return newLines


