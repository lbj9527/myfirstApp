from flask import request,url_for,redirect,flash
from flask import render_template, Flask
from dotenv import find_dotenv, load_dotenv
from flask_sqlalchemy import SQLAlchemy
import os,sys
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin,login_user,logout_user,login_required,current_user
import click

############################################################初始化工作##########################################################
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

#实例化登录类
login_manager = LoginManager(app)
login_manager.login_view = 'login'    #设为我们程序的登录视图端点(函数名)

#配置变量的名称必须使用大写，写入配置的语句一般会放到扩展类实例化语句之前
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False          # 关闭对模型修改的监控
app.config['SECRET_KEY'] = 'dev'   #flash() 函数在内部会把消息存储到 Flask 提供的 session 对象里。session 用来在请求间存储数据，
                                   #它会把数据签名后存储到浏览器的 Cookie 中，所以我们需要设置签名所需的密钥
                                   #这个密钥的值在开发时可以随便设置。基于安全的考虑，在部署时应该设置为随机字符，且不应该明文写在代码里， 在部署章节会详细介绍

db = SQLAlchemy(app)  #初始化扩展，传入程序实例


#######################################################建立数据库操作函数#########################################################
#创建模型类
class User(db.Model, UserMixin):     #表名将会是user;继承UserMixin类会让 User 类拥有几个用于判断认证状态的属性和方法
    id = db.Column(db.Integer, primary_key=True)   #主键
    name = db.Column(db.String(20))                #名字
    username = db.Column(db.String(20))            #用户名
    password_hash = db.Column(db.String(128))      #密码散列值

    def set_password(self, password):      #用来设置密码的方法，接受密码作为参数
        self.password_hash = generate_password_hash(password)      #将生成的密码保存到对应字段     

    def validate_password(self, password):      #用于验证密码的方法，接受密码作为参数
        return check_password_hash(self.password_hash, password)     #返回布尔值

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))    #电影标题
    year = db.Column(db.String(4))      #电影年份

#手动命令行命令，用来创建虚拟数据
@app.cli.command()
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
    click.echo('Done.')


#####################################################flask网页生成(视图函数)####################################################
#主页
@app.route('/',methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        if not current_user.is_authenticated:    #如果用户未认证
            return redirect(url_for('index'))
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
    movies = Movie.query.all()  # 读取所有电影记录
    return render_template('index.html', movies=movies)    #导入模板文件，并传入参数

#记录编辑页
@app.route('/movie/edit/<int:movie_id>', methods=['GET','POST'])
@login_required     #登录保护，未登录用户不能访问
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

#用户登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))

        user = User.query.first()
        #验证用户名和密码是否一致
        if username == user.username and user.validate_password(password):
            login_user(user)    #登入用户
            flash('Login success.')
            return redirect(url_for('index'))    #重定向到主页

        flash('Invalid username or password.')   #如果验证失败，显示错误消息
        return redirect(url_for('login'))      #重定向回登录页面
    return render_template('login.html')

#用户登出
@app.route('/logout')
@login_required   #登录保护，未登录用户不能访问
def logout():
    logout_user()   #登出用户
    flash('Goodbye.')
    return redirect(url_for('index'))

#设置页面，支持设置用户名字
@app.route('/settings', methods=['GET','POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']
        
        if not name or len(name) > 20:
            flash('Invalid input.')
            return redirect(url_for('settings'))

        # current_user 会返回当前登录用户的数据库记录对象
        # 等同于下面的用法
        # user = User.query.first()
        # user.name = name
        current_user.name = name
        
        db.session.commit()
        flash('Setting updated.')
        return redirect(url_for('index'))

    return render_template('settings.html')

###############################################################生成管理员账户#######################################################
def admin(username, password):
    user = User.query.first()
    print('user', user)
    if user is not None:
        user.username = username
        user.set_password(password)    #设置密码
    else:
        user = User(username=username, name='Admin')
        user.set_password(password)
        db.session.add(user)
    db.session.commit()      #提交数据库会话
    
#初始化Flask-Login(用户加载回调函数)
#Flask-Login 提供了一个 current_user 变量，注册这个函数的目的是，当程序运行后，
# 如果用户已登录， current_user 变量的值会是当前用户的用户模型类记录
@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    return user    #返回用户对象

#############################################################模板上下文处理函数#####################################################
@app.context_processor
def inject_user():
    user = User.query.first()    # 读取用户记录
    return dict(user=user)    #返回字典，等同于return {'user':user}

################################################################错误处理函数#######################################################
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404









###################################主程序######################################
if __name__ == "__main__":

    #生成管理员账户
    admin('admin','123456')

    app.run()




###################################备注######################################
#1.程序中会报db没有某某成员的错误，着其实不是错误，运行时没有问题
#  原因：db的成员是程序运行时产生的，pylint只能检查静态的语法错误
