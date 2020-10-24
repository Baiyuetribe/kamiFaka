from service.database.models import creat_table,drop_table
from service.config.config import init_db
# 清空表
drop_table()
# 创建表
creat_table()
# 初始化表
init_db()