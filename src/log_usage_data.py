import os
import sys
import logging
import logging.config

from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import config
from helpers import create_connection, get_session
import argparse

logging.config.fileConfig(config.LOGGING_CONFIG)
logger = logging.getLogger('sportco-models')

Base = declarative_base()


class Tweet(Base):
    """ Defines the data model for the table `tweet`. """

    __tablename__ = 'tweet'

    tweet_id = Column(String(100), primary_key=True, unique=True, nullable=False)
    timestamp = Column(String(100), unique=False, nullable=False)
    username = Column(String(100), unique=False, nullable=False)
    message = Column(Text, unique=False, nullable=False)

    def __repr__(self):
        tweet_repr = "<Tweet(tweet_id='%s', timestamp='%s', username='%s', message='%s')>"
        return tweet_repr % (self.tweet_id, self.timestamp, self.username, self.message)


# ADD CLASS FOR TWEET SCORE TABLE HERE
class Tweet_Table(Base):
    """ Defines the data model for the table `tweet_table`. """

    __tablename__ = 'tweet_score'

    tweet_id = Column(String(100), primary_key=True, unique=True, nullable=False)
    score = Column(Integer, unique=False, nullable=True)
    
    def __repr__(self):
        tweet_repr = "<Tweet(tweet_id='%s', score='%d')>"
        return tweet_repr % (self.tweet_id, self.score)


def _truncate_tweet_score(session):
    """Deletes tweet scores table if rerunning and run into unique key error."""

    session.execute('''DELETE FROM tweet_score''')


def create_db(engine=None, engine_string=None):
    """Creates a database with the data models inherited from `Base` (Tweet and TweetScore).

    Args:
        engine (:py:class:`sqlalchemy.engine.Engine`, default None): SQLAlchemy connection engine.
            If None, `engine_string` must be provided.
        engine_string (`str`, default None): String defining SQLAlchemy connection URI in the form of
            `dialect+driver://username:password@host:port/database`. If None, `engine` must be provided.

    Returns:
        None
    """
    if engine is None and engine_string is None:
        return ValueError("`engine` or `engine_string` must be provided")
    elif engine is None:
        engine = create_connection(engine_string=engine_string)

    Base.metadata.create_all(engine)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create defined tables in database")
    parser.add_argument("--truncate", "-t", default=False, action="store_true",
                        help="If given, delete current records from tweet_scores table before create_all "
                             "so that table can be recreated without unique id issues ")
    args = parser.parse_args()

    # If "truncate" is given as an argument (i.e. python models.py --truncate), then empty the tweet_score table)
    if args.truncate:
        session = get_session(engine_string=config.SQLALCHEMY_DATABASE_URI)
        try:
            logger.info("Attempting to truncate tweet_score table.")
            _truncate_tweet_score(session)
            session.commit()
            logger.info("tweet_score truncated.")
        except Exception as e:
            logger.error("Error occurred while attempting to truncate tweet_score table.")
            logger.error(e)
        finally:
            session.close()

    create_db(engine_string=config.SQLALCHEMY_DATABASE_URI)
