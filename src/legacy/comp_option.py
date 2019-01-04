# -*- coding: UTF-8 -*-

#TODO: colocar essas especificidades de melhor forma, no pacote borland

import xml.dom.minidom
import string
import re

def replace_param(rc, old, new):
	if re.search(r"(\s|^)" + old.replace('$','\$').replace('+','\+') + "(\s|$)", rc):
		lista = rc.split()
		idx = lista.index(old)
		lista.remove(old)
		lista.insert(idx, new)
		rc = string.join(lista, ' ')
	return rc

def add_param(rc, param, separator = ' '):
	if separator == ' ':
		if re.search(r"(\s|^)" + param + "(\s|$)", rc) is None:
			lista = rc.split()
			lista.append(param)
			rc = string.join(lista, ' ')
	elif separator == ';':
		if re.search(r"" + param, rc) is None:
			lista = re.split(';*', rc.replace(' ', ''))
			lista.append(param)
			rc = string.join(lista, ';')
	return rc

def remove_param(rc, param, separator = ' '):
	if separator == ' ':
		if re.search(r"(\s|^)" + param + "(\s|$)", rc):
			lista = rc.split()
			lista.remove(param)
			rc = string.join(lista, ' ')
	elif separator == ';':
		if re.search(r"" + param, rc):
			lista = re.split(';*', rc.replace(' ', ''))
			lista.remove(param)
			rc = string.join(lista, ';')
	return rc

def procFile(path, file, option, disableInlineExpansion = False):
	pathall = path + '\\' + file
	dom2 = xml.dom.minidom.parse(pathall)

	if option == "FULL_RELEASE":
		change_to_release(dom2, disableInlineExpansion)
	elif option == "FULL_DEBUG":
		change_to_debug(dom2)

	f = open(pathall, "w")	
	f.write(dom2.toxml('UTF-8'))
	f.close()

def change_to_release(dom2, disableInlineExpansion = False):
	"""Altera o dom para FULL RELEASE
	
	Keyword arguments:
	dom -- o documento xml do bpk/bpr
	disableInlineExpansion -- 	 eh um parametro para ativar essa opcao de 
		compilacao foi criado inicialmente para fazer uma release com apenas 
		essa opcao habilitada, pois existem alguns pacotes do Gemini que 
		necessitam de dar disable nesta opcao para funcionar corretamente 
		(default False)
	 
	"""
	no = dom2.getElementsByTagName("MACROS")[0]	
	childs = no.childNodes
	for node in childs:
		if node.nodeType == node.ELEMENT_NODE:
			if node.nodeName == 'USERDEFINES':
				rc = node.attributes.values()[0].value
				node.attributes.values()[0].value = remove_param(rc, '_DEBUG', ';')

	no = dom2.getElementsByTagName("OPTIONS")[0]	
	childs = no.childNodes
	for node in childs:
		if node.nodeType == node.ELEMENT_NODE:
			rc = ''
			if node.nodeName == 'IDLCFLAGS':
				rc = remove_param(node.attributes.values()[0].value, '-D_DEBUG')
			elif node.nodeName == 'CFLAG1': 
				rc = replace_param(node.attributes.values()[0].value, '-Od', '-O2')
				rc = replace_param(rc, '-k', '-k-')
				
				if disableInlineExpansion:
					rc = replace_param(rc, '-vi', '-vi-')
				else:
					rc = replace_param(rc, '-vi-', '-vi')
					
				for param in ['-r-', '-y', '-v']:
					rc = remove_param(rc, param)
			elif node.nodeName == 'PFLAGS':
				rc = replace_param(node.attributes.values()[0].value, '-$Y+', '-$Y-')
				rc = replace_param(rc, '-$W', '-$L-')
				rc = replace_param(rc, '-$O-', '-$D-')
			elif node.nodeName == 'AFLAGS':
				rc = replace_param(node.attributes.values()[0].value, '/zi', '/zn')
			elif node.nodeName == 'LFLAGS':
				rc = remove_param(node.attributes.values()[0].value, '-v')
			if rc:
				node.attributes.values()[0].value = rc

def change_to_debug(dom2):
	no = dom2.getElementsByTagName("MACROS")[0]	
	childs = no.childNodes
	for node in childs:
		if node.nodeType == node.ELEMENT_NODE:
			if node.nodeName == 'USERDEFINES':
				rc = node.attributes.values()[0].value
				node.attributes.values()[0].value = add_param(rc, '_DEBUG', ';')

	no = dom2.getElementsByTagName("OPTIONS")[0]	
	childs = no.childNodes
	for node in childs:
		if node.nodeType == node.ELEMENT_NODE:
			rc = ''
			if node.nodeName == 'IDLCFLAGS':
				rc = add_param(node.attributes.values()[0].value, '-D_DEBUG')
			elif node.nodeName == 'CFLAG1':
				rc = replace_param(node.attributes.values()[0].value, '-O2', '-Od')
				rc = replace_param(rc, '-k-', '-k')
				rc = replace_param(rc, '-vi', '-vi-')
				for param in ['-r-', '-y', '-v']:
					rc = add_param(rc, param)
			elif node.nodeName == 'PFLAGS':
				rc = replace_param(node.attributes.values()[0].value, '-$Y-', '-$Y+')
				rc = replace_param(rc, '-$L-', '-$W')
				rc = replace_param(rc, '-$D-', '-$O-')
			elif node.nodeName == 'AFLAGS':
				rc = replace_param(node.attributes.values()[0].value, '/zn', '/zi')
			elif node.nodeName == 'LFLAGS':
				rc = add_param(node.attributes.values()[0].value, '-v')
			if rc:
				node.attributes.values()[0].value = rc
