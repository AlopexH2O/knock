import subprocess
import os
import re
import stat
#import shutil

def unzip_file(filepath, destpath = "./", filesign = "*", unzip_type = 'e', pathof7z = "7z"):
	'''
	description: this func is made to use 7z tool to extact .zip/.7z file
	input:
	1) filepath : the source file abs name
	2) despath  : the destion file path
	3) filesign : the specified file sign or type
	4) unzip_type:  'e' -> extact the file to the destpath totally
	                'x' -> extact the filetree to the destpath
	5) pathof7z : the specified path of 7z.exe, 
	'''

	if not os.path.isfile(filepath):
		return -1, "Error in fileinput"
	if not os.path.isdir(destpath):
		return -2, "Error in destpath"
	if unzip_type not in ['e', 'x']:
		return -3, "Error unzip_type! Choose in ['e', 'x']"

	#cmd = r"7z e -y " + filepath + r" -o" + destpath + r" " + filesign + r" -r"
	cmd = r"{4} {0} -y {1} -o{2} {3} -r".format(unzip_type, filepath, destpath, filesign, pathof7z)
	p = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
	try:
		out, err = p.communicate(timeout = 15)
	except TimeoutExpired:
		p.kill()
		out, err = p.communicate()
		res = p.returncode
		return res, err
	#check the destpath
	res = p.returncode
#	if os.path.exists(destpath):
#		for root, dirs, filename in os.walk(os.path.abspath(destpath)):
#			for i in filename:
#				file_list.append(os.path.join(root, i))
	return res, err

def uapcar_file(exepath, filename):
	'''
	Description: this function is meant to decompress the *bin type file
	exepath: the path of uapcar.exe
	filename : the destname
	'''
	if not os.path.isfile(exepath):
		return -1, "Error : wrong exepath! {0}".format(exepath)
	if os.path.basename(exepath) != 'uapcar.exe':
		return -1, "Error : wrong exepath! {0}".format(exepath)
	if not os.path.isfile(filename):
		return -2, "Error : wrong dest filename! {0}".format(filename)
	if not os.path.splitext(os.path.basename(filename)):
		return -2, "Error : wrong dest filename! {0}".format(filename)
	if not os.path.exists(exepath):
		return -3, "Error : no exefile found! {0}".format(exepath)
	if not os.path.exists(filename):
		return -3, "Error : no dest bin file found! {0}".format(filename)
	
	cmd = r"{0} {1}".format(exepath, filename)
	p = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
	try:
		out, err = p.communicate(timeout = 30)
	except TimeoutExpired:
		p.kill()
		out, err = p.communicate()
		res = p.returncode
		return res, err, file_list

	#check the destpath
	res = p.returncode

	#check the file
	basedir = os.path.dirname(exepath)
	if not os.path.exists(os.path.join(basedir + "\\downlist")):
		res = -4
	return res, err


def find_special(filelist, sign):
	p = re.compile(sign)
	return list(filter(p.search, filelist))

def list_file(filepath = r'./', sign = '-rf'):
	filelist = []
	if not os.path.exists(filepath):
		print("Error(func_list_file): cannot find {0}".format(filepath))
		return filelist
	if sign == '-rf':
		for root, _, files in os.walk(filepath):
			for i in files:
				filelist.append(os.path.join(root, i))
	elif sign == '-f':
		for i in os.listdir(filepath):
			fl = os.path.join(filepath, i)
			if os.path.isfile(fl):
				filelist.append(fl)
	#	filelist = os.listdir(filepath)
	else:
		print("Error in filesign, please choose between [-rf, -f]")
	return filelist
		

def set_readable(filepath):
	if not os.path.exists(filepath):
		return -1
	if not os.path.isdir(filepath):
		return -1
	for root, _, files in os.walk(filepath):
		for f in files:
			os.chmod(os.path.join(root, f), stat.S_IWRITE)
	return 0


def bcompare(exepath, leftfile, rightfile, reportfile = './report.txt'):
	if not os.path.exists(leftfile):
		print("Error: no leftfile of {0}".format(leftfile))
		return -1, []
	if not os.path.isfile(rightfile):
		print("Error: no rightfile of {0}".format(rightfile))
		return -1, []
	report = os.path.abspath(reportfile)
	left = os.path.abspath(leftfile)
	right = os.path.abspath(rightfile)
	dirname = os.path.dirname(report)
	batch = os.path.join(dirname, "batch.txt")

	content = "file-report layout:summary options:display-mismatches,line-numbers output-to:{0} output-options:wrap-word  {1} {2}".format(report, left, right)
	with open(batch, 'w') as fb:
		fb.write(content)
	fb.close()


	cmd = "{0} @{1}".format(exepath, batch)
	p = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
	try:
		out, err = p.communicate(timeout = 120)
	except TimeoutExpired:
		p.kill()
		out, err = p.communicate()
		res = p.returncode
		return res, err
	#check the destpath
	res = p.returncode	

	return res, err

