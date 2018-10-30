
#! /bin/bash
mysql -uturing -pmysql -h127.0.0.1 shopMall < areas.sql;

#! 增加权限
#! chmod +x import_area_data_to_db.sh
