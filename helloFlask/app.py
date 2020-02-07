from flask import request,url_for,redirect,flash
from flask import render_template, Flask
from dotenv import find_dotenv, load_dotenv
from flask_sqlalchemy import SQLAlchemy
import os,sys

###################################初始化工作######################################
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
app.config['SECRET_KEY'] = 'dev'   #flash() 函数在内部会把消息存储到 Flask 提供的 session 对象里。session 用来在请求间存储数据，
                                   #它会把数据签名后存储到浏览器的 Cookie 中，所以我们需要设置签名所需的密钥
                                   #这个密钥的值在开发时可以随便设置。基于安全的考虑，在部署时应该设置为随机字符，且不应该明文写在代码里， 在部署章节会详细介绍

db = SQLAlchemy(app)  #初始化扩展，传入程序实例


###################################建立数据库操作函数######################################
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


###################################flask网页生成(视图函数)######################################
#主页
@app.route('/',methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        #获取表单数据
        title = request.form.get('title')  #传入表单对应输入字段的name值
        year = request.form.get('year')
        #验证数据
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invaild input.')    #显示错误提示
            return redirect(url_for('index'))    #重定向回主页
        #保存表单数据到数据库
        movie = Movie(title=title, year=year)    #创建记录
        db.session.add(movie)    #添加到数据库会话
        db.session.commit()      #提交数据库会话
        flash('Item created.')   #显示成功创建的提示
        return redirect(url_for('index'))    #重定向回主页
    user = User.query.first()
    movies = Movie.query.all()
    return render_template('index.html', user=user, movies = movies)
        
    movies = Movie.query.all()  # 读取所有电影记录
    return render_template('index.html', movies=movies)    #导入模板文件，并传入参数

#记录编辑页
@app.route('/movie/edit/<int:movie_id>', methods=['GET','POST'])
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if request.method == 'POST':    #处理编辑表单的提交请求
        title = request.form['title']
        year = request.form['year']

        if not title or not year or len(year) > 4 or len(title) > 60:
            flash("Invalid input.")
            return redirect(url_for('edit', movie_id=movie_id))
        
        
        movie.title = title  #更新标题
        movie.year = year    #更新年份
        db.session.commit()  #提交数据库会话
        flash('Item updated.')
        return redirect(url_for('index'))    #重定向回主页

    return render_template('edit.html', movie=movie)    #传入被编辑的电影记录

#删除电影条目
@app.route('/movie/delete/<int:movie_id>', methods=['POST'])   #限定只接受POST请求
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)   #获取电影记录
    db.session.delete(movie)     #删除对应的记录
    db.session.commit()
    flash('Item deleted.')
    return redirect(url_for('index')) #重定向到主页







#######################################模板上下文处理函数#################################
@app.context_processor
def inject_user():
    user = User.query.first()    # 读取用户记录
    return dict(user=user)    #返回字典，等同于return {'user':user}

#######################################错误处理函数#################################
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404









###################################主程序######################################
if __name__ == "__main__":
    #创建数据库，并生成虚拟数据
    forge()
    app.run()

