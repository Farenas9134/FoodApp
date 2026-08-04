from flask import Blueprint, render_template, request, flash, redirect, url_for

recipes_db = Blueprint('recipes', __name__, template_folder='templates')

@recipes_db.route('recipes')
def recipes():
    return 'Page to view top recipes or something'
