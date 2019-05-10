import gmplot
import os
from math import sin, cos, sqrt, radians, atan2, log, pi, ceil
from app import db, USER_ID
from app.models import Summary, Heart_Rate, Map, Goal
from datetime import datetime, timedelta

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
	average_pace = sum([3.6 * (x.total_distance / ((x.end_time - x.start_time).seconds+0.1)) for x in result]) / len(result)
	average_pace = round(average_pace,2)
	return_dict = {'Distance Traveled': total_distance,
					'Average Pace': average_pace,
					'Completed Runs': len(result),
					'Step Count': total_steps}
	return return_dict

def get_heart_rate_data(time_range):
	points = list(Heart_Rate.query.filter_by(user_id=USER_ID))
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
	l = list(Goal.query.filter_by(user_id=user_id).order_by(Goal.set_time))[-1]
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