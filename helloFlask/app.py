from flask import Flask, render_template
from dotenv import find_dotenv, load_dotenv

#读取.env文件并设置环境变量
load_dotenv(find_dotenv())

name = 'Grey Li'
movies = [
    {'title': 'My Neighbor Totoro', 'year': '1988'},
    {'title': 'Dead Poets Society', 'year': '1989'},
    {'title': 'A Perfect World', 'year': '1993'},
    {'title': 'Leon', 'year': '1994'},
    {'title': 'Mahjong', 'year': '1996'},
    {'title': 'Swallowtail Butterfly', 'year': '1996'},
    {'title': 'King of Comedy', 'year': '1999'},
    {'title': 'Devils on the Doorstep', 'year': '1999'},
    {'title': 'WALL-E', 'year': '2008'},
    {'title': 'The Pork of Music', 'year': '2012'},
]

#实例化这个类，创建一个程序对象 app
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', name=name, movies=movies)    #导入模板文件，并传入参数

if __name__ == "__main__":
    app.run()

