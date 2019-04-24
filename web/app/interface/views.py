from flask import Blueprint, render_template

app_bp = Blueprint("app", __name__, url_prefix='/')


# @app_bp.route('/dashboard')
# def dashboard():
# 	return render_template('dashboard.html')