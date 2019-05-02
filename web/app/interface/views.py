from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from app import db
from flask_sqlalchemy import SQLAlchemy
import datetime
from app.models import Summary, Heart_Rate, Map

USER_ID = '1'

interface_bp = Blueprint("interface", __name__, url_prefix='/')

@interface_bp.route('/')
def index():
	return redirect(url_for('interface.dashboard'))

@interface_bp.route('/dashboard', methods=['GET'])
def dashboard():
	return render_template('dashboard.html')

@interface_bp.route('/runs', methods=['GET'])
def run_summaries():
	summaries = Summary.query.filter_by(user_id=USER_ID).all()
	summaries = sorted(summaries, key=lambda x:x.start_time, reverse=True)
	return render_template('run_summaries.html', summaries=summaries)

@interface_bp.route('/maps/<num>', methods=['GET'])
def maps_(num):
	return render_template(f'map{num}.html')

@interface_bp.route('/maps', methods=['GET'])
def maps():
	# map_coords = Map.query.filter_by(user_id=USER_ID).all()
	# summaries = sorted(map_coords, key=lambda x:x.start_time, reverse=True)
	# return render_template('run_summaries.html', summaries=summaries)
	return render_template('maps.html', map_addr=1)



@interface_bp.route('/profile', methods=['GET'])
def user_profile():
	return render_template('user.html')