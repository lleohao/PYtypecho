from flask import Blueprint

ui = Blueprint("ui", __name__, template_folder="templates")

from . import views