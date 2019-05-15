from random import random, randint
import gmplot
from math import sin, cos, sqrt, radians, atan2, log, pi, ceil
import numpy as np

MAP_HEIGHT = 600

DIST_CONST = 1

def new_data(length):
	lat_seed = 42.36 + random()*0.01
	lon_seed = -71.05 + random()*0.01
	lat_list, lon_list = [lat_seed],[lon_seed]
	for i in range(length):
		d = randint(0,10)
		s = 1 if d %2==0 else -1
		lat_list.append(lat_list[-1] + s * d * random() * 0.001)
		lon_list.append(lon_list[-1] + -1 * s * (10-d) * random() * 0.001)
	return lat_list, lon_list

def new_data2(length):
	lat_seed = 42.3612 + random()*0.0001
	lon_seed = -71.0920 + random()*0.0001
	lat_list, lon_list = [lat_seed],[lon_seed]
	for i in range(length):
		d = randint(0,5)
		s = 1 if d %2==0 else -1
		lat_list.append(lat_list[-1] + d * random() * 0.00005)
		lon_list.append(lon_list[-1] + (5-d) * random() * 0.00005)
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

def dist(p1, p2):
	return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5

def build_map(lat_list, lon_list, gm=None, color='#4dcbcc'):
	center, zoom = find_center_zoom(lat_list, lon_list)
	print(f'Center: {center}')
	if gm:
		gmap = gm
	else:
		gmap = gmplot.GoogleMapPlotter(center[0], center[1], zoom, apikey='AIzaSyBxhQschyIWYAi9Yu3_vW-Wwb2YgK3dWO4')
	gmap.scatter(lat_list, lon_list, color, size=30, marker=True)
	gmap.plot(lat_list, lon_list, color, edge_width=3)
	return gmap

if __name__ == '__main__':
	lat, lon = new_data(50)
	lat2,lon2 = new_data2(20)
	print(lat2, lon2)
	lat3, lon3 = new_data2(10)

	#lat2_i, lon2_i = interp(0.9, lat2, lon2)
	#lat = [0,1,2,3,3,2,1,0,-1,-1,0,1,2,3,4,4,3,2,1,0,-1,-2,-2,-1,0,1,2,3,4]
	#lon = [0,0,0,0,5,5,5,5,5,-5,-5,-5,-5,-5,-5,10,10,10,10,10,10,10,10,-15,-15,-15,-15,-15,-15,-15]
	lat_i, lon_i = interp(51/180,lat, lon)
	print(f"TEST{len(lat_i), len(lat)}")
	m1 = build_map(lat, lon)
	#m2 = build_map(lat2,lon2)
	#m3 = build_map(lat3, lon3, m2)
	m4 = build_map(lat_i, lon_i, m1, color='#111111')
	m1.draw('1.html')
