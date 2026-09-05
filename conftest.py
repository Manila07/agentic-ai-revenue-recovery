import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

os.environ["DATABASE_URL"] = f"sqlite:///{os.path.join(tempfile.gettempdir(), 'revenue_test.db')}"

import pytest  # noqa: E402

@pytest.fixture(scope="session", autouse=True)
def _prepare_db():
    from app.database import Base, engine
    from app import models  # noqa: F401
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
