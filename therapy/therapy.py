import sys
import visits_page
import customers_page
import therapist_page
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import PySide2.QtWidgets as qt
import pdf_writer
import customer
import therapist
import sql_base
from PySide2.QtWidgets import (
    QTabWidget,
    )

sql_base.Base.metadata.create_all()


Session = sessionmaker(bind=sql_base.engine)
s = Session()

app = qt.QApplication(sys.argv)

visits = visits_page.MainPage(s)
customers = customers_page.MainPage(s)
therapist = therapist_page.MainPage(s)

def onTabChange(*args, **kwargs):
    visits.update_page()
    customers.update_page()
    therapist.update_page()


tabWidget = QTabWidget()
tabWidget.addTab(visits, "Käynnit")
tabWidget.addTab(customers, "Asiakkaat")
tabWidget.addTab(therapist, "Terapeutti")
tabWidget.currentChanged.connect(onTabChange)
tabWidget.showMaximized()
tabWidget.setWindowTitle("Terapiakäynnit")


tabWidget.show()
exit_code = app.exec_()
sys.exit(exit_code)

'''
https://stackoverflow.com/questions/2047814/is-it-possible-to-store-python-class-objects-in-sqlite
https://gist.github.com/minorsecond/93706951d2dbdecf0c44
https://docs.sqlalchemy.org/en/13/_modules/examples/association/basic_association.html
'''