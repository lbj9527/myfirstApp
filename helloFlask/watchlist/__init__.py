#包构造文件，创建程序实例
import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import find_dotenv, load_dotenv

WIN = sys.platform.startswith('win')
if WIN:  # 如果是 Windows 系统，使用三个斜线
    prefix = 'sqlite:///'
else:  # 否则使用四个斜线
    prefix = 'sqlite:////'

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

#实例化登录类
login_manager = LoginManager(app)
#初始化Flask-Login(用户加载回调函数)
#Flask-Login 提供了一个 current_user 变量，注册这个函数的目的是，当程序运行后，
# 如果用户已登录， current_user 变量的值会是当前用户的用户模型类记录
@login_manager.user_loader
def load_user(user_id):
    from watchlist.models import User
    user = User.query.get(int(user_id))
    return user

login_manager.login_view = 'login'    #设为我们程序的登录视图端点(函数名)



#############################################################模板上下文处理函数#####################################################
@app.context_processor
def inject_user():
    from watchlist.models import User
    user = User.query.first()    # 读取用户记录
    return dict(user=user)    #返回字典，等同于return {'user':user}

#为了让视图函数、错误处理函数和命令函数注册到程序实例上，我们需要在这里导入这几个模块。
# 但是因为这几个模块同时也要导入构造文件中的程序实例，为了避免循环依赖（A 导入 B，B 导入 A），我们把这一行导入语句放到构造文件的结尾
from watchlist import views, errors, commands