import db.module_db as module_db

data = module_db.insert_post("shangusdnswl", "SELECT * FROM user", "2020-01-01", "vic8701")
print(module_db.select_post(data[0]))