def makehex(exepath):
	"""
	在view_src目录下寻找make.bat和makefile文件,自动编译生成hex文件
	"""
	if not os.path.exists(exepath):
		print("Error[func makehex]: Cannot find {0}".format(exepath))
		exit()
	if not os.path.isdir(exepath):
		print("Error[func makehex]: Not a directory! {0}".format(exepath))
		exit()
	cmdmake = "make.bat"
	makefile = "makefile"
	_bat_found = False
	_file_found = False
	for str in os.listdir(exepath):
		if str.lower() == makefile:
			_file_found = True
			makefile = str
			continue
	if not _file_found:
		print("Error[func makehex]: File missing {0}".format(makefile))
		exit()
	#check makefile
	check_makefile(os.path.join(exepath, makefile))

	#make the hex
	#cmd = os.path.join(os.path.abspath(exepath), cmdmake)
	cmd_cls = "gmake-378.exe clean"
	cmd_make = "gmake-378.exe make"
	#更变编译目录
	os.chdir(exepath)
	print(os.getcwd())
	#执行clean
	print("make clean ...")
	res1 = subprocess.call(cmd_cls, shell = True)
	if res1 != 0:
		print("Error[func exepath]: subprocess.call {0}".format(cmd_cls))
		return -1
	print("make hex ...")
	res = subprocess.call(cmd_make, shell = True)
	if res != 0:
		print("Error[func exepath]: subprocess.call {0}".format(cmd_cls))
		return -1
	
	return res

def check_makefile(filepath):
#	_tag = r'((\.){2}[/\\]){4}uapc_releaseR'
#	_tag_se = r'((\.){2}[/\\])+uapc_releaseR'
	_tag = r'((\.){2}[/\\]){4}uapc_releaseR'
	_tag_se = r'((\.){2}[/\\])+uapc_release.2'
	_rpel = "..\\..\\..\\..\\uapc_releaseR2"
	_bak = filepath+ "_bak"
	_p = re.compile(_tag)
	_p_se = re.compile(_tag_se)

	with open(filepath, 'r') as _fd:
		_content = _fd.read()
	res = re.search(_p, _content)
#	print(res)
	if res:
		print("Log[func {0}]: Success in checking Makefile {1}".format(check_makefile.__name__, filepath))
		return
	#系统目录不对
	print("Warning[func {0}]: Something wrong in {1}".format(check_makefile.__name__, filepath))
	print(re.search(_p_se, _content))
	if re.search(_p_se, _content):
		#目录层次问题
		_content = re.sub(_tag_se, _rpel, _content)
		#备份文件，重写makefile
		#shutil.copy(filepath, _bak)
		print("Log[func {0}]: Rename Makefile. From {1} to {2}".format(check_makefile.__name__, filepath, _bak))
		os.rename(filepath, _bak)
		with open(filepath, 'w') as fw:
			fw.write(_content)
			return
	return


def clearcase_mkbl(view, tag):
	"""
	mkbl 
	"""
	err = ""
	if not os.path.exists(view):
		print("Error[func {0}]: Cannot find the view - {1}".format(clearcase_mkbl.__name__, view))
		return -1, "View doesn't exist!"
	if not os.path.isdir(view):
		print("Error[func {0}]: Cannot find the view - {1}".format(clearcase_mkbl.__name__, view))
		return -1, "View isn't a directory!"
	now = os.getcwd()
	dest = os.path.dirname(view)
	view_name = os.path.basename(view)

	print("pwd = {0}\ndest = {1}\nview_name = {2}".format(now, dest, view_name))
	
	print("Log[func clearcase_mkbl]: Changedir to {0}".format(dest))
	os.chdir(dest)  #切换至view目录

	cmd = "cleartool mkbl -all -full -identical -view {0} {1}".format(view_name, tag)
	out = subprocess.check_output(cmd, shell=True).decode('gb2312')
	print(out)

	os.chdir(now) #返回之前目录
	return 0, ""












if __name__ == '__main__':
	file = r"G:\PCS_PROJECT\_TEST\PCS_992_TEST\src\MASTER1151\Makefile"
	dest = r"G:\PCS_PROJECT\_TEST\PCS_992_TEST\report1.txt"
	sign = r"G:\PCS_PROJECT\_TEST\PCS_992_TEST\rr.txt"
	ztype = r'r'
	#res ,err = bcompare('BCompare.exe', file, dest, sign)
	#res  = makehex(r"G:\PCS_PROJECT\_TEST\PCS_992_TEST\src\MASTER1151")
	check_makefile(file)
	#print("res = ", res)
	

