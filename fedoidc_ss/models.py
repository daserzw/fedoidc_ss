from sqlalchemy import Column, Integer, Text
from fedoidc_ss.database import Base


class Entity(Base):
    __tablename__ = 'entities'
    id = Column(Integer, primary_key = True)
    issuer = Column(Text, unique=True)
    signing_keys = Column(Text, unique=True)

    def __init__(self, issuer=None, signing_keys=None):
        self.issuer = issuer
        self.signing_keys = signing_keys


class Superior(Base):
    __tablename__ = 'superiors'
    id = Column(Integer, primary_key = True)
    issuer = Column(Text, unique=True)
    uri = Column(Text, unique=True)
            
    def __init__(self, issuer=None, uri=None):
        self.issuer = issuer
        self.uri = uri

    
