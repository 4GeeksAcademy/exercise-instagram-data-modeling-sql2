import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

# Tabla de asociación para la relación muchos-a-muchos entre usuarios (seguidores)
follower_association_table = Table('follower', Base.metadata,
    Column('user_from_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('user_to_id', Integer, ForeignKey('user.id'), primary_key=True)
)

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False)
    firstname = Column(String(250), nullable=False)
    lastname = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    
    posts = relationship('Post', backref='user')
    comments = relationship('Comment', backref='user')
    media = relationship('Media', backref='user')

    # Relación muchos-a-muchos para seguidores
    followed = relationship(
        'User',
        secondary=follower_association_table,
        primaryjoin=id == follower_association_table.c.user_from_id,
        secondaryjoin=id == follower_association_table.c.user_to_id,
        backref='followers',
        lazy='dynamic'
    )

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    
    comments = relationship('Comment', backref='post')
    media = relationship('Media', backref='post')

class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    comment_text = Column(String(250), nullable=False)
    author_id = Column(Integer, ForeignKey('user.id'))
    post_id = Column(Integer, ForeignKey('post.id'))

class Media(Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True)
    type = Column(Integer, nullable=False)
    url = Column(String(250), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'))



try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem generating the diagram")
    raise e
