from sqlalchemy import Column, Integer, Text, DateTime, Index
from calamari_common.db.base import Base


class Event(Base):
    """
    Events generated by the Cthulhu Eventer.
    """
    __tablename__ = 'cthulhu_event'

    id = Column(Integer, autoincrement=True, primary_key=True)

    # Time at which event was synthesized by Eventer
    when = Column(DateTime(timezone=True))

    severity = Column(Integer)

    # Human readable message
    message = Column(Text)

    # Optionally associated with a cluster
    fsid = Column(Text, nullable=True)
    # Optionally associated with a server
    fqdn = Column(Text, nullable=True)
    # Optionally associated with a service type ('osd', 'mon', 'mds') (FSID must be set)
    service_type = Column(Text, nullable=True)
    # Optionally associate with a particular service (service_type must be set)
    service_id = Column(Text, nullable=True)

    __table_args__ = (
        # For looking up by specific service
        Index('ix_cthulhu_event_fsid_type_id', "fsid", "service_type", "service_id"),
        # For looking up events for one cluster
        Index('ix_cthulhu_event_fsid', "fsid"),
        # For looking up events for one server
        Index('ix_cthulhu_event_fqdn', "fqdn"),
        # For looking up events less than a certain severity
        Index('ix_cthulhu_event_severity', "severity")
    )

    def __repr__(self):
        return "<Event %s @ %s>" % (self.id, self.when)
