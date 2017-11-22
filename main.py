import os
import shutil
import json
import re
from autocheck import detectfile


def check_src_dir(src):
	mk = os.path.join(src, 'MASTER1151\\make.bat')
	link = os.path.join(src, 'MASTER1151\\link')
	obj = os.path.join(src, "MASTER1151\\obj")
	header = os.path.join(src, "MASTER1151\\src")

	if not os.path.exists(mk):
		return -1
	if not os.path.exists(header):
		return -1
	if not os.path.exists(link):
		os.mkdir(link)
	if not os.path.exists(obj):
		os.mkdir(obj)
	return 0
	
def check_success(filepath):
	if not os.path.exists(filepath):
		print("Error: failed to find {0}".format(filepath))
		return false
	result = false
	with open(filepath, 'r') as fd:
		content = fd.read()
		p = re.compile("\d+ important difference line")
		res = p.search(content)
		result = (int(res.group().split()[0]) == 1)
	return result




if __name__ == '__main__':
	with open('setup.json', 'r', encoding = 'utf-8') as fin:
		setinfo = json.load(fin)
	view = setinfo['view']
	project = setinfo['project']
	production = setinfo['production']
	p7z = setinfo['p7z']
	pUapcar = setinfo['pUapcar']
	
	prod = os.path.join(project, production)#生产文件全地址
	view_src = os.path.join(view, "PCS_SYS_PROT\\PCS-992\\src\\src")
	proj_src = os.path.join(project, "src")
	print("1. Copying Directory:{0} to {1}".format(view_src, proj_src))
	#复制文件
	if os.path.exists(proj_src):
		print("WARNING: {0} already exist! Please Check!".format(proj_src))
		exit()
	if not os.path.exists(view_src):
		print("ERROR: {0} don't exist! Please Check!")
		exit()

	shutil.copytree(view_src, proj_src)
	#设置文件可读写
	detectfile.set_readable(proj_src)
	#查看MASTER1151
	res = check_src_dir(proj_src)
	if res < 0:
		print("Error: File dump in src dir!!")
		exit()


	print("2. unzip_file {0}".format(prod))
	res, err = detectfile.unzip_file(prod, project, "*.bin", 'e')
	print("res = ", res)
	print("err = ", err)

	if res != 0:
		print("Failed in unzip_file")
		exit()

	print("3. uapcar bin file")
	#搜索bin文件
	bin_file = detectfile.find_special(detectfile.list_file(project, '-f'), '\.[bB][iI][nN]$')
	if len(bin_file) == 0:
		print("Error: There is no bin in {0}".format(project))
		exit()
	for i in bin_file:
		print("uapcar file {0}".format(i))
		detectfile.uapcar_file(pUapcar, i)

	print("4. BeyondCompare NR1151.hex")
	BIN_NR1151 = detectfile.find_special(detectfile.list_file(os.path.join(project, "downlist"), '-f'), "_NR1151\.[hH][eE][xX]$")
	SRC_NR1151 = detectfile.find_special(detectfile.list_file(os.path.join(proj_src, "MASTER1151"), '-f'), "NR1151\.[hH][eE][xX]$")
	print("BIN_NR1151 = ", BIN_NR1151)
	print("SRC_NR1151 = ", SRC_NR1151)
	if len(BIN_NR1151) != 1 and len(SRC_NR1151) != 1:
		print("WARNING: Please Check !!!")
		exit()
	report = os.path.join(project, "reprot.txt")
	res, err = detectfile.bcompare("BCompare.exe", SRC_NR1151[0], BIN_NR1151[0], report)
	print("res = ", res)
	print("err = ", err)

	res = check_success(report)
	if res:
		print("Well Done!!")
	else:
		print("Bad Luck!!")
		





