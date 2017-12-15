import os
import sys
import shutil
import json
import re
import time
from autocheck import detectfile


def check_src_dir(src):
	link = os.path.join(src, 'link')
	obj = os.path.join(src, "obj")
	header = os.path.join(src, "src")

	if not os.path.exists(header):
		print("WARNING: Cannot Find {0}".format(header))
		return -1
	if not os.path.exists(link):
		print("WARNING: Creating dir {0}".format(link))
		os.mkdir(link)
	if not os.path.exists(obj):
		print("WARNING: Creating dir {0}".format(obj))
		os.mkdir(obj)
	return 0

def get_master1151(view):
	if not os.path.exists(view):
		print("Error[func {0}]: view dont exist! - {1}".format(get_master1151.__name__, view))
		return None
	if not os.path.isdir(view):
		print("Error[func {0}]: view isnt a directory! - {1}".format(get_master1151.__name__, view))
		return None
	for _root, _dirs, _ in os.walk(view):
		for _d in _dirs:
			if _d == "MASTER1151":
				return os.path.join(_root, _d)
	return None

def check_success(filepath):
	if not os.path.exists(filepath):
		print("Error: failed to find {0}".format(filepath))
		return False
	result = False
	with open(filepath, 'r') as fd:
		content = fd.read()
	p = re.compile("\d+ important difference line")
	res = p.search(content)
	result = (int(res.group().split()[0]) == 1)
	return result

def remove_dir(filepath):
	if not os.path.exists(filepath):
		print("Error[func remove_dir]: directory not found {0}".format(filepath))
		return
	for i in os.listdir(filepath):
		tmp = os.path.join(filepath, i)
		if os.path.isdir(tmp):
			print("## remove dir {0}".format(tmp))
			shutil.rmtree(tmp)
			continue
		if os.path.isfile(tmp):
			if os.path.basename(tmp).lower() == "uapcar.exe":
				continue
			if os.path.basename(tmp).lower() == "qt-mt338.dll":
				continue
			if os.path.basename(tmp).lower() == "生产文件.7z":
				continue
			print("## remove file {0}".format(tmp))
			os.remove(tmp)
	return

#清理战场
def proc_clear_battle_field(project):
	print("log[func {0}]: Clean the battle field - {1}".format(proc_clear_battle_field.__name__, project))
	time.sleep(2)
	remove_dir(project)

#复制MASTER1151目录
def proc_copy_master1151(src, dest):
	#复制文件
	if not os.path.exists(src):
		print("Error[func {0}]: {1} don't exist! Please Check!".format(proc_copy_master1151.__name__, src))
		exit()
	if not os.path.exists(dest):
		print("Log[func {2}]: Copying master1151 \n\t{0}\n\t to \n\t{1}".format(src, dest, proc_copy_master1151.__name__))
		shutil.copytree(src, dest)
	else:
		print("WARNING[func {0}]: {1} already exist! Please Check!".format(proc_copy_master1151.__name__, dest))
		con = input("Whether to Continue?[y/n]?")
		if con == "n":
			print("ByeBye...")
			exit()


	#设置文件可读写
	detectfile.set_readable(dest)
	#查看MASTER1151
	res = check_src_dir(dest)
	if res < 0:
		print("Error: File dump in src dir!!")
		exit()
	return

#解压生产文件获得hex
def proc_handle_hex(dest, project, zipcmd, uapcmd):
	print("Log[func {0}] handle 生产文件：\n\t{1}".format(proc_handle_hex.__name__, dest))
	print("Log[func {0}] unzip_file ...".format(proc_handle_hex.__name__))
	res, err = detectfile.unzip_file(dest, project, "*.bin", 'e')
	if res != 0:
		print("Error[func {0}] Failed in unzip_file: {1}".format(proc_handle_hex.__name__, dest))
		print("err = ", err)
		exit()

	print("Log[func {0}] search bin file ...".format(proc_handle_hex.__name__))
	#搜索bin文件
	bin_file = detectfile.find_special(detectfile.list_file(project, '-f'), '\.[bB][iI][nN]$')
	if len(bin_file) == 0:
		print("Error[func {0}] found no bin file!".format(proc_handle_hex.__name__))
		exit()
	for i in bin_file:
		print("Log[func {0}] uapcar bin file ...".format(proc_handle_hex.__name__))
		detectfile.uapcar_file(uapcmd, i)
	return

#自动编译hex
def proc_make_hex(project):
	print("Log[func {0}] making hex file ...".format(proc_make_hex.__name__))
	res = detectfile.makehex(project)
	if res != 0:
		print("Error[func {0}] Failed in making hex!".format(proc_make_hex.__name__))
		exit()

