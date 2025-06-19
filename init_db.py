import os
import csv
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Asset, Vulnerability, SIEMEvent, Incident, User

# Path configuration
dir_path = os.path.dirname(os.path.realpath(__file__))
db_path = os.path.join(dir_path, 'siem.db')
csv_dir = os.path.join(dir_path, 'data')

# Create engine and session
engine = create_engine(f'sqlite:///{db_path}', echo=True)
Session = sessionmaker(bind=engine)

# Initialize database schema
def init_schema():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    print("Initialized SQLite database at:", db_path)

# Helper to parse dates
def parse_datetime(s):
    return datetime.fromisoformat(s) if s else None

# Load CSV into table
def load_csv(model, filename, mapper):
    file_path = os.path.join(csv_dir, filename)
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            obj = mapper(row)
            session.add(obj)
    session.commit()
    print(f"Loaded data from {filename}")

# Mappers for each model
def map_asset(row):
    return Asset(
        asset_id=int(row['asset_id']),
        hostname=row['hostname'],
        ip_address=row['ip_address'],
        device_type=row.get('device_type'),
        location=row.get('location')
    )

def map_vulnerability(row):
    return Vulnerability(
        vuln_id=int(row['vuln_id']),
        cve_id=row['cve_id'],
        description=row.get('description'),
        score=int(row['score']),
        status=row['status'],
        discovered_date=parse_datetime(row['discovered_date']),
        fixed_date=parse_datetime(row['fixed_date']),
        asset_id=int(row['asset_id'])
    )

def map_siem_event(row):
    return SIEMEvent(
        event_id=int(row['event_id']),
        timestamp=parse_datetime(row['timestamp']),
        event_type=row.get('event_type'),
        severity=int(row['severity']),
        message=row.get('message'),
        asset_id=int(row['asset_id'])
    )

def map_user(row):
    return User(
        user_id=int(row['user_id']),
        name=row.get('name'),
        role=row.get('role'),
        email=row.get('email')
    )

def map_incident(row):
    # Note: We'll link incidents to events via join table later or CSV includes event IDs
    return Incident(
        incident_id=int(row['incident_id']),
        title=row.get('title'),
        description=row.get('description'),
        created_date=parse_datetime(row['created_date']),
        status=row.get('status'),
        assigned_to_id=int(row['assigned_to_id']) if row.get('assigned_to_id') else None
    )

if __name__ == '__main__':
    # Create DB and tables
    init_schema()
    session = Session()

    # Load base entities
    load_csv(Asset, 'assets.csv', map_asset)
    load_csv(Vulnerability, 'vulnerabilities.csv', map_vulnerability)
    load_csv(User, 'users.csv', map_user)
    load_csv(SIEMEvent, 'siem_events.csv', map_siem_event)
    load_csv(Incident, 'incidents.csv', map_incident)

    # TODO: If you have a CSV with incident-event mappings, load into join table here
    print("Database population complete.")
