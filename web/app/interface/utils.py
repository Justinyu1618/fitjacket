import gmplot
import os

MAP_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)))
print(MAP_PATH)

def build_map(maps, dest):
	try:
		lat_list = [float(m.lat) for m in maps]
		lon_list = [float(m.lon) for m in maps]
		gmap = gmplot.GoogleMapPlotter(lat_list[0], lon_list[0], 10, apikey='AIzaSyBxhQschyIWYAi9Yu3_vW-Wwb2YgK3dWO4')
		gmap.scatter(lat_list, lon_list, '#4DCBCC', size=30, marker=True)
		gmap.plot(lat_list, lon_list, '#4dcbcc', edge_width=3)
		print('DREW_MAP')
		print(dest)
		gmap.draw(dest)
		return True
	except Exception as e:
		print(e)
		print(f'LAT: {lat_list}, LON: {lon_list}')