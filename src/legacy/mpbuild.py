# -*- coding: UTF-8 -*-
"""
Created on ???

@author: Gustavo Gomes

"""

#TODO: refactory

import os
import string
from threading import Thread
from threading import Condition
from threading import Event
import subprocess

def obtem_lista_objs(makeOrig):
    """Obtem a lista de objetos do conteudo do arquivo .mak"""

    objSection = False
    resSection = False
    objList = ''
    resList = ''
    for linha in makeOrig:

        if string.find(linha, 'OBJFILES = ') >= 0:
            objSection = True

        if objSection:
            if string.find(linha, 'RESFILES = ') == -1:
                objList += linha
            else:
                objSection = False
                resSection = True

        if resSection:
            if string.find(linha, 'MAINSOURCE = ') == -1:
                resList += linha
            else:
                resSection = False


    objList = string.split(objList.replace('OBJFILES = ', '').replace(' \\', ''))
    resList = string.split(resList.replace('RESFILES = ', '').replace(' \\', ''))

    return (objList, resList)

def divide_lista_objs(objList, resList, numThreads):
    """Divide a lista de objetos em numCPU sublistas"""

    numThreads = int(numThreads)
    numObj = len(objList)
    numSubSet = 1
    if int(numThreads) > int(numObj):
        numSubSet = numObj
    else:
        numSubSet = numThreads
    markerList = []
    
    for i in range(numSubSet):
        markerList.append(0)
    i = numObj

    while i > 0:
        for j in range(numSubSet):
            if i > 0:
                markerList[j] = markerList[j] + 1
                i = i - 1

    for i in range(numSubSet):
        objList.insert(i, [])
        for j in range(markerList.pop(0)):
            objList[i].append(objList.pop(i + 1))

    if numThreads <= numObj:
        resList.insert(0, [])
        remaider = len(resList[1:])
        for j in range(remaider):
            resList[0].append(resList.pop(1))
        while len(resList) < len(objList):
            resList.insert(0, [])
    else:
        lenResList = len(resList)
        for i in range(lenResList):
            resList.insert(i, [])
            resList[i].append(resList.pop(i + 1))
        while (len(objList) + len(resList)) > numThreads:
            resList[0].append(resList[1].pop())
            resList.pop(1)
        for i in range(len(objList)):
            resList.insert(0, [])
        while len(resList) > len(objList):
            objList.append([])

    return (objList, resList)

def gera_texto_make(objList, resList):
    """Gera as linhas OBJFILES e RESFILES para cada arquivo .mak"""

    objTextList = []
    group = 4

    for i in range(len(objList)):
        objIndex = 0
        objTextList.append('OBJFILES = ')
        for obj in objList[i]:
            if objIndex % group == 0 and objIndex <> 0:
                objTextList[i] += '\\\n    '
            objTextList[i] += obj + ' '
            objIndex += 1

        objIndex = 0
        objTextList[i] += '\nRESFILES = '
        for obj in resList[i]:
            if objIndex % group == 0 and objIndex <> 0:
                objTextList[i] += '\\\n    '
            objTextList[i] += obj + ' '
            objIndex += 1

        objTextList[i] += '\n'

    return objTextList

def gera_inicio_make(makeOrig, tipo):
    """Gera string com o inicio do arquivo .mak ate a linha OBJFILES exclusive"""

    try:
        if tipo == 'C':
            padrao = "OBJFILES = "
        elif tipo == 'L':
            padrao = "MAINSOURCE = "
    
        indexLinha = 0
        for linha in makeOrig:
            if string.find(linha, padrao) >= 0:
                indexLinha = makeOrig.index(linha)
                break;
    
        listaMake = makeOrig[:indexLinha]
        inicioMake = string.join(listaMake, '')
    except Exception, e:
        raise e

    return inicioMake

def gera_meio_make(makeOrig, name = ''):
    """Gera string com a linha MAINSOURCE do arquivo .mak ate a linha $(PROJECT): exclusive"""

    for linha in makeOrig:
        if string.find(linha, 'MAINSOURCE = ') >= 0:
            indexInicio = makeOrig.index(linha)
        if string.find(linha, '$(PROJECT): ') >= 0:
            indexFim = makeOrig.index(linha)
            break;

    listaMake = makeOrig[indexInicio : indexFim]
    
    for i in range(len(listaMake)):
        if string.find(listaMake[i], 'CFLAG1 = ') >= 0:
            listaMake[i] = listaMake[i].replace('vcl60.csm', 'vcl60' + name + '.csm')    

    meioMake = string.join(listaMake, '')

    return meioMake

def exeProject(makeOrig):
    """Determina se o PROJECT eh um executavel"""

    for linha in makeOrig:
        if string.find(linha, 'PROJECT = ') >= 0:
            if linha[len(linha) - 4 : len(linha) - 1] == 'exe':
                return True

    return False

def gera_rules_make(makeOrig, tipo):
    """Gera string com as regras do make para compilar ou linkar"""

    for linha in makeOrig:
        if string.find(linha, '$(PROJECT): ') >= 0:
            indexlinha = makeOrig.index(linha)
            break;

    listaMake = makeOrig[indexlinha:]

    if tipo == 'C':
        listaMake[0] = '$(PROJECT): $(OBJFILES) $(RESDEPEN)\n'
        if not exeProject(makeOrig):
            listaMake[1:9] = []
        else:
            listaMake[2] = '    $(LFLAGS) -L$(LIBPATH), +\n'
            listaMake.pop(3)
            listaMake[5] = '    $(DEFFILE)\n'
            listaMake.pop(6)
    elif tipo == 'L':
        listaMake[0] = '$(PROJECT): $(OTHERFILES) $(IDLGENFILES) $(DEFFILE)\n'

    rulesMake = string.join(listaMake, '')

    return rulesMake

