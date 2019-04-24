#http://exploreflask.com/en/latest/organizing.html
#https://pusher.com/tutorials/live-dashboard-python

"""
create table run_summaries(user_id text, run_id text, start_time timestamp, end_time timestamp, total_distance text, step_count text)
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String
from sqlalchemy.types import DateTime, JSON, Boolean
from sqlalchemy.dialects.postgresql import array
from flask import Flask 
import app.views
from app.views import app_bp
import sqlite3


app = Flask(__name__)
db = create_engine('postgres://ndkjqzukyumppd:10a3fa2383a84cc5ba49af738ff7252288c590d25c4461d3d18e7cdc42d737bc@ec2-50-19-127-115.compute-1.amazonaws.com:5432/d6hg72imukrjj8')

app.register_blueprint(app_bp)
