import os
import shutil
import json
from autocheck import detectfile






if __name__ == '__main__':
	with open('setup.json', 'r', encoding = 'utf-8') as fin:
		setinfo = json.load(fin)
	view = setinfo['view']
	project = setinfo['project']
	production = setinfo['production']
	p7z = setinfo['p7z']
	pUapcar = setinfo['pUapcar']
	print(view)
	print(project)
	print(production)
	print(p7z)
	print(pUapcar)