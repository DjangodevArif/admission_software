from sqlalchemy import inspect
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String, Text
from sqlalchemy_file.types import ImageField

# from db import Base


@as_declarative()
class Base:
    def _asdict(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}


class Students(Base):
    __tablename__ = 'student'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30))
    father_name = Column(String(30))
    mother_name = Column(String(15))
    permanent_address = Column(String(150))
    present_address = Column(String(150))
    description = Column(Text())
    image = Column(ImageField())

    def __repr__(self):
        return f"Student- {self.id} {self.name}"
