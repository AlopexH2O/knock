import subprocess


def unzip_file(filepath, destpath, filesign):
	cmd = r"7z e " + filepath + r" -o" + destpath + r" " + filesign + r" -r"
	p = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE)
	str = p.stdout.read()
	res = p.wait()
	return res, str



if __name__ == '__main__':
	file = r"G:\PCS_PROJECT\_TEST\PCS_992_TEST\aaa.7z"
	dest = r".\dest"
	sign = r"*.dev"
	rt, content = unzip_file(file, dest, sign)
	print("rt = ", rt)
	print(content.decode())
