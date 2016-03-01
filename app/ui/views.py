# coding: utf-8
from . import ui


@ui.route("/")
def index():
    # url_for('ui.static', filename="js/main.js") 引入前台静态文件
    return "ok"
