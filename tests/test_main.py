from sqlmodel import create_engine, Session
from fastapi.testclient import TestClient
from app.main import app, get_session, ToDo
from app import settings
from sqlmodel import SQLModel


def test_write_main():
    connection_string = str(settings.TEST_DATABASE_URL).replace("postgresql", "postgresql+psycopg")
    engine = create_engine(connection_string, connect_args={"sslmode" : "require"}, pool_recycle=300, echo=True)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        def get_session_override():
            return session
        
        app.dependency_overrides[get_session] = get_session_override

        client = TestClient(app = app)

        todo_content = {"title" : "buy bread", "description" : "buy bread from market"}

        response = client.post("/todo", json={"content": todo_content})
        data = response.json()

        assert response.status_code == 200
        assert data["content"] == todo_content

def test_read_list_main():
    connection_string = str(settings.TEST_DATABASE_URL).replace("postgresql", "postgresql+psycopg")
    engine = create_engine(connection_string, connect_args={"sslmode" : "require"}, pool_recycle=300, echo=True)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        def get_session_override():
            return session
        
        app.dependency_overrides[get_session] = get_session_override

        client = TestClient(app = app)

        response = client.get("/todo")

        assert response.status_code == 200
    
# client = TestClient(app = app)

# def test_root_path():
#     response = client.get("/")

#     assert response.status_code == 200
#     assert response.json() == {"message": "Hello World"}

# def test_root_path_1():
#     response = client.get("/")

#     assert response.status_code == 200  
#     assert response.json() == {"message": "Hello"}