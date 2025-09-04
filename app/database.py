from databases import Database
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv() 

DATABASE_URL = os.getenv("DATABASE_URL")

database = Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)
metadata = MetaData()

Base = declarative_base(metadata=metadata)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
