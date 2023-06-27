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

import therapist
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

        # Yet again interesting design decision. On QT you cannot set style for layout.

        self.list_of_therapists = qt.QTreeWidget()

        self.list_of_therapists.setHeaderLabels(
            [
                "Nimi",
                "Yrityksen nimi",
                "Osoite",
                "Puhelin",
                "Y-tunnus",
                "Sähköposti",
                "Kelakorvaus",
            ]
        )
        self.list_of_therapists.setSortingEnabled(True)

        # Allow multiselect
        self.list_of_therapists.setSelectionMode(qt.QAbstractItemView.ExtendedSelection)

        third_stupid_widget = QWidget()

        right_side_layout = qt.QVBoxLayout(third_stupid_widget)

        main_grid.addWidget(third_stupid_widget, 0, 1)

        self.update_page()

        right_side_layout.addWidget(self.list_of_therapists)
        # Add properties view
        # main_grid.addWidget(qt.QPlainTextEdit(), 0, 2)

    def update_page(self):
        self.list_of_therapists.clear()
        self.therapist = self.db_session.query(therapist.Therapist).all()

        if not self.therapist:
            self.db_session.add(
                therapist.Therapist(
                    company_name="",
                    name="Uusi Terapeutti",
                    street_address="",
                    phone_number="",
                    id_number="",
                    iban="",
                    bic="",
                    email="",
                    kelakorvaus=0,
                )
            )

        for _therapist in self.therapist:
            cell_objects = {
                0: 'name',
                1: 'company_name',
                2: 'street_address',
                3: 'phone_number',
                4: 'id_number',
                5: 'email',
                6: 'kelakorvaus',
            }

            MyTreeWidget(
                self.list_of_therapists,
                [
                    _therapist.name,
                    _therapist.company_name,
                    _therapist.street_address,
                    _therapist.phone_number,
                    _therapist.id_number,
                    _therapist.email,
                    _therapist.kelakorvaus,
                ],
                cell_objects=cell_objects,
                db_session=self.db_session,
                id=_therapist.id,
                class_item=therapist.Therapist,
            )
