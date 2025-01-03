import db.module_db as module_db
import datetime

date = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

# data = module_db.insert_post("shangusdnswl", "SELECT * FROM user", date, "vic8701")
# print(module_db.select_post(data[0]))

for i in range(1,20):
    module_db.insert_post(f"나는야노무현", f"노무현{i}명이 운지했습니다\n부엉부엉부엉", date, "니애미창녀")

# import db.setting_db as setting_db

# setting_db.addtable()