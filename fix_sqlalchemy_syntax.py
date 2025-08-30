#!/usr/bin/env python3
"""
修复SQLAlchemy 2.0语法问题
将所有 db.session.execute('SQL') 改为 db.session.execute(text('SQL'))
"""

import os
import re
import glob

def fix_sqlalchemy_syntax():
    """修复SQLAlchemy语法"""
    print("🔧 修复SQLAlchemy 2.0语法问题...")
    
    # 查找所有Python文件
    python_files = glob.glob("**/*.py", recursive=True)
    
    for file_path in python_files:
        if os.path.isfile(file_path):
            print(f"   检查文件: {file_path}")
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 检查是否需要添加text导入
                needs_text_import = False
                if 'db.session.execute(' in content and 'from sqlalchemy import text' not in content:
                    needs_text_import = True
                
                # 修复db.session.execute语法
                old_pattern = r"db\.session\.execute\('([^']+)'\)"
                new_pattern = r"db.session.execute(text('\1'))"
                
                if re.search(old_pattern, content):
                    print(f"     🔄 修复SQL语法...")
                    content = re.sub(old_pattern, new_pattern, content)
                    
                    # 如果需要，添加text导入
                    if needs_text_import:
                        print(f"     📝 添加text导入...")
                        # 查找from sqlalchemy import行
                        if 'from sqlalchemy import' in content:
                            # 在现有的import行中添加text
                            content = re.sub(
                                r'from sqlalchemy import ([^,\n]+)',
                                r'from sqlalchemy import \1, text',
                                content
                            )
                        else:
                            # 添加新的import行
                            content = 'from sqlalchemy import text\n' + content
                    
                    # 写回文件
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    print(f"     ✅ 修复完成")
                
            except Exception as e:
                print(f"     ❌ 处理文件时出错: {e}")

def test_fix():
    """测试修复结果"""
    print("\n🧪 测试修复结果...")
    
    try:
        # 测试应用导入
        from app import create_app
        print("   ✅ 应用导入成功")
        
        # 测试应用创建
        app = create_app()
        print("   ✅ 应用创建成功")
        
        # 测试数据库连接
        from app.models import db
        from sqlalchemy import text
        
        with app.app_context():
            result = db.session.execute(text('SELECT 1'))
            print("   ✅ 数据库查询成功")
            
        print("   🎉 所有测试通过！")
        return True
        
    except Exception as e:
        print(f"   ❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("🚀 SQLAlchemy语法修复工具")
    print("=" * 50)
    
    # 执行修复
    fix_sqlalchemy_syntax()
    
    # 测试修复结果
    if test_fix():
        print("\n🎉 修复成功！现在应该可以正常访问了。")
        print("\n🌐 请访问: http://60.205.251.52/auth/sign")
    else:
        print("\n❌ 修复失败，请检查错误信息。")

if __name__ == "__main__":
    main()
