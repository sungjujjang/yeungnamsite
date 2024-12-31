import db.module_db as module_db
import datetime

date = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

data = module_db.insert_post("shangusdnswl", "SELECT * FROM user", date, "vic8701")
print(module_db.select_post(data[0]))

module_db.insert_notice("shangusdnswl", "SELECT * FROM user", date, "vic8701")