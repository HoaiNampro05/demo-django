import argparse
import os

# Tạo parser để nhận thông tin database từ dòng lệnh
parser = argparse.ArgumentParser(description='Run Django with RDS database settings.')

# Các đối số cần thiết cho RDS
parser.add_argument('--db_name', required=True, help='Name of the RDS database')
parser.add_argument('--db_user', required=True, help='RDS database user')
parser.add_argument('--db_password', required=True, help='Password for RDS database user')
parser.add_argument('--db_host', required=True, help='RDS endpoint')
parser.add_argument('--db_port', default='3306', help='RDS port (default: 3306 for MySQL)')

# Thêm tùy chọn để thực hiện migrate hoặc runserver
parser.add_argument('--makemigration', action='store_true', help='Run makemigrations')
parser.add_argument('--createsuperuser', action='store_true', help='Run createsuperuser')
parser.add_argument('--migrate', action='store_true', help='Run migrations')
parser.add_argument('--runserver', action='store_true', help='Run the Django development server')

# Lấy các đối số từ dòng lệnh
args = parser.parse_args()

# Thiết lập các biến môi trường tương ứng
os.environ['DATABASE_NAME'] = args.db_name
os.environ['DATABASE_USER'] = args.db_user
os.environ['DATABASE_PASSWORD'] = args.db_password
os.environ['DATABASE_HOST'] = args.db_host
os.environ['DATABASE_PORT'] = args.db_port

# Chạy migrate nếu có tham số --migrate
if args.makemigration:
    os.system('python manage.py makemigrations')

if args.createsuperuser:
    os.system('python manage.py createsuperuser')
    
if args.migrate:
    os.system('python manage.py migrate')

# Chạy server nếu có tham số --runserver
if args.runserver:
    os.system('python manage.py runserver 0.0.0.0:8000')
