from flask import Flask
from dotenv import find_dotenv, load_dotenv

# 1、读取.env文件并设置环境变量
load_dotenv(find_dotenv())

app = Flask(__name__)

@app.route('/home')
def hello():
    return '<h1>Helloo Totoro!</h1><img src="http://helloflask.com/totoro.gif">'

if __name__ == "__main__":
    app.run()