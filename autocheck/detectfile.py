import subprocess
import os

def unzip_file(filepath, destpath = "./", filesign = "*", unzip_type = 'e'):
	'''
	description: this func is made to use 7z tool to extact .zip/.7z file
	input:
	1) filepath : the source file abs name
	2) despath  : the destion file path
	3) filesign : the specified file sign or type
	4) unzip_type:  'e' -> extact the file to the destpath totally
	                'x' -> extact the filetree to the destpath

	'''
	file_list = []

#	if os.path.isfile
	if not os.path.isfile(filepath):
		return -1, "Error in fileinput", file_list
	if not os.path.isdir(destpath):
		return -2, "Error in destpath", file_list
	if unzip_type not in ['e', 'x']:
		return -3, "Error unzip_type! Choose in ['e', 'x']", file_list

	#cmd = r"7z e -y " + filepath + r" -o" + destpath + r" " + filesign + r" -r"
	cmd = r"7z {0} -y {1} -o{2} {3} -r".format(unzip_type, filepath, destpath, filesign)
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




if __name__ == '__main__':
	file = r"G:\PCS_PROJECT\_TEST\PCS_992_TEST\aaa.7z"
	dest = r".\dest"
	sign = r"*.txt"
	ztype = r'r'
	rt, err, content = unzip_file(file, dest, sign, ztype)
	print("rt = ", rt)
	print("err = ", err)
	print("content = ", content)
