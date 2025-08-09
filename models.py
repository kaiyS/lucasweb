from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class Livro(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    livroname: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    genero: Mapped[str] = mapped_column(String(80), nullable=True)
    sinopse: Mapped[str] = mapped_column(String(1000), nullable=True)
    autor: Mapped[str] = mapped_column(String(100), nullable=True)
    ano_lancamento: Mapped[int] = mapped_column(Integer, nullable=True)
