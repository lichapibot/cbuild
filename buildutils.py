import os
from utils import create_dir
from utils import write_string_to_file
from utils import load_yaml
from utils import dump_yaml

DEFAULTS_PATH = "defaults.yml"

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

