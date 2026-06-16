from sqlalchemy import MetaData, BigInteger, String
from sqlalchemy.orm import DeclarativeBase, mapped_column

metadata = MetaData()


class Base(DeclarativeBase):
    pass


class ChatLanguages(Base):
    __tablename__ = "chat_languages"

    chat_id = mapped_column(BigInteger, primary_key=True)
    lang = mapped_column(String)
