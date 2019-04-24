from flask import Blueprint, render_template, request, jsonify
from app import db
from flask_sqlalchemy import SQLAlchemy
import datetime
from app.models import Summary, Heart_Rate, Map

api_bp = Blueprint("api", __name__, url_prefix='/api')

@api_bp.route('/summaries', methods=['GET', 'POST'])
def summaries():
	if request.method == 'POST':
		try:
			new_summary = Summary()
			new_summary.populate(request.form)
			db.session.add(new_summary)
			db.session.commit()
			return "True"
		except Exception as e:
			return str(e)
	elif request.method == 'GET':
		user_id = request.args.get('user_id')
		sums = Summary.query.filter_by(user_id=user_id)
		ret = {'timestamp': datetime.datetime.now(),
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
		ret = {'timestamp': datetime.datetime.now(),
				'data': sums[:min(len(sums), num)]
				}
		return jsonify(ret)

@api_bp.route('/maps', methods=['POST'])
def map():
	if request.method == 'POST':
		try:
			new_map = Map()
			new_map.populate(request.form)
			db.session.add(new_map)
			db.session.commit()
			return "True"
		except Exception as e:
			return str(e)
	# elif request.method == 'GET':
	# 	user_id = request.args.get('user_id')
	# 	sums = Summary.query.filter_by(user_id=user_id)
	# 	ret = {'timestamp': datetime.datetime.now(),
	# 			'data': [s.serialize() for s in sums]
	# 			}
	# 	return jsonify(ret)