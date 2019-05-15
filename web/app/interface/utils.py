import gmplot
import os
from math import sin, cos, sqrt, radians, atan2, log, pi, ceil
from app import db
from app.models import Summary, Heart_Rate, Map, Goal, User
from datetime import datetime, timedelta
import numpy as np

MAP_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)))
print(MAP_PATH)
MAP_HEIGHT = 600

def build_map(maps, dest):
	try:
		lat_list = [float(m.lat) for m in maps]
		lon_list = [float(m.lon) for m in maps]
		center, zoom = find_center_zoom(lat_list, lon_list)
		print(f'Center: {center}')
		gmap = gmplot.GoogleMapPlotter(center[0], center[1], zoom, apikey='AIzaSyBxhQschyIWYAi9Yu3_vW-Wwb2YgK3dWO4')
		gmap.scatter(lat_list, lon_list, '#4DCBCC', size=30, marker=True)
		gmap.plot(lat_list, lon_list, '#4dcbcc', edge_width=3)
		print('DREW_MAP')
		print(dest)
		gmap.draw(dest)
		return True
	except Exception as e:
		print(e)
		print("ARGH")
		#print(f'LAT: {lat_list}, LON: {lon_list}')

def dist(p1, p2):
	return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5

def find_center_zoom(lats, lons):
	largest = 0
	farthest = 0
	points = zip(lats,lons)
	for p1 in points:
		for p2 in points:
			if dist(p1,p2) > largest:
				farthest = (p1,p2)
				largest = dist(p1, p2)

	p1, p2 = farthest
	center = ((p1[0]+p2[0])/2, (p1[1]+p2[1])/2)
	dlat, dlon = radians(p1[0]) - radians(p2[0]), radians(p1[1]) - radians(p2[1])
	a = sin(dlat / 2)**2 + cos(p2[0]) * cos(p2[0]) * sin(dlon / 2)**2
	c = 2 * atan2(sqrt(a), sqrt(1 - a))
	distance = c * 6373.0 * 1000
	target_mpp = (distance/MAP_HEIGHT)*1.5
	#meters_per_pixel = 156543.03392 * cos(center[0] * pi / 180) / (2 ** zoom)
	temp = 156543.03392 * cos(center[0] * pi / 180) / target_mpp
	zoom = log(temp, 2)
	print(f'ZOOOM: {zoom}')
	zoom = ceil(zoom)

	return center, zoom

def get_stats(uid):
	result = list(Summary.query.filter_by(user_id=uid))
	total_distance = sum([x.total_distance for x in result])
	total_steps = sum([x.step_count for x in result])
	average_pace = sum([3.6 * (x.total_distance / ((x.end_time - x.start_time).seconds+0.1)) for x in result]) / len(result) if result else 0
	average_pace = round(average_pace,2)
	return_dict = {'Distance Traveled': total_distance,
					'Average Pace': average_pace,
					'Completed Runs': len(result),
					'Step Count': total_steps}
	return return_dict

def get_heart_rate_data(time_range, uid):
	points = list(Heart_Rate.query.filter_by(user_id=uid))
	data = []
	cutoff = datetime.now() - timedelta(days=time_range)
	x_axis = time_range * 3600
	for p in points:
		if p.time_stamp > cutoff:
			x = p.time_stamp.strftime("%B %d, %Y %H:%M:%S")
			y = p.heart_rate
			data.append({"x":x, "y":y})
	print(data)
	return data

def get_goal_stats(user_id):
	l = list(Goal.query.filter_by(user_id=user_id).order_by(Goal.set_time))
	if not l:
		return {
		'steps_current': 0,
		'steps_goal': 1,
		'steps_last': 0,
		'distance_current': 0,
		'distance_goal': 1,
		'distance_last': 0
		}
	else:
		l = l[-1]
	print(l.serialize())
	result = {
		'steps_current': l.steps_goal - l.steps,
		'steps_goal': l.steps_goal,
		'steps_last': l.last_modified,
		'distance_current': l.distance_goal - l.distance,
		'distance_goal': l.distance_goal,
		'distance_last': l.last_modified
	}
	return result

def get_users():
	return list(User.query.order_by(User.user_id))

def find_partner(target_user, verbose=False):
	T_lat, T_lon = get_most_recent_map(target_user)
	all_users = [x.user_id for x in User.query.all()]
	print(all_users)
	lowest = (float("Inf"),0)
	tracker = {}
	for user in all_users:
		if user == target_user:
			continue
		runs = [s.run_id for s in Summary.query.filter_by(user_id=user).all()]
		if not runs:
			continue
		current = 0
		for r in runs:
			maps = Map.query.filter_by(run_id=r).all()
			try:
				lat_list = [float(m.lat) for m in maps]
				lon_list = [float(m.lon) for m in maps]
			except:
				continue
			if not maps:
				continue
			if len(lat_list) >= len(T_lat):
				new_lat, new_lon = interp(len(T_lat)/len(lat_list), T_lat, T_lon)
				old_lat, old_lon = lat_list[:len(new_lat)], lon_list[:len(new_lat)]
			else:
				new_lat, new_lon = interp(len(lat_list)/len(T_lat), lat_list, lon_list)
				old_lat, old_lon = T_lat[:len(new_lat)], T_lon[:len(new_lat)]
			score = correlate(list(zip(new_lat, new_lon)), list(zip(old_lat, old_lon)))
			current += score
		avg = current / len(runs)
		if avg < lowest[0]:
			lowest = (avg, user)
		tracker[user] = avg
	print(f"FOUND USER: {lowest[1]} WITH SCORE {lowest[0]}")
	if verbose:
		return lowest, tracker
	return lowest



def correlate(pts1, pts2):
	return sum([dist(pts1[i], pts2[i]) for i in range(len(pts1))])/len(pts1)

def get_most_recent_map(user_id):
	run = sorted(list(Summary.query.filter_by(user_id=user_id).all()), key=lambda x:x.end_time, reverse=True)
	if run:
		run = run[0].run_id
	print(f"USER: {user_id}, RUN: {run}")
	maps = Map.query.filter_by(run_id=run)
	lat_list = [float(m.lat) for m in maps]
	lon_list = [float(m.lon) for m in maps]
	return lat_list, lon_list

def interp(frac, lat, lon):
	result_y = [lon[0]]
	result_x = [lat[0]]
	i = 1
	temp_frac = 0
	while(i < len(lat)-1):
		print(temp_frac)
		x = lat[i-1]+temp_frac*(lat[i]-lat[i-1])
		result_x.append(x)
		result_y.append(np.interp(x, lat[i-1:i+1], lon[i-1:i+1]))
		temp_frac += frac 
		if temp_frac > 1:
			i += 1
			temp_frac -= 1
	return result_x, result_y