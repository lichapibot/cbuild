import os

def create_dir(path):
	if not os.path.exists(path):
		os.makedirs(path)
		print("created directory {}".format(path))
	else:
		#print("{} exists".format(path))
		pass

def write_string_to_file(path,str):
	with open(path,"w") as outfile:
		outfile.write(str)
	print("written file {} ( {} characters )".format(path,len(str)))