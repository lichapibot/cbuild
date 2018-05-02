import argparse
from utils import create_dir
from utils import write_string_to_file
from utils import store_url
import buildutils
from buildutils import create_env
from buildutils import load_defaults
from buildutils import dump_defaults
from buildutils import get_next_lichess_db_name
from buildutils import get_lichess_db_url
from buildutils import zip_path
import yaml
import os

#store_url("https://database.lichess.org/atomic/lichess_db_atomic_rated_2018-02.pgn.bz2","envs/atomic/zip/lichess_db_atomic_rated_2018-02.pgn.bz2")

#print(get_next_lichess_db(buildutils.zip_path("atomic"),"atomic"))

#########################################################################
# setup args and defaults

parser = argparse.ArgumentParser(description='Filter PGN files and build a book from them')

parser.add_argument('-e', '--env', help='create / activate build environment')
parser.add_argument('--force', action="append", help='force [ env ]')
parser.add_argument('--variant', action="store", help='variant')
parser.add_argument('--nextlichessdb', action="store_true", help='download next lichess db')

args = parser.parse_args()

print(args)

def get_force(key):
	if not args.force:
		return False
	return key in args.force

defaults = load_defaults()

if not "env" in defaults:
	defaults["env"] = None

env = defaults["env"]

def assert_env():	
	if env is None:
		raise Exception("EnvironmentMissing")

if not args.variant is None:
	defaults["variant"] = args.variant

if not "variant" in defaults:
	defaults["variant"] = "standard"

variant = defaults["variant"]

print("------")

#########################################################################
# command interpreter

if not args.env is None:
	env = args.env
	print("creating / activating environment {}".format(env))
	create_env(env, get_force("env"))
	print("environment {} created ok".format(env))
	defaults["env"] = env
elif args.nextlichessdb:
	assert_env()
	dbname = get_next_lichess_db_name(zip_path(env), variant)
	dburl = get_lichess_db_url(variant, dbname)
	dbpath = os.path.join(zip_path(env), dbname)
	print("retrieving {}".format(dbname))
	store_url(dburl, dbpath)

#########################################################################
# store defaults

dump_defaults(defaults)

print(defaults)

print("------\nactive environment > {}".format(defaults["env"]))