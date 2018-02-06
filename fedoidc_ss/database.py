import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

_basedir = os.path.abspath(os.path.dirname(__file__))


sqlite_db_path = 'sqlite:///' + os.path.join(_basedir, 'data/app.db')

engine = create_engine(sqlite_db_path,  convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
""":type: sqlalchemy.orm.Session"""


Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import fedoidc_ss.models
    Base.metadata.create_all(bind=engine)

    
