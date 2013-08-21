"""database.py

Handles the database connection
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bmr_statbot import config


url = "postgresql://{0}:{1}@{2}/{3}".format(config.db_user,
                                            config.db_password,
                                            config.db_address,
                                            config.db_name)

engine = create_engine(url)
Session = sessionmaker(bind=engine)