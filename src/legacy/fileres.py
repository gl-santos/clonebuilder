# -*- coding: UTF-8 -*-

from __future__ import with_statement
from futil import change_ext
from os import popen
import codecs
from app.cache import Workspace

#TODO: externalizar esses parametros de res para configuracao
class DataRes(object):
    company_name = ""
    fileVersion = ""
    internalName = ""
    originalFileName = ""
    fileDescription = ""
    productName = ""
    legalCopyright = ""
    legalTrademarks = ""
    comments = "Gerado por Clone"

class FileRes:
    def CriaRes(self, path, file, dataRes):
        self.CriaRC(path, file, dataRes)
        self.CompilaRc(path, file)

    def CompilaRc(self, path, file):
        fileRc = change_ext(file, 'rc')
        popen("brcc32 " + path + "\\" + fileRc)
    
    def CriaRC(self, path, file, dataRes):
        #versao com virgula
        versao_v = dataRes.fileVersion.replace(".", ",")
        
        #Icon placed first or with lowest ID value becomes application icon
        #MAINICON é o índice buscado pelo compilador na hora de criar o EXE
        
        out = 'MAINICON ICON "'+ Workspace().data['path'] +'Packages\Resources\PROLUX.ICO"\n'
        out += 'VS_VERSION_INFO VERSIONINFO\n'
        out += 'FILEVERSION ' + versao_v + '\n'
        out += 'PRODUCTVERSION ' + versao_v + '\n'
        out += 'FILEFLAGSMASK VS_FFI_FILEFLAGSMASK\n'
        out += 'FILEOS VOS__WINDOWS32\n'
        out += 'FILETYPE VFT_APP\n'
        out += 'BEGIN\n'
        out += ' BLOCK "StringFileInfo"\n'
        out += '  BEGIN\n'
        out += '  BLOCK "040904E4"\n'
        out += '   BEGIN\n'
        out += '        VALUE "CompanyName", "' + dataRes.company_name + '\\x00"\n'
        out += '        VALUE "FileDescription", "' + dataRes.fileDescription + '\\x00"\n'
        out += '        VALUE "FileVersion", "' + dataRes.fileVersion + '\\x00"\n'
        out += '        VALUE "InternalName", "' + dataRes.internalName + '\\x00"\n'
        out += '        VALUE "LegalCopyright", "' + dataRes.legalCopyright + '\\x00"\n'
        out += '        VALUE "LegalTrademarks", "' + dataRes.legalTrademarks + '\\x00"\n'
        out += '        VALUE "OriginalFilename", "' + dataRes.originalFileName + '\\x00"\n'
        out += '        VALUE "ProductName", "' + dataRes.productName + '\\x00"\n'
        out += '        VALUE "ProductVersion", "' + dataRes.fileVersion + '\\x00"\n'
        out += '        VALUE "Comments", "' + dataRes.comments + '\\x00"\n'
        out += '   END\n'
        out += '  END\n'
        out += ' BLOCK "VarFileInfo"\n'
        out += ' BEGIN\n'
        out += '  VALUE "Translation"\n'
        out += '     ,0x0409, 1252\n'
        out += ' END\n'
        out += 'END\n'

        #eh necessario abrir o arquivo .rc como utf-8
        fileRc = change_ext(file, 'rc')
        with codecs.open(path + "\\" + fileRc, 'w', "latin-1") as f:
            f.write(out)

