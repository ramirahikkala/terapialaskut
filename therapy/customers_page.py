import re
import time
import datetime
from PySide2 import QtCore, QtGui
from PySide2.QtCore import QDateTime
import PySide2.QtWidgets as qt
from PySide2.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QMessageBox,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QDateEdit,
    QLineEdit,
)

import customer
from custom_tree_widget import MyTreeWidget

class MainPage(qt.QWidget):
    def __init__(self, db_session, **kwargs):
        super(MainPage, self).__init__()
        self.db_session = db_session

        central_widget = QWidget()
        central_widget.setStyleSheet("background: white;")

        # Create main grid layout that will organize everything
        main_grid = qt.QGridLayout(central_widget)

        main_grid.setSpacing(0)
        main_grid.setMargin(0)

        self.setLayout(main_grid)

        self.list_of_customers = qt.QTreeWidget()

        self.list_of_customers.setColumnCount(3)
        self.list_of_customers.setHeaderLabels(
            [
                "Nimi",
                "Osoite",
                "Puhelin",
                "Hetu",
                "Sähköposti",
                "Nick Name",
                "Tuntihinta",
                "Laskutustapa",
                "Aktiivinen",
            ]
        )
        self.list_of_customers.setSortingEnabled(True)

        # Allow multiselect
        self.list_of_customers.setSelectionMode(qt.QAbstractItemView.ExtendedSelection)

        third_stupid_widget = QWidget()

        right_side_layout = qt.QVBoxLayout(third_stupid_widget)

        main_grid.addWidget(third_stupid_widget, 0, 1)

        self.update_page()

        self.new_customer_button = qt.QPushButton("Lisää asiakas")

        second_stupid_widget = QWidget()
        new_visit_layout = QHBoxLayout(second_stupid_widget)
        right_side_layout.addWidget(second_stupid_widget)
        new_visit_layout.addWidget(self.new_customer_button)

        right_side_layout.addWidget(self.list_of_customers)
        # Add properties view
        # main_grid.addWidget(qt.QPlainTextEdit(), 0, 2)

        def new_customer_handler():
            db_session.add(customer.Customer("", "Z Asiakas", "" "", "", "", 0, ""))
            db_session.commit()
            self.update_page()

        self.new_customer_button.clicked.connect(new_customer_handler)

    def update_page(self):
        self.list_of_customers.clear()
        self.customers = self.db_session.query(customer.Customer).all()

        for _customer in self.customers:
            cell_objects = {
                0: 'name',
                1: 'street_address',
                2: 'phone_number',
                3: 'id_number',
                4: 'email',
                5: 'nick_name',
                6: 'hour_price',
                7: 'way_of_billing',
                8: 'active',

            }

            MyTreeWidget(
                self.list_of_customers,
                [
                    _customer.name,
                    _customer.street_address,
                    _customer.phone_number,
                    _customer.id_number,
                    _customer.email,
                    _customer.nick_name,
                    str(_customer.hour_price),
                    _customer.way_of_billing,
                    str(_customer.active),
                ],
                cell_objects=cell_objects,
                db_session=self.db_session,
                id=_customer.id,
                class_item=customer.Customer
            )
