#!/usr/bin/env python3
"""
重置或创建高管账号脚本。
用法：
  python scripts/reset_or_create_executive.py                     # 默认 executive@example.com / password123
  python scripts/reset_or_create_executive.py email@xx.com        # 指定邮箱，默认密码 password123
  python scripts/reset_or_create_executive.py email@xx.com newpw  # 指定邮箱与密码
"""

import sys
import os
from datetime import date

# 项目根目录加入路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import User

def main():
	email = sys.argv[1] if len(sys.argv) >= 2 else "executive@example.com"
	password = sys.argv[2] if len(sys.argv) >= 3 else "password123"
	app = create_app()
	with app.app_context():
		user = User.query.filter_by(email=email).first()
		if user:
			user.password = password
			user.user_type = 'executive'
			user.is_active = True
			if not user.first_name:
				user.first_name = "高管"
			if not user.last_name:
				user.last_name = "示例"
			if not user.position:
				user.position = "CEO"
			if not user.department:
				user.department = "总裁办"
			if not user.hire_date:
				user.hire_date = date.today()
			action = "重置"
		else:
			user = User(
				first_name="高管",
				last_name="示例",
				company_name="示例公司",
				position="CEO",
				email=email,
				phone_number="13800000000",
				birthday="1980-01-01",
				password=password,
				user_type='executive',
				department="总裁办",
				employee_id="EXE999",
				hire_date=date.today(),
				is_active=True,
			)
			db.session.add(user)
			action = "创建"
		db.session.commit()
		print(f"{action}成功：{email} / {password}")

if __name__ == "__main__":
	main()
