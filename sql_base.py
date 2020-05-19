from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import pathlib


db_path = (
        pathlib.Path.home()
        / 'terapialaskut.db'
    )
engine = create_engine('sqlite:///' + str(db_path))
Base = declarative_base(bind=engine)


def as_dict(self):
    dic = {c.name: getattr(self, c.name) for c in self.__table__.columns}

    for name, attr in self.__dict__.items():
        if 'InstrumentedList' in str(type(attr)):
            _list = []
            for item in attr:
                if hasattr(item, 'as_dict'):
                    _list.append(item.as_dict())

            dic[name] = _list

    return dic


Base.as_dict = as_dict
