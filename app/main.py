from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, create_engine, Field, Session, select
from app import settings
from contextlib import asynccontextmanager
from typing import Annotated


class ToDo(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    description: str


connection_string = str(settings.DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg"
)

engine = create_engine(connection_string, echo=True)

def create_tables():
    # print("DB_URL\n", connection_string)
    SQLModel.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating Tables...")
    create_tables()
    yield

app: FastAPI = FastAPI(lifespan=lifespan)


def get_session():
    with Session(engine) as session:
        yield session


@app.get("/")
def read_root():
    return {"Hello": "World"}

# Create todos
@app.post("/todos", response_model=ToDo)
def create_todo(todo_content: ToDo, session: Annotated[Session, Depends(get_session)]):
    session.add(todo_content)
    session.commit()
    session.refresh(todo_content)
    return todo_content

# get todos
@app.get("/todo", response_model=list[ToDo])
def get_todo(session: Annotated[Session, Depends(get_session)]):
    statement = select(ToDo)
    # statement = select(ToDo).where(ToDo.id == 1)
    todo = session.exec(statement)
    return todo

# update todos
@app.put("/todo/{id}", response_model=ToDo)
def update_todo(id: int, todo_content: ToDo, session: Annotated[Session, Depends(get_session)]):
    todo = session.get(ToDo, id)
    todo.title = todo_content.title
    todo.description = todo_content.description
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo

# delete todo
@app.delete("/todo/{id}")
def delete_todo(id: int, session: Annotated[Session, Depends(get_session)]):
    todo = session.get(ToDo, id)
    session.delete(todo)
    session.commit()
    return {"message": "Todo deleted successfully"}


# delete table
# @app.delete("/todos")
# def delet_table():
#     with Session(engine) as session:
#         model_to_delete = SQLModel.metadata.tables['courses']
#         SQLModel.metadata.drop_all(bind=engine, tables=[model_to_delete])
#         session.commit()
