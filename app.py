from bottle import Bottle, run, template, static_file, request, redirect
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from models import Base, User, Asset, SIEMEvent, Vulnerability, Incident
from bottle import TEMPLATE_PATH
import os
from collections import Counter, defaultdict
from datetime import datetime
import json

# Nastavi pot do template map
TEMPLATE_PATH.insert(0, os.path.join(os.path.dirname(__file__), 'templates'))

# Inicializiraj Bottle aplikacijo
app = Bottle()

# Povezava z SQLite bazo
engine = create_engine('sqlite:///siem.db')
Session = sessionmaker(bind=engine)
session = Session()

@app.route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='static')

@app.route('/')
def dashboard():
    users_count = session.query(User).count()
    assets_count = session.query(Asset).count()
    events_count = session.query(SIEMEvent).count()
    vulns_count = session.query(Vulnerability).count()
    incidents = session.query(Incident).all()

    # Pie chart (incident types)
    incident_stats = Counter([inc.title for inc in incidents])

    # Histogram (incident counts per month)
    monthly_stats = defaultdict(int)
    for inc in incidents:
        if inc.created_date:
            key = inc.created_date.strftime('%Y-%m')
            monthly_stats[key] += 1

    return template('index.tpl',
                    users_count=users_count,
                    assets_count=assets_count,
                    events_count=events_count,
                    vulns_count=vulns_count,
                    incidents=incidents,
                    incident_stats=incident_stats,
                    monthly_stats=monthly_stats,
                    json=json)

@app.route('/incidents')
def list_incidents():
    page = int(request.query.get('page', 1))
    per_page = 40
    sort = request.query.get('sort', 'created_date')
    order = request.query.get('order', 'desc')

    q = session.query(Incident)
    if sort == 'severity':
        q = q.order_by(desc(Incident.status))  # adjust if severity exists
    else:
        q = q.order_by(desc(getattr(Incident, sort)))

    total = q.count()
    incidents = q.offset((page - 1) * per_page).limit(per_page).all()

    return template('incidents.tpl',
                    incidents=incidents,
                    page=page,
                    total=total,
                    per_page=per_page)

@app.route('/users')
def list_users():
    page = int(request.query.get('page', 1))
    per_page = 50
    total = session.query(User).count()
    users = session.query(User).offset((page-1)*per_page).limit(per_page).all()
    return template('users.tpl', users=users, page=page, total=total, per_page=per_page)


@app.route('/assets')
def list_assets():
    page = int(request.query.get('page', 1))
    per_page = 50
    total = session.query(Asset).count()
    assets = session.query(Asset).offset((page-1)*per_page).limit(per_page).all()
    return template('assets.tpl', assets=assets, page=page, total=total, per_page=per_page)


@app.route('/events')
def list_events():
    events = session.query(SIEMEvent).all()
    return template('events.tpl', events=events)

@app.route('/vulnerabilities')
def list_vulns():
    vulns = session.query(Vulnerability).all()
    return template('vulnerabilities.tpl', vulns=vulns)

if __name__ == '__main__':
    run(app, host='localhost', port=8080, debug=True, reloader=True)