from flask import Blueprint, render_template

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/login")
def login():
    return "原来如此"

@bp.route("/register")
def register():
    return render_template("login.html")
    #如果刚开始环境没有配好，不能自动出来flask的设置文件夹的话，一些目录路径还需要自己再进行手动的配置