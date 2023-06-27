from sqlalchemy import Column, Integer, UnicodeText, Float
import person
import sql_base


class Therapist(person.Person, sql_base.Base):
    __tablename__ = 'therapists'
    id = Column(Integer, primary_key=True)
    name = Column(UnicodeText)
    company_name = Column(UnicodeText)
    street_address = Column(UnicodeText)
    phone_number = Column(UnicodeText)
    id_number = Column(UnicodeText)
    iban = Column(UnicodeText)
    bic = Column(UnicodeText)
    email = Column(UnicodeText)
    kelakorvaus = Column(Float)

    def __init__(
        self, company_name, name, street_address, phone_number, id_number, iban, bic, email, kelakorvaus
    ):
        super().__init__(name, street_address, phone_number, id_number, email)
        self.iban = iban
        self.bic = bic
        self.company_name = company_name
        self.kelakorvaus = kelakorvaus

