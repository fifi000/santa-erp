import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from db.config import get_session
from db.models import Elf
from api.config import app


@pytest.fixture(name='session')
def session_fixture():
    engine = create_engine(
        'sqlite://', connect_args={'check_same_thread': False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name='client')
def client_fixture(session: Session):
    app.dependency_overrides[get_session] = lambda: session
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_create_elf(client: TestClient):
    response = client.post(
        '/elves/',
        json={'name': 'John'}
    )
    data = response.json()

    assert response.status_code == 200
    assert data['name'] == 'John'


def test_read_elves(session: Session, client: TestClient):
    elf1 = Elf(name='John')
    elf2 = Elf(name='Paul')

    session.add(elf1)
    session.add(elf2)
    session.commit()

    response = client.get('/elves/')
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]['name'] == 'John'
    assert data[1]['name'] == 'Paul'
