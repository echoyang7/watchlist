# 包构造文件，创建程序实例
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_moment import Moment

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'jiubugaosuni')#读取系统环境变量 SECRET_KEY 的值，如果没有获取到，则使用jiubugaosuni
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///'  + os.path.join(os.path.dirname(app.root_path), os.getenv('DATABASE_FILE', 'data.db'))

db = SQLAlchemy(app)
login_manager = LoginManager(app)
moment = Moment(app)


#Flask-Login 提供了一个 current_user 变量，注册这个函数的目的是，当程序运行后，如果用户已登录， current_user 变量的值会是当前用户的用户模型类记录。
@login_manager.user_loader
def load_user(user_id): # 创建用户加载回调函数，接受用户ID作为参数
    from watchlist.models import User# 避免循环依赖
    user = User.query.get(int(user_id)) # 用ID作为User模型的主键查询对应的用户
    return user # 返回用户对象

login_manager.login_view = 'login'

# 模板上下文处理函数
# 这个函数返回的变量（以字典键值对的形式）将会统一注入到每一个模板的上下文环境中，因此可以直接在模板中使用。
@app.context_processor
def inject_user():
    from watchlist.models import User# 避免循环依赖
    user = User.query.first()
    return dict(user=user)


#这几个模块同时也要导入构造文件中的程序实例，为了避免循环依赖（A 导入 B，B 导入 A），我们把这一行导入语句放到构造文件的结尾
from watchlist import views, errors, commands