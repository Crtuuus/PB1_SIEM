from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# Association table for many-to-many relationship between Incident and SIEMEvent
incident_event_table = Table(
    'incident_event', Base.metadata,
    Column('incident_id', Integer, ForeignKey('incident.incident_id'), primary_key=True),
    Column('event_id', Integer, ForeignKey('siem_event.event_id'), primary_key=True)
)

class Asset(Base):
    __tablename__ = 'asset'
    asset_id = Column(Integer, primary_key=True)
    hostname = Column(String, nullable=False)
    ip_address = Column(String, nullable=False)
    device_type = Column(String)
    location = Column(String)

    vulnerabilities = relationship('Vulnerability', back_populates='asset')
    events = relationship('SIEMEvent', back_populates='asset')

class Vulnerability(Base):
    __tablename__ = 'vulnerability'
    vuln_id = Column(Integer, primary_key=True)
    cve_id = Column(String, nullable=False)
    description = Column(String)
    score = Column(Integer)
    status = Column(String)  # e.g., 'open', 'under investigation', 'fixed'
    discovered_date = Column(DateTime)
    fixed_date = Column(DateTime, nullable=True)

    asset_id = Column(Integer, ForeignKey('asset.asset_id'))
    asset = relationship('Asset', back_populates='vulnerabilities')

class SIEMEvent(Base):
    __tablename__ = 'siem_event'
    event_id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False)
    event_type = Column(String)
    severity = Column(Integer)
    message = Column(String)

    asset_id = Column(Integer, ForeignKey('asset.asset_id'))
    asset = relationship('Asset', back_populates='events')
    incidents = relationship('Incident', secondary=incident_event_table, back_populates='events')

class User(Base):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True)
    name = Column(String)
    role = Column(String)
    email = Column(String)

    incidents = relationship('Incident', back_populates='assigned_to')

class Incident(Base):
    __tablename__ = 'incident'
    incident_id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    created_date = Column(DateTime)
    status = Column(String)  # e.g., 'open', 'in progress', 'resolved'
    assigned_to_id = Column(Integer, ForeignKey('user.user_id'))

    assigned_to = relationship('User', back_populates='incidents')
    events = relationship('SIEMEvent', secondary=incident_event_table, back_populates='incidents')
