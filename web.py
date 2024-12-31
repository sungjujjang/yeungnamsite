from flask import Flask # type: ignore
import db.module_db as module_db
import config.settings as settings

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask!"

if __name__ == '__main__':
    app.run(debug=True)