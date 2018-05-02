import argparse
from utils import create_dir
from utils import write_string_to_file
from buildutils import create_env

parser = argparse.ArgumentParser(description='Filter PGN files and build a book from them')

parser.add_argument('-e', '--env', help='create build environment')

args = parser.parse_args()

if not args.env is None:
	env = args.env
	print("creating environment {}".format(env))
	create_env(env)	
	print("environment {} created ok".format(env))