from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from app import db
from flask_sqlalchemy import SQLAlchemy
import datetime, os
from app.models import Summary, Heart_Rate, Map, Goal
from app.interface.utils import build_map, get_stats, get_heart_rate_data, get_goal_stats

USER_ID = '1'
MAP_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'templates/maps/map-%s.html')
print("MAP PATH:", MAP_PATH)

DEBUG_MAP = True


interface_bp = Blueprint("interface", __name__, url_prefix='/')

@interface_bp.route('/')
def index():
	return redirect(url_for('interface.dashboard'))

@interface_bp.route('/dashboard', methods=['GET'])
def dashboard():
	stats = get_stats(USER_ID)
	heart_rate_data = get_heart_rate_data(20)
	print(f"HRD: {heart_rate_data}")
	return render_template('dashboard.html', stats=stats, heart_rate_data=heart_rate_data)

@interface_bp.route('/runs', methods=['GET'])
def run_summaries():
	summaries = Summary.query.filter_by(user_id=USER_ID).all()
	summaries = sorted(summaries, key=lambda x:x.start_time, reverse=True)
	return render_template('run_summaries.html', summaries=summaries)

@interface_bp.route('/maps/<run_id>', methods=['GET'])
def maps_(run_id):
	return render_template(f'maps/map-{run_id}.html')

@interface_bp.route('/maps', methods=['GET'])
def maps():
	# map_coords = Map.query.filter_by(user_id=USER_ID).all()
	# summaries = sorted(map_coords, key=lambda x:x.start_time, reverse=True)
	# return render_template('run_summaries.html', summaries=summaries)
	base = request.base_url
	urls = {}
	summaries = Summary.query.filter_by(user_id=USER_ID).all()
	runs = [s.run_id for s in summaries]
	for r in runs:
		if os.path.isfile(MAP_PATH % r) and not DEBUG_MAP:
			urls[r] = base + f'/{r}'
		else:
			maps = Map.query.filter_by(run_id=r).all()
			if list(maps):
				if build_map(maps, MAP_PATH % r):
					urls[r] = base + f'/{r}'
	print('abouot to render')
	return render_template('maps.html', urls=urls)

@interface_bp.route('/goals', methods=['GET', 'POST'])
def goals():
	print(f"REQ: {request.form}")
	if request.method == 'POST':
		result = request.form.copy()
		result['user_id'] = USER_ID
		new_goal = Goal()
		new_goal.populate(result)
		db.session.add(new_goal)
		db.session.commit()

	stats = get_goal_stats(USER_ID)
	print(f"GOAL: {stats}")
	return render_template('goals.html', stats=stats)

@interface_bp.route('/profile', methods=['GET'])
def user_profile():
	return render_template('user.html')