def proc_compare(project, src):
	BIN_NR1151 = detectfile.find_special(detectfile.list_file(os.path.join(project, "downlist"), '-f'), "_NR1151\.[hH][eE][xX]$")
	SRC_NR1151 = detectfile.find_special(detectfile.list_file(src, '-f'), "NR1151\.[hH][eE][xX]$")
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
		print("=======================================================================================")
		print("*         ####                  ###       ###    ########     ####       ####         *")
		print("*        #    #   #       #    #   #     #   #   #           #    #     #    #        *")
		print("*       #      #  #       #   #     #   #     #  #          #      #   #      #       *")
		print("*        #        #       #  #         #         #           #          #             *")
		print("*         #       #       #  #         #         #            #          #            *")
		print("*          #      #       #  #         #         # #####       #          #           *")
		print("*           #     #       #  #         #         #              #          #          *")
		print("*            #    #       #  #         #         #               #          #         *")
		print("*      #      #   #       #   #     #   #     #  #         #      #   #      #        *")
		print("*       #    #     #     #     #   #     #   #   #          #    #     #    #         *")
		print("*        ####       #####       ###       ###    ########    ####       ####          *")
		print("=======================================================================================")
	else:
		print("=======================================================================================")
		print("*       #########       ###       ##   ##          #       #  #####       ########    *")
		print("*       #              #  #       ##   ##          #       #  #     #     #           *")
		print("*       #             #    #           ##          #       #  #      #    #           *")
		print("*       #            #      #     ##   ##          #       #  #     #     #           *")
		print("*       #######     ## # # # #    ##   ##          #       #  ######      #           *")
		print("*       #          #          #   ##   ##          #       #  #     #     # #####     *")
		print("*       #         #            #  ##   ##          #       #  #      #    #           *")
		print("*       #        #              # ##   ##          #       #  #       #   #           *")
		print("*       #        #              # ##   ##           #     #   #        #  #           *")
		print("*       #        #              # ##   ##########    #####    #         # ########    *")
		print("=======================================================================================")
	return res#返回是否成功True or False



def main():
	"""
		命令行参数:
		-all : 全流程执行
		-cls ：首先清除project目录其他文件
		-cp  ：拷贝view中MASTER1151文件夹
		-bin ：解压生产文件获取并拆分bin文件
		-make：通过makefile生成hex文件
		-comp：hex文件比对
		-mkbl: 打标签
		-help：命令行帮助
	"""
	_conf = {"-all":False, "-cls":False, "-cp":False, "-bin":False, "-make":False, "-comp":False, "-mkbl":False, "-help":False}
	for ar in sys.argv[1:]:
		if ar in _conf:
			_conf[ar] = True
	
	if _conf["-help"]:
		#help参数
		print(main.__doc__)
		return
	if _conf["-all"]:
		_conf["-cls"]  = True
		_conf["-cp"]   = True
		_conf["-bin"]  = True
		_conf["-make"] = True
		_conf["-comp"] = True
		_conf["-mkbl"] = True

	with open('setup.json', 'r', encoding = 'utf-8') as fin:
		setinfo = json.load(fin)
	view = setinfo['view']
	project = setinfo['project']
	production = setinfo['production']
	p7z = setinfo['p7z']
	pUapcar = setinfo['pUapcar']
	view_tag = setinfo['tag']

	prod = os.path.join(project, production)#生产文件全地址
	#view_src = os.path.join(view, "PCS_SYS_PROT\\PCS-992\\src\\MASTER1151")
	#view_src = get_master1151(os.path.join(view, "PCS_SYS_PROT\\PCS-992\\src"))
	proj_src = os.path.join(project, "src\\MASTER1151")

	succ = False

	if _conf["-cls"]:
		#清理战场
		proc_clear_battle_field(project)
	if _conf["-cp"]:
		#复制master1151目录
		view_src = get_master1151(os.path.join(view, "PCS_SYS_PROT\\PCS-992\\src"))
		proc_copy_master1151(view_src, proj_src)
	if _conf["-bin"]:
		#生产文件处理
		proc_handle_hex(prod, project, p7z, pUapcar)
	if _conf["-make"]:
		proc_make_hex(proj_src)
	
	if _conf["-comp"]:
		succ = proc_compare(project, proj_src)
		if not succ:#文件比对失败
			exit()

	if _conf["-mkbl"]:
			#文件比对成功，开始询问是否需要打标签
		print("Asking: Mkbl the view - {0} - {1}".format(view, view_tag))
		yes_no = input("Yes or No [y/n]? Your Choice: ")

		if yes_no.lower() == "yes" or yes_no.lower() == "y":
			print("hahahah")
			detectfile.clearcase_mkbl(view, view_tag)
		else:
			print("ByeBye...")


		



if __name__ == '__main__':

	main()
	exit()

	with open('setup.json', 'r', encoding = 'utf-8') as fin:
		setinfo = json.load(fin)
	view = setinfo['view']
	project = setinfo['project']
	production = setinfo['production']
	p7z = setinfo['p7z']
	pUapcar = setinfo['pUapcar']
	view_tag = setinfo['tag']

	prod = os.path.join(project, production)#生产文件全地址
	#view_src = os.path.join(view, "PCS_SYS_PROT\\PCS-992\\src\\MASTER1151")
	view_src = get_master1151(os.path.join(view, "PCS_SYS_PROT\\PCS-992\\src"))
	proj_src = os.path.join(project, "src\\MASTER1151")

	#清理战场
	proc_clear_battle_field(project)
	#复制master1151目录
	proc_copy_master1151(view_src, proj_src)
	#生产文件处理
	proc_handle_hex(prod, project, p7z, pUapcar)
	#自动编译
	proc_make_hex(proj_src)
	#文件比对
	succ = proc_compare(project, proj_src)

	#打标签处理
	if not succ:#文件比对失败
		exit()
	#文件比对成功，开始询问是否需要打标签
	print("Asking: Mkbl the view - {0}".format(view))
	yes_no = input("Yes or No [y/n]? Your Choice: ")

	if yes_no.lower() == "yes" or yes_no.lower() == "y":
		print("hahahah")
		detectfile.clearcase_mkbl(view, view_tag)
	else:
		print("ByeBye...")

	#清理战场
	#proc_clear_battle_field(project)
	





