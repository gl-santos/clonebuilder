# -*- coding: UTF-8 -*-
#import wx
import string
import re
import glob
import os
import stat
import sys

#class AltVerFrame(wx.Dialog):
#	def __init__(
#			self, parent, ID, title, size=wx.DefaultSize, pos=wx.DefaultPosition, 
#			style=wx.DEFAULT_DIALOG_STYLE
#			):

#		# Instead of calling wx.Dialog.__init__ we precreate the dialog
#		# so we can set an extra style that must be set before
#		# creation, and then we create the GUI dialog using the Create
#		# method.
#		pre = wx.PreDialog()
#		pre.Create(parent, ID, title, pos, size, style)

#		# This next step is the most important, it turns this Python
#		# object into the real wrapper of the dialog (instead of pre)
#		# as far as the wxPython extension is concerned.
#		self.PostCreate(pre)

#		sizer = wx.BoxSizer(wx.VERTICAL)
#		box = wx.BoxSizer(wx.HORIZONTAL)

#		label = wx.StaticText(self, -1, "Versao:")
#		box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

#		self.text = wx.TextCtrl(self, -1, "9.2.3.4", size=(80,-1))
#		box.Add(self.text, 1, wx.ALIGN_CENTRE|wx.ALL, 5)		

#		sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

#		box = wx.BoxSizer(wx.HORIZONTAL)

#		sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

#		line = wx.StaticLine(self, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
#		sizer.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 5)

#		btnsizer = wx.StdDialogButtonSizer()

#		if wx.Platform != "__WXMSW__":
#			btn = wx.ContextHelpButton(self)
#			btnsizer.AddButton(btn)

#		btn = wx.Button(self, wx.ID_OK)
#		btn.SetDefault()
#		btnsizer.AddButton(btn)

#		btn = wx.Button(self, wx.ID_CANCEL)
#		btnsizer.AddButton(btn)
#		btnsizer.Realize()

#		sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

#		self.SetSizer(sizer)
#		sizer.Fit(self)

#class VersaoInvalida(Exception):
#	None

class AlteraVer:
	def __init__(self, ver, dir):
		self.ver = ver
		self.dir = dir
		#print ver
		#print dir
#		self.index = 0
#		self.__consitVer()
#		self.__searchDirs()

#	def __consitVer(self):
#		aversao = string.split(self.ver, '.')
#		if len(aversao) is not 4:
#			raise VersaoInvalida, "Versao invalida: " + self.ver

#		for v in aversao:
#			if not v.isdigit():
#				raise VersaoInvalida, "Versao invalida: " + self.ver

	def __apaga_res(self, path) :
		""" Remove arquivo de resource compilado, pois o builder usa esse
		 arquivo em primeiro lugar para ler as informacoes de versao """

		resource = glob.glob(path + '\\' + '*.res')
		for res in resource :
			os.remove(res)

	def __altera_ver(self, path) :
		aversao = string.split(self.ver, '.')
		
		MajorVer = aversao[0]
		MinorVer = aversao[1]
		ReleaseVer = aversao[2]
		BuildVer = aversao[3]
		
		os.chmod(path, stat.S_IWRITE)
		f = open(path, 'r+')
		a = f.readlines()
		
		if a == [] :
			raise Exception, 'Arquivo ' + path + ' ' + 'esta vazio!'
		
		for x in range(len(a)):
			if re.match('^MajorVer=',a[x],1) :
				a[x] = 'MajorVer=' + MajorVer + '\n'
			elif re.match('^MinorVer=',a[x],1) :
				a[x] = 'MinorVer=' + MinorVer + '\n'
			elif re.match('^Release=',a[x],1) :
				a[x] = 'Release=' + ReleaseVer + '\n'
			elif re.match('^Build=',a[x],1) :
				a[x] = 'Build=' + BuildVer + '\n'
			elif re.match('^FileVersion=',a[x],1) :
				a[x] = 'FileVersion=' + self.ver + '\n'
			elif re.match('^ProductVersion=',a[x],1) :
				a[x] = 'ProductVersion=' + self.ver + '\n'
				break
			
		f.seek(0)
		#Limpa o arquivo para evitar que algum lixo apareca no mesmo
		f.truncate(0)
		f.writelines(a)
		f.close()

	
	def __aplica_ver(self, path, tipo) :
		out = None
		for tipo_atual in tipo :
			file  = glob.glob(path + '\\' + tipo_atual)
			if file :
				out = 'Alterando versao: ' + file[0]
				self.__altera_ver(file[0])
				# Para testar todos os tipos em um mesmo diretorio comentar
				# a linha o break
				break 
		return out

#	def __iter__(self):
#		return self

#	def next(self):
#		if self.index >= len(self.dirs):
#			self.index = 0
#			raise StopIteration

	def run(self):
		self.__apaga_res(self.dir)
		out = self.__aplica_ver(self.dir, ['*.bpk', '*.bpr'])
#		self.index = self.index + 1
                #print out
		return out



def main() :
	if (len(sys.argv) < 3):
		print "Erro na quantidade de argumentos use: altver.py 6.4.19.170 c:\\gemini"
	else:
		for dir in AlteraVer(sys.argv[1], sys.argv[2]):
			if dir is not None:
				print dir

if __name__ == '__main__':
	main()
