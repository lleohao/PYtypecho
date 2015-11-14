from flask import render_template, redirect, flash, request
from flask.ext.login import login_required
from . import admin


@admin.route("/main")
@login_required
def main():
    return render_template("/admin/main.html")