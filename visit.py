from sqlalchemy import Column, Integer, UnicodeText, Date
from sqlalchemy import ForeignKey
import sql_base


class Visit(sql_base.Base):
    __tablename__ = "visits"
    id = Column(Integer, primary_key=True)
    notes = Column(UnicodeText)
    visit_type = Column(UnicodeText)
    cost = Column(Integer)
    cost_note = Column(UnicodeText)
    visit_length_min = Column(Integer)
    visit_date = Column(Date)
    billed = Column(Date)
    bolling_date = Column(Date)
    customer_id = Column(Integer, ForeignKey("customers.id"))

    def __init__(
        self,
        visit_type='',
        notes='',
        cost=0,
        cost_note='',
        visit_length_min=0,
        visit_date=0,
        customer_id='',
    ):
        self.billed = None
        self.visit_date = visit_date
        self.visit_length_min = visit_length_min
        self.notes = notes
        self.visit_type = visit_type
        self.cost = cost
        self.cost_note = cost_note
        self.customer_id = customer_id
