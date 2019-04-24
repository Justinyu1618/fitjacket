from flask import Flask
from flask_sqlalchemy import SQLAlchemy


application = None
db = None


def create_app():
	global application, db
	application = Flask(__name__)
	application.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ndkjqzukyumppd:10a3fa2383a84cc5ba49af738ff7252288c590d25c4461d3d18e7cdc42d737bc@ec2-50-19-127-115.compute-1.amazonaws.com:5432/d6hg72imukrjj8'
	application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

	db = SQLAlchemy(application)
	

	from app.api.views import api_bp
	from app.interface.views import interface_bp
	application.register_blueprint(api_bp)
	application.register_blueprint(interface_bp)

	db.create_all()
	return application