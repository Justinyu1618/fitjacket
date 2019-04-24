from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from app import db
from flask_sqlalchemy import SQLAlchemy
import datetime
from app.models import Summary, Heart_Rate, Map

interface_bp = Blueprint("interface", __name__, url_prefix='/')

@interface_bp.route('/')
def redirect():
	return redirect(url_for('interface.dashboard'))

@interface_bp.route('/dashboard', methods=['GET'])
def dashboard():
	return render_template('dashboard.html')

@interface_bp.route('/runs', methods=['GET'])
def run_summaries():
	return render_template('run_summaries.html')

@interface_bp.route('/maps', methods=['GET'])
def maps():
	return render_template('maps.html')

@interface_bp.route('/profile', methods=['GET'])
def user_profile():
	return render_template('user.html')