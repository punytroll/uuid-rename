import os
import re
import sys
import uuid

uuid_pattern = re.compile("^[0123456789abcdefABCDEF]{8,8}-[0123456789abcdefABCDEF]{4,4}-[0123456789abcdefABCDEF]{4,4}-[0123456789abcdefABCDEF]{4,4}-[0123456789abcdefABCDEF]{12,12}$")
keep_existing = False
verbose = False
recursive = False

def process_directory(directory_path):
	item_names = os.listdir(directory_path)
	for item_name in item_names:
		process_item(os.path.join(directory_path, item_name))

def process_item(item_path):
	if os.path.exists(item_path) == True:
		if keep_existing == False or uuid_pattern.match(os.path.basename(item_path)) == None:
			if os.path.isdir(item_path) == True and recursive == True:
				process_directory(item_path)
			uuid_name = str(uuid.uuid4())
			uuid_path = os.path.join(os.path.dirname(item_path), uuid_name)
			if verbose == True:
				print "Renaming '" + item_path + "'\n      to '" + uuid_path + "'."
			os.rename(item_path, uuid_path)
		else:
			if verbose == True:
				print "Ignoring '" + item_path + "'."
	else:
		if verbose == True:
			print "Item '" + item_path + "' doesn't exist."

for item_name in sys.argv[1:]:
	if item_name == "--keep-existing":
		keep_existing = True
	elif item_name == "--override-existing":
		keep_existing = False
	elif item_name == "--verbose":
		verbose = True
	elif item_name == "--silent":
		verbose = False
	elif item_name == "--recursive":
		recursive = True
	elif item_name == "--not-recursive":
		recursive = False
	else:
		process_item(os.path.abspath(item_name))
