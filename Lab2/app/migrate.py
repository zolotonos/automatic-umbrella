import argparse
import pymysql

parser = argparse.ArgumentParser()
parser.add_argument('--db-host', required=True)
parser.add_argument('--db-user', required=True)
parser.add_argument('--db-pass', required=True)
parser.add_argument('--db-name', required=True)
parser.add_argument('--port', type=int)
args, unknown = parser.parse_known_args()

conn = pymysql.connect(
    host=args.db_host,
    user=args.db_user,
    password=args.db_pass
)
cursor = conn.cursor()
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {args.db_name}")
cursor.execute(f"USE {args.db_name}")
cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()
conn.close()