import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from starlette.testclient import TestClient

from models.models import Base, get_db
from main import app

test_ALCHEMY_URL = "sqlite:///test_gg_db.db"

test_engine = create_engine(test_ALCHEMY_URL)

test_SessonLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

Base.metadata.bind = test_engine


def test_get_db():
    with test_SessonLocal() as session:
        yield session


app.dependency_overrides = {get_db: test_get_db}


@pytest.fixture(autouse=True, scope="session")
def prepare_database():

    try:
        Base.metadata.create_all(bind=test_engine)
        yield  # This is where the test runs

    finally:
        Base.metadata.drop_all(bind=test_engine)


client = TestClient(app)
