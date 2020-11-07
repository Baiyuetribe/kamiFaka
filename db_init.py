from service.database.models import creat_table,drop_table
from service.config.config import init_db
# 清空表
drop_table()
# 创建表
creat_table()
# 初始化表
init_db()


## 上述逻辑为强制数据库清空与刷新，适合一遍部署环境或开发环境，如果是docker环境，如果重启则存在重复执行可能性，
## 因此正式环境需要补加一个判断。