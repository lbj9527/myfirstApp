from flask import Flask
from flask import url_for, escape    #url_for如果跟在Flask模块后面会报错
from dotenv import find_dotenv, load_dotenv

#读取.env文件并设置环境变量
load_dotenv(find_dotenv())


#实例化这个类，创建一个程序对象 app
app = Flask(__name__)

#实验1
#注册一个处理函数，这个函数是处理某个请求的处理函数，Flask 官方把它叫做视图函数（view funciton），可以理解为“请求处理函数”
@app.route('/')
def hello():
    return '<h1>Helloo Totoro!</h1><img src="http://helloflask.com/totoro.gif">'

#实验2
#url也可以设置成变量
@app.route('/user/<name>')
def hello2(name):
    return '<h1>Helloo Totoro!</h1><img src="http://helloflask.com/totoro.gif"> %s' % escape(name)   # 也可以通过escape获取到变量值

#实验3
@app.route('/user/<name>')
def user_page(name):
    return 'User: %s' % escape(name)

@app.route('/test')
def test_url_for():
    # 下面是一些调用示例（请在命令行窗口查看输出的 URL）：
    print(url_for('hello'))  # 输出：/
    # 注意下面两个调用是如何生成包含 URL 变量的 URL 的
    print(url_for('user_page', name='greyli'))  # 输出：/user/greyli
    print(url_for('user_page', name='peter'))  # 输出：/user/peter
    print(url_for('test_url_for'))  # 输出：/test
    # 下面这个调用传入了多余的关键字参数，它们会被作为查询字符串附加到 URL 后面。
    print(url_for('test_url_for', num=2))  # 输出：/test?num=2
    return 'Test page'

if __name__ == "__main__":
    app.run()


###############################备注#############################
#1.调试模式可以通过将系统环境变量 FLASK_ENV 设为 development 来开启。
#  调试模式开启后，当程序出错，浏览器页面上会显示错误信息；代码出现变动后，程序会自动重载。