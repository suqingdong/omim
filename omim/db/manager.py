import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.state import InstanceState

from omim.db.model import Base

from simple_loggers import SimpleLogger


class Manager(object):
    """
        uri:
            - sqlite:///relative/path/to/db
            - sqlite:////absolute/path/to/db
            - sqlite:///:memory:
    """
    def __init__(self, dbfile=':memory:', echo=False, drop=False, logger=None):
        self.drop = drop
        self.dbfile = dbfile
        self.uri = f'sqlite:///{dbfile}'
        self.logger = logger or SimpleLogger('Manager')
        self.engine = sqlalchemy.create_engine(self.uri, echo=echo)
        self.engine.logger.level = self.logger.level
        self.session = self.connect()
    
    def __enter__(self):
        self.create_table(drop=self.drop)
        return self

    def __exit__(self, *exc_info):
        self.session.commit()
        self.session.close()
        self.logger.debug('database closed.')

    def connect(self):
        DBSession = sessionmaker(bind=self.engine)
        return DBSession()

    def create_table(self, drop=False):
        if drop:
            Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)

    def query(self, Meta, key=None, value=None):
        query = self.session.query(Meta)
        if key:
            if key not in Meta.__dict__:
                self.logger.warning(f'unavailable key: {key}')
                return None
            else:
                query = query.filter(Meta.__dict__[key]==value)

        return query

    def delete(self, Meta, key, value):
        res = self.query(Meta, key, value)
        if res.count():
            self.logger.debug(f'delete one item: {res.first()}')
            res.delete()
        else:
            self.logger.debug(f'key input not in database: {key}={value}')

    def insert(self, Meta, key, datas, upsert=True):
        """
            upsert: add when key not exists, update when key exists
        """
        if isinstance(datas, Base):
            datas = [datas]

        for data in datas:
            res = self.query(Meta, key, data.__dict__[key])
            if not res.first():
                self.logger.debug(f'>>> insert data: {data}')
                self.session.add(data)
            elif upsert:
                self.logger.debug(f'>>> update data: {data}')
                context = {k: v for k, v in data.__dict__.items() if not isinstance(v, InstanceState)}
                res.update(context)
