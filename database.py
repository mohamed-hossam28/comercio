"""Database setup using SQLAlchemy.

Creates an engine, session factory and a declarative base. Call
`init_db()` to create tables from ORM models.
"""
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Generator

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./db.sqlite3")

# SQLite needs check_same_thread=False for use with multiple threads
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def init_db():
	"""Import all modules that define models so they are registered with
	`Base`, then create all tables."""
	# Import models so they are registered on Base.metadata
	try:
		import models.users  # noqa: F401
		import models.products  # noqa: F401
	except Exception:
		# If imports fail, continue silently — errors will surface when models are used
		pass

	Base.metadata.create_all(bind=engine)


def get_db() -> Generator:
	"""Yield a SQLAlchemy DB session, suitable for FastAPI dependencies.

	Usage in FastAPI endpoints:
		from fastapi import Depends
		from database import get_db

		def endpoint(db: Session = Depends(get_db)):
			...
	"""
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()

