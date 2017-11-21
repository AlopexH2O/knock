import subprocess
import os

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
	file_list = []

	if not os.path.isfile(filepath):
		return -1, "Error in fileinput", file_list
	if not os.path.isdir(destpath):
		return -2, "Error in destpath", file_list
	if unzip_type not in ['e', 'x']:
		return -3, "Error unzip_type! Choose in ['e', 'x']", file_list

	#cmd = r"7z e -y " + filepath + r" -o" + destpath + r" " + filesign + r" -r"
	cmd = r"{4} {0} -y {1} -o{2} {3} -r".format(unzip_type, filepath, destpath, filesign, pathof7z)
	p = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
	try:
		out, err = p.communicate(timeout = 15)
	except TimeoutExpired:
		p.kill()
		out, err = p.communicate()
		res = p.returncode
		return res, err, file_list

	#check the destpath
	res = p.returncode

	if os.path.exists(destpath):
		for root, dirs, filename in os.walk(os.path.abspath(destpath)):
			for i in filename:
				file_list.append(os.path.join(root, i))
	return res, err, file_list

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





if __name__ == '__main__':
	file = r"G:\PCS_PROJECT\_TEST\PCS_992_TEST\uapcar.exe"
	dest = r"G:\PCS_PROJECT\_TEST\PCS_992_TEST\dest\Milagr.bin"
	sign = r"*.txt"
	ztype = r'r'
	a, b = uapcar_file(file, dest)
	print("a = ", a)
	print("b = ", b)
