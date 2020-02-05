#关系型数据库管理系统（RDBMS）的 SQLite，它基于文件，不需要单独启动数据库服务器，适合在开发时使用，或是在数据库操作简单、访问量低的程序中使用
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os,sys

WIN = sys.platform.startswith('win')
if WIN:  # 如果是 Windows 系统，使用三个斜线
    prefix = 'sqlite:///'
else:  # 否则使用四个斜线
    prefix = 'sqlite:////'

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

if __name__ == "__main__":
    #有data.db则不用创建数据库
    #db.create_all()

    #写入数据库
    #在实例化模型类的时候，我们并没有传入 id 字段（主键），因为 SQLAlchemy 会自动处理这个字段。
    user = User(name='Grey Li')  # 创建一个 User 记录
    m1 = Movie(title='Leon', year='1994')  # 创建一个 Movie 记录
    m2 = Movie(title='Mahjong', year='1996')  # 再创建一个 Movie 记录
    db.session.add(user)  # 把新创建的记录添加到数据库会话
    db.session.add(m1)
    db.session.add(m2)
    db.session.commit()  # 提交数据库会话，只需要在最后调用一次即可

    #读取数据库
    movie = Movie.query.first()  # 获取 Movie 模型的第一个记录（返回模型类实例）
    str_year = movie.year
    str_all = Movie.query.all()  # 获取 Movie 模型的所有记录，返回包含多个模型类实例的列表
    str_num = Movie.query.count()  # 获取 Movie 模型所有记录的数量
    str_first_rec = Movie.query.get(1)  # 获取主键值为 1 的记录
    str_Mah = Movie.query.filter_by(title='Mahjong').first()  # 获取 title 字段值为 Mahjong 的记录
    str_Mah2 = Movie.query.filter(Movie.title=='Mahjong').first()  # 等同于上面的查询，但使用不同的过滤方法
    print(movie)
    print(str_year)
    print(str_all)
    print(str_num)
    print(str_first_rec)
    print(str_Mah)
    print(str_Mah2)

    #更新记录
    movie = Movie.query.get(2)
    movie.title = 'WALL-E'  # 直接对实例属性赋予新的值即可
    movie.year = '2008'
    db.session.commit()  # 注意仍然需要调用这一行来提交改动

    #删除记录
    movie = Movie.query.get(1)
    db.session.delete(movie)  # 使用 db.session.delete() 方法删除记录，传入模型实例
    db.session.commit()  # 提交改动


