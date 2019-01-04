# -*- coding: UTF-8 -*-

"""
@author rpereira
Aug 19, 2011

Arquivo principal, faz a decisao se foi chamada a interface grafica ou linha
de comando
"""

import sys
import traceback

#para contornar erro do pyinstall no Windows 7
import atexit 

from app.cmd import CmdApp 

def main():
    """
    Inicializacao da aplicação 
    """
    try:
        app = CmdApp(sys.argv)
        app.run()
    except Exception, e:
        print traceback.format_exc()
        raw_input()

if __name__ == '__main__':
    main()

