# Database initialization script
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import init_db, test_connection

def main():
    print("=" * 50)
    print("AI日报 v2.0 数据库初始化")
    print("=" * 50)
    
    # 测试连接
    print("\n[1/2] 测试数据库连接...")
    if not test_connection():
        print("\n❌ 连接失败，请检查 DATABASE_URL 环境变量")
        print("示例: export DATABASE_URL='postgresql://user:pass@host:port/db'")
        return
    
    # 创建表
    print("\n[2/2] 创建数据库表...")
    init_db()
    
    print("\n" + "=" * 50)
    print("✅ 数据库初始化完成")
    print("=" * 50)

if __name__ == "__main__":
    main()
