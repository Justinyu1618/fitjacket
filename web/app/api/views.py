from flask import Blueprint, render_template, request, jsonify
from app import db
from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
from app.models import Summary, Heart_Rate, Map, Goal
from app import USER_ID
from datetime import datetime, timedelta

api_bp = Blueprint("api", __name__, url_prefix='/api')

@api_bp.route('/summaries', methods=['GET', 'POST'])
def summaries():
	if request.method == 'POST':
		if True:# try:
			new_summary = Summary()
			new_summary.populate(request.form)
			print(new_summary)

			l = list(Goal.query.order_by(Goal.set_time))[::-1]
			print(f"GOALS: {l}")
			if l:
				l[0].progress(steps=new_summary.step_count, distance=new_summary.total_distance)
			else:
				print("NO GOALS SET")

			db.session.add(new_summary)
			db.session.commit()
			return "True"
		# except Exception as e:
		# 	return str(e)
	elif request.method == 'GET':
		user_id = request.args.get('user_id')
		sums = Summary.query.filter_by(user_id=user_id)
		ret = {'timestamp': datetime.now(),
				'data': [s.serialize() for s in sums]
				}
		return jsonify(ret)

@api_bp.route('/heart_rates', methods=['GET', 'POST'])
def heart_rate():
	if request.method == 'POST':
		try:
			new_hr = Heart_Rate()
			new_hr.populate(request.form)
			db.session.add(new_hr)
			db.session.commit()
			return "True"
		except Exception as e:
			return str(e)
	elif request.method == 'GET':
		user_id = request.args.get('user_id')
		num = int(request.args.get('num_samples'))
		sums = [x.serialize() for x in list(Heart_Rate.query.filter_by(user_id=user_id))]
		ret = {'timestamp': datetime.now(),
				'data': sums[:min(len(sums), num)]
				}
		return jsonify(ret)

@api_bp.route('/maps', methods=['POST', 'GET'])
def map():
	if request.method == 'POST':
		try:
			lats = request.form['lat'].strip().split(',')
			lons = request.form['lon'].strip().split(',')
			print(lats, len(lats))
			print(lons, len(lons))
			for i in range(len(lats)):
				new_map = Map()
				form = request.form.copy()
				form['lat'] = lats[i]
				form['lon'] = lons[i]
				new_map.populate(form)
				db.session.add(new_map)
			db.session.commit()
			return "True"
		except Exception as e:
			return str(e)
	elif request.method == 'GET':
		user_id = request.args.get('user_id')
		maps = Map.query.filter_by(user_id=user_id)
		ret = {'timestamp': datetime.now(),
				'data': [m.serialize() for m in maps]
				}
		return jsonify(ret)

@api_bp.route('/register', methods=['GET'])
def register():
	action = request.args.get('action')
	if action == 'new_user':
		return str(uuid4())
	elif action == 'new_run':
		user_id = request.args.get('user_id')
		if not user_id:
			return "Must provide user_id"
		return str(uuid4())

@api_bp.route('/goals', methods=['GET', 'POST'])
def goals():
	if request.method == 'POST':
		new_goal = Goal()
		new_goal.populate(request.form)
		db.session.add(new_goal)
		db.session.commit()
		return "True"
	elif request.method == 'GET':
		user_id = request.args.get('user_id')
		action = request.args.get('type')
		recent_goal = Goal.query.filter_by(user_id=user_id).order_by(Goal.set_time)[::-1]
		if not recent_goal:
			return "No goals found"
		recent_goal = recent_goal[0]
		print(recent_goal)
		if action == "steps":
			return str(recent_goal.steps)
		elif action == "distance":
			return str(recent_goal.distance)
		return "Incorrect parameters"

@api_bp.route('/charts-heart-rate', methods=['GET'])
def charts_heart_rate():
	time_range = int(request.args.get('range'))
	points = list(Heart_Rate.query.filter_by(user_id=USER_ID))
	data = []
	cutoff = datetime.now() - timedelta(days=time_range)
	x_axis = time_range * 3600
	for p in points:
		if p.time_stamp > cutoff:
			x = (p.time_stamp - cutoff).seconds
			y = p.heart_rate
			data.append({"x":x, "y":y})
	return jsonify(data)

