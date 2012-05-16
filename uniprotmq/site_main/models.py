from django.db import models
from django.conf import settings
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy.orm as orm
from uniprotmq.site_main.idparser import get_id_type

# Create your models here.

Base = declarative_base()

class Entry(Base):
    __tablename__ = 'entries'
    id = Column(String(16), primary_key=True)
    description = Column(Text)

class IDMapping(Base):
    __tablename__ = 'idmapping'
    __table_args__ = (
        PrimaryKeyConstraint('id', 'resource', 'value'),
    )
    id = Column(String(16), ForeignKey(Entry.id))
    resource = Column(String(16))
    value = Column(String(24))
    is_primary = Column(Boolean)

class UniProtInterface:
    def __init__(self, db_name):
        self.db_name = db_name
        dbpath = 'mysql://%s:%s@%s:%s/%s' % (settings.MYDB_USERNAME, settings.MYDB_PASSWORD, settings.MYDB_HOSTNAME, settings.MYDB_PORT, db_name)
        self.engine = create_engine(dbpath, echo=settings.MYDB_ECHO)
        Session = orm.scoped_session(orm.sessionmaker(bind=self.engine))
        self.session = Session()

UNIPROT_DATABASES = dict([(x, UniProtInterface(x)) for x in settings.MYDB_NAMES])
