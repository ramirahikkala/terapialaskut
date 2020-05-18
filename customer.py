from sqlalchemy import Column, Integer, UnicodeText, Float, Boolean
from sqlalchemy.orm import relationship
import person
import sql_base
import visit


class Customer(person.Person, sql_base.Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    name = Column(UnicodeText)
    street_address = Column(UnicodeText)
    phone_number = Column(UnicodeText)
    id_number = Column(UnicodeText)
    nick_name = Column(UnicodeText)
    hour_price = Column(Float)
    active = Column(Boolean)
    email = Column(UnicodeText)
    way_of_billing = Column(UnicodeText)
    visits = relationship("visit.Visit", backref='customers')

    def __init__(
        self, nick_name, name, street_address, phone_number, id_number, hour_price, email
    ):
        super().__init__(name, street_address, phone_number, id_number, email)
        self.hour_price = hour_price
        self.nick_name = nick_name
        self.visits = []
        self.active = True
        self.way_of_billing = ""

    def new_visit(
        self, **kwargs
    ):
        self.visits.append(visit.Visit(customer_id=self.name, **kwargs))

    def unbilled_visits(self):
        return [visit for visit in self.visits if not visit.billed]

    def unbilled_time(self):
        dates = [visit.visit_date for visit in self.unbilled_visits()]
        return str(min(dates).strftime("%d.%m.%Y")) + ' - ' + str(max(dates).strftime("%d.%m.%Y"))

    def unbilled_total(self):
        costs = [int(visit.cost) for visit in self.unbilled_visits()]
        return sum(costs)

    def number_of_unbilled(self):
        return len(self.unbilled_visits())
