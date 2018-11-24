import ast
import sys
import astunparse
import sys
import getopt
import glob
import os
import shutil
from config import get_default_config

def main(args):
	current_conf = get_default_config()
	if len(args) < 2:
		raise SystemExit("Please specify a target directory!")
	else:
		target_dir = args[1] if not args[1].endswith("/") else args[1][:-1]
	if len(args) < 3:
		raise SystemExit("Please specify whether to strip (-s) or restore (-r) imports")

	loc_fl = (current_conf["default_mut_dir"] + "/").replace("//","/") + current_conf.get("default_imp_tmp")
	opts, args = getopt.getopt(args[2:], "sr")
	for opt, a in opts:
		if opt == "-s":
			print("Adjusting relative imports...", target_dir, flush=True)
			if os.path.exists(loc_fl):
				os.remove(loc_fl)
			if os.path.exists(target_dir + "_stripped"):
				shutil.rmtree(target_dir + "_stripped")
			shutil.copytree(target_dir, target_dir + "_stripped")
			for fl in glob.iglob(target_dir + "_stripped/**/*.py", recursive=True):
				fl = fl.replace("\\","/")
				strip_and_store_imports(fl, loc_fl)
		elif opt == "-r":
			print("Restoring imports for:", target_dir)
			with open(loc_fl, "r", encoding="UTF-8") as f:
				str_dict_dict = {}
				for _, line in enumerate(f):
					(flp, fld) = eval(line)
					fld = eval(fld)
					str_dict_dict[flp] = fld

			for fl in glob.iglob(target_dir + "/**/*.py", recursive=True):
				fl = fl.replace("\\","/")
				if str_dict_dict.get(fl):
					restore_imports_for_file(fl, str_dict_dict[fl])


def strip_and_store_imports(fl, loc_fl):
	changes = {}
	with open(fl, "r", encoding="UTF-8") as f:
		myast = ast.fix_missing_locations(ast.parse(astunparse.unparse(ast.fix_missing_locations(ast.parse(f.read())))))

	for node in ast.walk(myast):
		if type(node) == ast.ImportFrom:
			if node.level != 0:
				changes[node.lineno] = node.level
				node.level = 0

	with open(fl, "w", encoding="UTF-8") as f:
		f.write(astunparse.unparse(myast))

	if changes:
		with open(loc_fl,"a") as f:
			f.write("(" + repr(fl) + " , " + repr(str(changes)) + ")\n")

def restore_imports_for_file(fl, ln_num_dict):
	with open(fl, "r", encoding="UTF-8") as f:
		myast = ast.fix_missing_locations(ast.parse(f.read()))

	for node in ast.walk(myast):
		if type(node) == ast.ImportFrom:
			if ln_num_dict.get(node.lineno):
				node.level = ln_num_dict[node.lineno]

	with open(fl, "w", encoding="UTF-8") as f:
		f.write(astunparse.unparse(myast))


if __name__ == "__main__":
	main(sys.argv)