def cria_arquivos_make(path, file, makeOrig, objTextList):
    """Gera arquivos make"""

    inicioMakeC = gera_inicio_make(makeOrig, 'C')
    inicioMakeL = gera_inicio_make(makeOrig, 'L')
    meioMakeL = gera_meio_make(makeOrig)
    rulesMakeC = gera_rules_make(makeOrig, 'C')
    rulesMakeL = gera_rules_make(makeOrig, 'L')

    index = 1
    for listaObj in objTextList:
        makeFile = string.replace(file, ".mak", 'C' + str(index) + ".mak")
        f = open(path + '\\' + makeFile , 'w')
        f.write(inicioMakeC)
        f.write(listaObj)
        f.write(gera_meio_make(makeOrig, 'C' + str(index)))
        f.write(rulesMakeC)
        f.close()
        index += 1

    makeFile = string.replace(file, ".mak", "L.mak")
    f = open(path + '\\' + makeFile , 'w')
    f.write(inicioMakeL)
    f.write(meioMakeL)
    f.write(rulesMakeL)
    f.close()

def gera_make_mp(path, file, numThreads):
    """ Gera multiplos make files para compilacao em paralelo"""

    #TODO: externalizar a extensao .mak
    f = open(path + '\\' + file, 'r')
    makeOrig = f.readlines()
    f.close()

    (objList,resList) = obtem_lista_objs(makeOrig)    

    if numThreads > 1:
        (objList, resList) = divide_lista_objs(objList, resList, numThreads)
        objTextList = gera_texto_make(objList, resList)
        cria_arquivos_make(path, file, makeOrig, objTextList)

class MultiProcBuilder:

    def __init__(self, makeFile, param):

        makeFileList = []
        index = 1
        while os.path.isfile(os.getcwd() + '\\' +
                             makeFile.replace('.mak', 
                                              'C' + str(index) + '.mak')):
            makeFileList.append(makeFile.replace('.mak',
                                                 'C' + str(index) + '.mak'))
            index = index + 1
            #TODO: externalizar a extensoes para parametros configuraveis
        makeFileLinker = makeFile.replace('.mak', 'L.mak')

        self.condition = Condition()
        self.output = []
        self.group = MakeGroup(makeFileList, makeFileLinker,
                               self.output, self.condition, param)

    def start(self):
        """Dispara compilacao multiprocessada"""

        self.group.start()

    def readMsg(self):

        self.condition.acquire()
        out = ""
        if len(self.output) == 0 and self.group.isAlive():
            self.condition.wait()
        while len(self.output) > 0:
            out += self.output.pop(0)
        self.condition.release()

        return out

    def getResult(self):
        return self.group.status    

class MakeGroup(Thread):
    """Thread que agrupa as threads de compilacao"""
    def __init__(self, makeList, lastMake, output, condition, param):
        Thread.__init__(self)
        self.threadList = []
        for make in makeList:
            self.threadList.append(Make(make, output, condition, param))
        self.lastThread = Make(lastMake, output, condition, param)
        self.output = output
        self.condition = condition
        self.status = None

    def run(self):
        for thread in self.threadList:
            thread.start()
        for thread in self.threadList:
            thread.join()
            self.status =  self.status or thread.status
        self.lastThread.start()
        self.lastThread.join()
        self.status = self.status or self.lastThread.status

        #adiciona um espaco no arquivo, para nao "colar"
        self.condition.acquire()
        self.output.append("")
        self.condition.notify()
        self.condition.release()
        
    def stop_all(self):
        self.lastThread.stop()
        for thread in self.threadList:
            thread.stop()


class Make(Thread):
    """classe que faz o build/make, é chamada individualmente por thread"""
    
    """EDIT: adicionado o evento de stop da thread, para interrompe-la"""
    def __init__(self, mkfile, output, condition, param = ""):
        Thread.__init__(self)
        self._stop = Event()
        
        self.mkfile = mkfile
        self.param = param
        self.output = output
        self.condition = condition
        self.status = None
        
        #checa se o arquivo .mak é necessário ser linkado 
        #(bug do Make Paralelo não linkar)
        if (self.mkfile[-5:] == "L.mak"):
            self.param = " -B "

    def run(self):
        """
        Este bloco de codigo abaixo era o def run(self) antigo, que usava o
        subprocess.Popen inves do os.popen (que está deprecated), entretanto o
        pyInstaller (aplicativo utilizado para gerar executavel para windows)
        tem algum problema com o subprocess.Popen, logo trocando para o
        os.popen, tudo passa a funcionar corretamente. Deve ficar atento ao
        fato da funcao ser deprecated, pois quando o suporte a ela cair, será
        necessário voltar o uso para o subprocess, fazendo que o pyInstaller
        gere um executável não funcional, contudo existe a possibilidade de
        até lá o bug ser corrigido no pyinstaller.
        
        cmd = "make -f " + self.mkfile + " -K " + self.param
        process = subprocess.Popen(cmd, 0, stdout=subprocess.PIPE)
        
        for line in iter(process.stdout.readline, ''):
            if (self.stopped()):
                break
            out = line.rstrip()
            self.condition.acquire()
            self.output.append(out)
            self.condition.notify()
            self.condition.release()
            
        self.status = process.stdout.close()
        """
        f = os.popen("make -f " + self.mkfile + " -K " + self.param, 'r')
        out = f.readline()
        while(out != ""):
            self.condition.acquire()
            self.output.append(out)
            self.condition.notify()
            self.condition.release()
            out = f.readline()
        self.status = f.close()
        
    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

