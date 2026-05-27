import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('--db-host', required=True)
parser.add_argument('--db-user', required=True)
parser.add_argument('--db-pass', required=True)
parser.add_argument('--db-name', required=True)
parser.add_argument('--port', type=int, required=True)
args, unknown = parser.parse_known_args()

os.environ['DB_HOST'] = args.db_host
os.environ['DB_USER'] = args.db_user
os.environ['DB_PASS'] = args.db_pass
os.environ['DB_NAME'] = args.db_name
os.environ['APP_PORT'] = str(args.port)

os.execvp('/opt/mywebapp/venv/bin/gunicorn', ['gunicorn', 'main:app'] + unknown)