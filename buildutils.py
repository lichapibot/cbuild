import os
from utils import create_dir
from utils import write_string_to_file
from utils import load_yaml
from utils import dump_yaml
import datetime
import re
import time

DEFAULTS_PATH = "defaults.yml"

DEFAULT_RATING = 1500
DEFAULT_PLAYER = "?"

TAG_REGEX = re.compile(r"^\[([A-Za-z0-9_]+)\s+\"(.*)\"\]\s*$")

def env_path(env):
	return os.path.join("envs",env)

def zip_path(env):
	return os.path.join(env_path(env),"zip")

def source_path(env):
	return os.path.join(env_path(env),"source")

def filtered_path(env):
	return os.path.join(env_path(env),"filtered")

def book_path(env):
	return os.path.join(env_path(env),"book")

def config_path(env):
	return os.path.join(env_path(env),"config.yml")

def filter_logic_path(env):
	return os.path.join(env_path(env),"filter_logic.py")

def default_config():
	return ""

def default_filter_logic():
	return ""

def create_env(env, force):
	create_dir("envs")
	create_dir(env_path(env))
	create_dir(zip_path(env))
	create_dir(source_path(env))
	create_dir(filtered_path(env))
	create_dir(book_path(env))
	write_string_to_file(config_path(env), default_config(), force)
	write_string_to_file(filter_logic_path(env), default_filter_logic(), force)

def load_defaults():
	return load_yaml(DEFAULTS_PATH)

def dump_defaults(defaults):
	dump_yaml(DEFAULTS_PATH, defaults)

def get_next_lichess_db_name(path, variant):
	now = datetime.datetime.now()		
	year = now.year
	month = now.month - 2

	names = sorted(list(os.listdir(path)))

	if len(names) > 0:
		last = names[0]
		parts = last.split("_rated_")
		if len(parts) > 1:
			parts2 = parts[1].split(".")
			parts3 = parts2[0].split("-")
			try:
				year = int(parts3[0])
				month = int(parts3[1]) - 1
			except:
				pass

	if month <= 0:
		month = 12
		year -= 1

	return "lichess_db_{}_rated_{}-{:02d}.pgn.bz2".format(variant, year, month)

def get_lichess_db_url(variant, name):
	return "https://database.lichess.org/{}/{}".format(variant, name)

class BasePgnVisitor():
	def __init__(self):
		self.cnt = 0
		self.headers = {}
		self.pgn = ""
		self.created = time.time()
		pass

	def get_prop_int(self, prop, default):
		try:
			value = int(self.headers[prop])
			return value
		except:
			return default

	def get_prop_str(self, prop, default):
		if prop in self.headers:
			return self.headers[prop]
		return default

	def get_white_elo(self):
		return self.get_prop_int("WhiteElo", DEFAULT_RATING)

	def get_black_elo(self):
		return self.get_prop_int("BlackElo", DEFAULT_RATING)

	def get_min_elo(self):
		return min(self.get_white_elo(), self.get_black_elo())

	def get_white(self):
		return self.get_prop_str("White", DEFAULT_PLAYER)

	def get_black(self):
		return self.get_prop_str("Black", DEFAULT_PLAYER)

	def process(self):
		pass

	def show_info():
		pass

	def process_raw(self, header_lines, move_lines):		
		self.cnt+=1

		self.headers = {}
		self.pgn = ""

		for line in header_lines:
			tag_match = TAG_REGEX.match(line)
			if tag_match:
				self.headers[tag_match.group(1)] = tag_match.group(2)

		self.pgn = "\n".join(header_lines) + "\n" + "\n".join(move_lines)

		elapsed = time.time() - self.created

		rate = 0

		if elapsed > 0:
			rate = self.cnt / elapsed		

		self.process()

		if self.cnt % 10000 == 0:
			print("completed {:8d} , elapsed {:8d} , games / sec {:12.2f}".format(self.cnt, int(elapsed), rate))
			self.show_info()
		

def visit_pgn_file(path, visitor = BasePgnVisitor()):
	print("visiting pgn file {}".format(path))

	parse_start = True
	parse_header = False
	parse_moves_start = False
	parse_moves = False
	header_lines = []
	move_lines = []
	for line in open(path):		
		sline = line.rstrip("\r\n")		
		firstchar = None
		if len(sline) > 0:
			firstchar = sline[0]
		if parse_start:
			if firstchar == "[":
				header_lines.append(sline)
				parse_start = False
				parse_header = True
		elif parse_header:
			if not firstchar == "[":
				parse_header = False
				parse_moves_start = True
			else:
				header_lines.append(sline)
		elif parse_moves_start:
			if len(sline) > 0:
				parse_moves_start = False
				parse_moves = True
				move_lines.append(sline)
		elif parse_moves:
			if len(sline) == 0:
				parse_moves = False
				parse_start = True
				visitor.process_raw(header_lines, move_lines)
				header_lines = []
				move_lines = []
			else:
				move_lines.append(sline)