import gmplot

def build_map(lat_list, lon_list, dest):
	starting
	gmap = gmplot.GoogleMapPlotter()
	gmap.scatter(lat_list, lon_list, '#4DCBCC', size=30, marker=True)
	gmap.plot(lat_list, lon_list, '#4dcbcc', edge_width=3)
	gmap.draw(dest)
	return True