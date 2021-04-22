from sqlalchemy import Column, Integer, Float, DECIMAL, String, DATETIME, ForeignKey, BOOLEAN, Index, DATE
from sqlalchemy.orm import relationship
from sqlalchemy.orm.state import InstanceState
from sqlalchemy.ext.declarative import declarative_base


# 创建对象的基类:
Base = declarative_base()


class OMIM_DATA(Base):
    __tablename__ = 'omim'

    mim_number = Column(String(10), primary_key=True, comment='MIM Number')

    prefix = Column(String(1), comment='The prefix symbol')
    title = Column(String(50), comment='The title')
    references = Column(String(300), comment='The references')

    geneMap = Column(String(300), comment='The geneMap data')
    phenotypeMap = Column(String(300), comment='The phenotypeMap data')

    mim_type = Column(String(20), comment='The mim_type')
    entrez_gene_id = Column(String(20), comment='The entrez_gene_id')
    ensembl_gene_id = Column(String(20), comment='The ensembl_gene_id')
    hgnc_gene_symbol = Column(String(20), comment='The hgnc_gene_symbol')

    generated = Column(DATETIME, comment='The generated time')

    __table_args__ = (
        Index('search_by_gene', 'hgnc_gene_symbol'),
        Index('search_by_title', 'title'),
    )

    @property
    def as_dict(self):
        return {k: v for k, v in self.__dict__.items() if not isinstance(v, InstanceState)}

    def __str__(self):
        return '[{mim_number} - {title}]'.format(**self.__dict__)

    __repr__ = __str__


OMIM_DATA_COLUMNS = dict(OMIM_DATA.metadata.tables['omim'].columns)
