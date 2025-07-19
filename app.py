from bottle import Bottle, run, request, redirect, template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Asset, Vulnerability, Incident, SIEMEvent, IncidentEvent

# Initialize Bottle app
app = Bottle()

# Initialize database session
engine = create_engine('sqlite:///siem.db')
Session = sessionmaker(bind=engine)

# Home page with navigation
@app.route('/')
def index():
    return template('''
    <h1>SIEM Dashboard</h1>
    <ul>
      <li><a href="/assets">Assets</a></li>
      <li><a href="/vulnerabilities">Vulnerabilities</a></li>
      <li><a href="/events">SIEM Events</a></li>
      <li><a href="/incidents">Incidents</a></li>
    </ul>
    ''')

# List all assets
@app.route('/assets')
def list_assets():
    session = Session()
    assets = session.query(Asset).all()
    return template('''
    <h2>Assets</h2>
    <ul>
    % for a in assets:
      <li><a href="/assets/{{a.asset_id}}">{{a.hostname}}</a></li>
    % end
    </ul>
    ''', assets=assets)

# Show asset details
@app.route('/assets/<id:int>')
def show_asset(id):
    session = Session()
    asset = session.query(Asset).get(id)
    if not asset:
        return "Asset not found"
    vulnerabilities = session.query(Vulnerability).filter_by(asset_id=id).all()
    events = session.query(SIEMEvent).filter_by(asset_id=id).all()
    incident_links = session.query(IncidentEvent).filter_by(event_id=None).all()  # placeholder for join filtering
    # Correctly fetch incidents via association
    incident_links = session.query(IncidentEvent).filter_by(event_id=None).all()  # remove placeholder if unnecessary
    # For simplicity, query via asset.events
    incidents = []
    for evt in events:
        for inc in evt.incidents:
            if inc not in incidents:
                incidents.append(inc)
    return template('''
    <h2>Asset: {{asset.hostname}}</h2>
    <p><strong>ID:</strong> {{asset.asset_id}}</p>
    <p><strong>IP Address:</strong> {{asset.ip_address}}</p>
    <p><strong>Device Type:</strong> {{asset.device_type}}</p>
<h3>Vulnerabilities</h3>
<ul>
% if vulnerabilities:
    % for v in vulnerabilities:
        <li>{{v.description}} (Score: {{v.score}})</li>
    % end
% else:
    <li>No vulnerabilities</li>
% end
</ul>

<h3>SIEM Events</h3>
<ul>
% if events:
    % for e in events:
        <li>{{e.event_type}} at {{e.timestamp}}</li>
    % end
% else:
    <li>No events</li>
% end
</ul>

<h3>Incidents</h3>
% if incidents:
    <ul>
    % for inc in incidents:
        <li><a href="/incidents/{{inc.incident_id}}">{{inc.title}}</a></li>
    % end
    </ul>
% else:
    <p>No incidents</p>
% end
    ''', asset=asset, vulnerabilities=vulnerabilities, events=events, incidents=incidents)

# List vulnerabilities
@app.route('/vulnerabilities')
def list_vulns():
    session = Session()
    vulns = session.query(Vulnerability).all()
    return template('''
    <h2>Vulnerabilities</h2>
    <ul>
    % for v in vulns:
      <li>Asset {{v.asset_id}}: {{v.description}} (Score: {{v.score}})</li>
    % end
    </ul>
    ''', vulns=vulns)

# List SIEM events
@app.route('/events')
def list_events():
    session = Session()
    events = session.query(SIEMEvent).all()
    return template('''
    <h2>SIEM Events</h2>
    <ul>
    % for e in events:
      <li>Asset {{e.asset_id}} - {{e.event_type}} at {{e.timestamp}}</li>
    % end
    </ul>
    ''', events=events)

# List incidents
@app.route('/incidents')
def list_incidents():
    session = Session()
    incidents = session.query(Incident).all()
    return template('''
    <h2>Incidents</h2>
    <ul>
    % for inc in incidents:
      <li><a href="/incidents/{{inc.incident_id}}">{{inc.title}}</a> (Status: {{inc.status}})</li>
    % end
    </ul>
    ''', incidents=incidents)

# Show incident details
@app.route('/incidents/<id:int>')
def show_incident(id):
    session = Session()
    inc = session.query(Incident).get(id)
    if not inc:
        return "Incident not found"
    events = inc.events
    return template('''
    <h2>Incident: {{inc.title}}</h2>
    <p><strong>Description:</strong> {{inc.description}}</p>
    <p><strong>Status:</strong> {{inc.status}}</p>
    <h3>Related Events</h3>
    <ul>
    % for e in events:
      <li>{{e.event_type}} on Asset {{e.asset_id}} at {{e.timestamp}}</li>
    % else:
      <li>No related events</li>
    % end
    </ul>
    ''', inc=inc, events=events)

# Run the application
if __name__ == '__main__':
    run(app, host='0.0.0.0', port=8080, reloader=True)
