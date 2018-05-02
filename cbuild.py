import argparse
from utils import create_dir
from utils import write_string_to_file
from buildutils import create_env
from buildutils import load_defaults
from buildutils import dump_defaults
import yaml

#########################################################################
# setup args and defaults

parser = argparse.ArgumentParser(description='Filter PGN files and build a book from them')

parser.add_argument('-e', '--env', help='create / activate build environment')
parser.add_argument('--force', action="append", help='force [ env ]')

args = parser.parse_args()

def get_force(key):
	if not args.force:
		return False
	return key in args.force

defaults = load_defaults()

if not "env" in defaults:
	defaults["env"] = None

print("------")

#########################################################################
# command interpreter

if not args.env is None:
	env = args.env
	print("creating / activating environment {}".format(env))
	create_env(env, get_force("env"))
	print("environment {} created ok".format(env))
	defaults["env"] = env

#########################################################################
# store defaults

dump_defaults(defaults)

print("------\nactive environment > {}".format(defaults["env"]))