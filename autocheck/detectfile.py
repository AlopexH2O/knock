import subprocess
import os

def unzip_file(filepath, destpath = "./", filesign = "*", unzip_type = 'e'):
	#   return value:
	#	res: success(0) or fail
	#   err: error information
	#	file: the dest file list
	#
	file_list = []
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
		ndir = os.path.abspath(destpath)
		flist = os.listdir(ndir)
		for i in flist:
			file_list.append(os.path.join(ndir, i))
	return res, err, file_list




if __name__ == '__main__':
	file = r"G:\PCS_PROJECT\_TEST\PCS_992_TEST\aaa.7z"
	dest = r".\dest"
	sign = r"*.bin"
	rt, err, content = unzip_file(file, dest, sign)
	print("rt = ", rt)
	print("err = ", err.decode())
	print("content = ", content)
