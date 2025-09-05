"""
LLRC Header Start
文件功能: 通用 Python 脚本/模块：scripts/link_employees_to_executive.py
创建时间: 2025-08-19 09:18
创建人: 张宇成
更新记录:
- 2025-08-19 09:48 by 潘显雨
- 2025-08-23 12:10 by 谢佳悦
- 2025-08-23 12:33 by 潘显雨
LLRC Header End
"""
#!/usr/bin/env python3
"""
FILE-HEADER-AUTO-ADDED
文件: scripts/link_employees_to_executive.py
功能: 通用模块
创建时间: 2025-09-01 15:34
创建人: 谢佳悦
更新记录:
- 2025-08-25 16:22 by 苏杰
"""
"""
把现有员工批量挂到某位高管名下（设置 supervisor_id），
用于让高管首页与员工管理页面的统计不为 0。
用法：
  python scripts/link_employees_to_executive.py               # 使用默认 executive@example.com
  python scripts/link_employees_to_executive.py other@xx.com  # 指定高管邮箱
"""

import sys
import os

# 将项目根路径加入 sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import User

def main():
	"""函数 main：核心业务逻辑。"""
	app = create_app()
	with app.app_context():
		exec_email = sys.argv[1] if len(sys.argv) > 1 else "executive@example.com"
		exec_user = User.query.filter_by(email=exec_email, user_type='executive').first()
		if not exec_user:
			print(f"未找到高管用户: {exec_email}")
			return
		
		employees = User.query.filter_by(user_type='employee').all()
		count = 0
		for emp in employees:
			if emp.supervisor_id != exec_user.id:
				emp.supervisor_id = exec_user.id
				count += 1
		
		db.session.commit()
		print(f"已将 {count} 名员工挂载到高管 {exec_email} (ID={exec_user.id}) 名下。")

if __name__ == "__main__":
	main()
