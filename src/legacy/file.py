# -*- coding: UTF-8 -*-
import os
import string
import re
import stat
import legacy.futil as futil
import legacy.makefile as mkfile
import codecs


class BuilderFile:
	file = None
	buff = []

	def __init__(self, path):
		self.path = mkfile.find_type_project_path(path)
		if self.path is None:
			raise Exception, 'Erro ao incializar BuilderFile'		
	
	def open(self):
		os.chmod(self.path, stat.S_IWRITE)
		self.file = codecs.open(self.path, 'r+', "utf-8")
		self.buff = self.file.readlines()
		
	def close(self):
		if self.file is not None:
			self.file.close()
		self.buff = None
	
	def salvar(self):
		self.file.seek(0)		
		#Limpa o arquivo para evitar que algum lixo apareca no mesmo
		self.file.truncate(0)
		self.file.writelines(self.buff)		
	
	def setInfo(self, key, val):
		if self.buff == [] :
			raise Exception, 'Arquivo ' + self.path + ' ' + 'esta vazio!'

		if key == "FileVersion":
			self.setFileVersion(val)
		elif key == "ProductVersion":
			self.setProductVersion(val)
		elif key == "Version":
			self.setVersion(val)

	
	def getInfo(self, key):
		if self.buff == [] :
			raise Exception, 'Arquivo ' + self.path + ' ' + 'esta vazio!'
		
		out = ""

		#TODO: refactory abaixo, eliminaria esses if's 
		if key == "FileVersion":
			out = self.getFileVersion()
		elif key == "ProductVersion":
			out = self.getProductVersion()
		elif key == "Version":
			out = self.getVersion()
		elif key == "FileDescription":
			out = self.getFileDescription()
		elif key == "ProductName":
			out = self.getProductName()

		return out.strip();

	def getVersion(self):
		majorVer = ""
		minorVer = ""
		releaseVer = ""
		buildVer = ""

		for x in range(len(self.buff)):
			if re.match('^MajorVer=',self.buff[x],1) :
				majorVer = string.split(self.buff[x], '=')[1]
			elif re.match('^MinorVer=',self.buff[x],1) :
				minorVer = string.split(self.buff[x], '=')[1]
			elif re.match('^Release=',self.buff[x],1) :
				releaseVer = string.split(self.buff[x], '=')[1]
			elif re.match('^Build=',self.buff[x],1) :
				buildVer = string.split(self.buff[x], '=')[1]
				break

		majorVer = futil.elimina_enter_line(majorVer)
		minorVer = futil.elimina_enter_line(minorVer)
		releaseVer = futil.elimina_enter_line(releaseVer)
		buildVer = futil.elimina_enter_line(buildVer)
		return majorVer + "." + minorVer + "." + releaseVer + "." + buildVer

	#TODO: Refatorar esses metodos para pegar o parametro da regex como parametro do 
	#metodo, generalizando-os. (getProductVersion, getFileVersion)
	'''Metodo pra pegar a FileDescription do BPK/R necessario para gerar o .RC'''
	def getFileDescription(self):		
		for x in range(len(self.buff)):
			if re.match('^FileDescription=',self.buff[x],1) :
				fileDescription = string.split(self.buff[x], '=')
				return futil.elimina_enter_line(fileDescription[1])
			
	def getProductName(self):		
		for x in range(len(self.buff)):
			if re.match('^ProductName=',self.buff[x],1) :
				productName = string.split(self.buff[x], '=')
				return futil.elimina_enter_line(productName[1])
			
	def getProductVersion(self):		
		for x in range(len(self.buff)):
			if re.match('^ProductVersion=',self.buff[x],1) :
				productVer = string.split(self.buff[x], '=')
				return futil.elimina_enter_line(productVer[1])

	
	def getFileVersion(self):
		for x in range(len(self.buff)):
			if re.match('^FileVersion=',self.buff[x],1) :
				fileVer = string.split(self.buff[x], '=')
				return futil.elimina_enter_line(fileVer[1])

	def setVersion(self, val):
		aversao = string.split(val, '.')
		
		majorVer = aversao[0]
		minorVer = aversao[1]
		releaseVer = aversao[2]
		buildVer = aversao[3]

		for x in range(len(self.buff)):
			if re.match('^MajorVer=',self.buff[x],1) :
				self.buff[x] = 'MajorVer=' + majorVer + '\n'
			elif re.match('^MinorVer=',self.buff[x],1) :
				self.buff[x] = 'MinorVer=' + minorVer + '\n'
			elif re.match('^Release=',self.buff[x],1) :
				self.buff[x] = 'Release=' + releaseVer + '\n'
			elif re.match('^Build=',self.buff[x],1) :
				self.buff[x] = 'Build=' + buildVer + '\n'
				break
			
	
	def setProductVersion(self, val):		
		for x in range(len(self.buff)):
			if re.match('^ProductVersion=',self.buff[x],1) :
				self.buff[x] = 'ProductVersion=' + val + '\n'
	
	def setFileVersion(self, val):
		for x in range(len(self.buff)):
			if re.match('^FileVersion=',self.buff[x],1) :
				self.buff[x] = 'FileVersion=' + val + '\n'
