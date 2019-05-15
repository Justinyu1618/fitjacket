from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from app import db
from flask_sqlalchemy import SQLAlchemy
import datetime, os
from app.models import Summary, Heart_Rate, Map, Goal, User
from app.interface.utils import build_map, get_stats, get_heart_rate_data, get_goal_stats, get_users, find_partner

USER_ID = '1'
MAP_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'templates/maps/map-%s.html')
print("MAP PATH:", MAP_PATH)

DEBUG_MAP = True


interface_bp = Blueprint("interface", __name__, url_prefix='/')

@interface_bp.route('/')
def index():
	return redirect(url_for('interface.dashboard'))

@interface_bp.route('/dashboard', methods=['GET','POST'])
def dashboard():

	if request.method == 'POST':
		new_user = request.form['new_user']
		session['USER_ID'] = new_user
	stats = get_stats(session['USER_ID'])
	heart_rate_data = get_heart_rate_data(20, session['USER_ID'])
	print(f"HRD: {heart_rate_data}")
	return render_template('dashboard.html', stats=stats, heart_rate_data=heart_rate_data, users=get_users())

@interface_bp.route('/runs', methods=['GET'])
def run_summaries():
	summaries = Summary.query.filter_by(user_id=session['USER_ID']).all()
	summaries = sorted(summaries, key=lambda x:x.start_time, reverse=True)
	return render_template('run_summaries.html', summaries=summaries, users=get_users())

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
	summaries = Summary.query.filter_by(user_id=session['USER_ID']).all()
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
	return render_template('maps.html', urls=urls, users=get_users())

@interface_bp.route('/goals', methods=['GET', 'POST'])
def goals():
	print(f"REQ: {request.form}")
	if request.method == 'POST':
		result = request.form.copy()
		result['user_id'] = session['USER_ID']
		new_goal = Goal()
		new_goal.populate(result)
		db.session.add(new_goal)
		db.session.commit()

	stats = get_goal_stats(session['USER_ID'])
	print(f"GOAL: {stats}")
	return render_template('goals.html', stats=stats, users=get_users())

@interface_bp.route('/profile', methods=['GET', 'POST'])
def user_profile():
	if request.method == 'POST':
		new_user = request.form.copy()
		new_user['partners'] = ','
		new_id = list(User.query.order_by(User.user_id))
		if not new_id:
			new_id = 1
		else:
			new_id = int(sorted(new_id, key=lambda x: x.user_id)[-1].user_id) + 1
		new_user['user_id'] = new_id
		new_user['level'] = ''
		new = User()
		new.populate(new_user)
		db.session.add(new)
		db.session.commit()

	user = list(User.query.filter_by(user_id=session['USER_ID']))
	if not user:
		return render_template('user.html', exists=False)
	return render_template('user.html', user=user[0].serialize(), exists=True, users=get_users())

@interface_bp.route('/new_user', methods=['GET'])
def new_user():
	new_user = request.args.get('switch_to')
	session['USER_ID'] = new_user
	print(f'SWITCHING TO {new_user}')
	return redirect(url_for('interface.dashboard'))

@interface_bp.route('/find_partner', methods=['GET'])
def find_p():
	result, tracker = find_partner(session['USER_ID'], verbose=True)

	return f"RESULT: {result} <br> ALL USERS:{tracker}"

@interface_bp.route('/partners', methods=['GET', 'POST'])
def partners():
	if request.method == 'POST':
		score,partner = find_partner(session['USER_ID'])
		u = list(User.query.filter_by(user_id=partner))[0]
		return render_template('partners.html', valid=True, user=u,  users=get_users())
	else:
		return render_template('partners.html', valid=False, users=get_users())