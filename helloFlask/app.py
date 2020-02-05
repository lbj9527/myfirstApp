from flask import Flask, render_template
from dotenv import find_dotenv, load_dotenv
from flask_sqlalchemy import SQLAlchemy
import os,sys

WIN = sys.platform.startswith('win')
if WIN:  # 如果是 Windows 系统，使用三个斜线
    prefix = 'sqlite:///'
else:  # 否则使用四个斜线
    prefix = 'sqlite:////'

app = Flask(__name__)

#读取.env文件并设置环境变量
load_dotenv(find_dotenv())

#实例化这个类，创建一个程序对象 app
app = Flask(__name__)

#配置变量的名称必须使用大写，写入配置的语句一般会放到扩展类实例化语句之前
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False          # 关闭对模型修改的监控

db = SQLAlchemy(app)  #初始化扩展，传入程序实例

#创建模型类
class User(db.Model):     #表名将会是user
    id = db.Column(db.Integer, primary_key=True)   #主键
    name = db.Column(db.String(20))    #名字

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))    #电影标题
    year = db.Column(db.String(4))      #电影年份

def forge():
    """Generate fake data."""
    db.drop_all()    #先删除所有数据
    db.create_all()

    # 全局的两个变量移动到这个函数内
    name = '老北京9527'
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

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)
    db.session.commit()

@app.route('/')
def index():
    user = User.query.first()  # 读取用户记录
    movies = Movie.query.all()  # 读取所有电影记录
    return render_template('index.html', user = user, movies=movies)    #导入模板文件，并传入参数

if __name__ == "__main__":
    #创建数据库，并生成虚拟数据
    forge()
    app.run()

