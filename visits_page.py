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
import visit
from custom_tree_widget import MyTreeWidget

class MainPage(qt.QWidget):

    def __init__(self, db_session, **kwargs):
        super(MainPage, self).__init__()
        self.db_session = db_session

        # Create central widget that will contain everything
        # (Bit odd design decision from QT, I would say, to separate widgets and
        # layouts. Now we need to have central _widget_ to contain layout to contain
        # widgets)
        central_widget = QWidget()
        central_widget.setStyleSheet("background: white;")

        # Add central widget to main window

        # Create main grid layout that will organize everything
        main_grid = qt.QGridLayout(central_widget)

        self.setLayout(main_grid)

        main_grid.setSpacing(0)
        main_grid.setMargin(0)

        # Yet again interesting design decision. On QT you cannot set style for layout.
        # Thus, we create widget that will contain layout and now we can set style for the widget.

        widget_that_would_not_be_needed_if_qt_would_not_be_so_stupid = QWidget()

        widget_that_would_not_be_needed_if_qt_would_not_be_so_stupid.setStyleSheet(
            '''
            QObject { background: #FF005AA1; }
            QPushButton {
                background: #FF005AA1;
                color: white;
                text-align: center;
                border: none;
                font-weight: 500;
                font-size: 15px;
                height: 48px;
                width: 120px;
            }
            QPushButton:hover {
               background-color: #FF014a82;
            }
            QPushButton:checked {
            background: #FF01508c;
            }
            QPushButton:pressed {
                color: #FF005AA1;
                background: white;
            }
            QWidget{
                background: #FF005AA1;
            }
            '''
        )

        # On left side we will have some (or at least one) button
        left_side_buttons = QVBoxLayout(
            widget_that_would_not_be_needed_if_qt_would_not_be_so_stupid
        )

        left_side_buttons.setSpacing(0)
        left_side_buttons.setMargin(0)

        # And add it to main box the left most cell
        main_grid.addWidget(widget_that_would_not_be_needed_if_qt_would_not_be_so_stupid, 0, 0)

        main_grid.setRowStretch(0, 1)

        # Column 0 must not stretch
        main_grid.setColumnStretch(0, 0)

        # Column 1 must stretch
        main_grid.setColumnStretch(1, 1)

        # Separator line
        line = qt.QFrame()
        line.setFrameShape(qt.QFrame.HLine)
        line.setFrameShadow(qt.QFrame.Sunken)

        # Add scan button
        self.scan_button = qt.QPushButton("Luo laskut")
        self.scan_button.clicked.connect(self.luo_lasku_pressed_handler)

        # Add widgets to container
        left_side_buttons.addWidget(self.scan_button)

        # Add separator line
        line = qt.QFrame()
        line.setFrameShape(qt.QFrame.HLine)
        line.setFrameShadow(qt.QFrame.Sunken)

        left_side_buttons.addWidget(line)

        # Add stretch that will stretch to fill rest of the space
        left_side_buttons.addStretch()

        self.list_of_visits = qt.QTreeWidget()

        self.list_of_visits.setColumnCount(3)
        self.list_of_visits.setHeaderLabels(["Käyntipäivä", "Nimi", "Terapian laji", "Lisätiedot"])
        self.list_of_visits.setSortingEnabled(True)

        # Allow multiselect
        self.list_of_visits.setSelectionMode(qt.QAbstractItemView.ExtendedSelection)

        third_stupid_widget = QWidget()

        right_side_layout = qt.QVBoxLayout(third_stupid_widget)

        main_grid.addWidget(third_stupid_widget, 0, 1)

        new_visit_date = QDateEdit(datetime.datetime.now())
        new_visit_date.setCalendarPopup(True)
        new_visit_date.setDisplayFormat('dd.MM.yyyy')
        self.new_visit_customers_combobox = QComboBox()
        new_visit_type = QLineEdit()
        new_visit_type.setText("Terapia")

        self.update_page()

        self.new_visit_button = qt.QPushButton("Lisää käynti")

        second_stupid_widget = QWidget()
        new_visit_layout = QHBoxLayout(second_stupid_widget)
        right_side_layout.addWidget(second_stupid_widget)
        new_visit_layout.addWidget(new_visit_date)
        new_visit_layout.addWidget(self.new_visit_customers_combobox)
        new_visit_layout.addWidget(new_visit_type)
        new_visit_layout.addWidget(self.new_visit_button)

        right_side_layout.addWidget(self.list_of_visits)
        # Add properties view
        # main_grid.addWidget(qt.QPlainTextEdit(), 0, 2)

        def new_visit_handler():
            for _customer in self.customers:
                if _customer.name == self.new_visit_customers_combobox.currentText():
                    _customer.new_visit(
                        cost=_customer.hour_price,
                        visit_length_min=45,
                        visit_date=new_visit_date.date().toPython(),
                        visit_type=new_visit_type.text(),
                    )
                    self.update_page()
                    db_session.commit()

        self.new_visit_button.clicked.connect(new_visit_handler)
        # create context menu
        self.popMenu = qt.QMenu(self)
        self.popMenu.addAction(
           qt.QAction('Poista käynti', self.list_of_visits, triggered=self._delete_visit)
        )

        # set button context menu policy
        self.list_of_visits.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.list_of_visits.customContextMenuRequested.connect(self.on_context_menu)

    def on_context_menu(self, point):
        # show context menu
        self.popMenu.exec_(QtGui.QCursor.pos())

    def luo_lasku_pressed_handler(self):

        import pdf_writer
        import therapist

        billed_customers = []
        customers = self.db_session.query(customer.Customer).all()
        therapist = self.db_session.query(therapist.Therapist).first()
        for cust in customers:
            if cust.unbilled_visits():
                billed_customers.append(cust)
                pdf_writer.write_invoice(therapist, cust)

        if billed_customers:
            pdf_writer.write_tilitys(therapist, billed_customers)

        for cust in customers:
            for _visit in cust.unbilled_visits():
                _visit.billed = datetime.date.today()

        # Commit billed visits
        self.db_session.commit()
        self.update_page()

    def update_page(self):
        self.list_of_visits.clear()
        self.new_visit_customers_combobox.clear()
        self.customers = self.db_session.query(customer.Customer).group_by(customer.Customer.name)

        for _customer in self.customers:
            self.add_visits_for_customer(_customer)
            self.new_visit_customers_combobox.addItem(_customer.name)

    def add_visits_for_customer(self, _customer):

        for _visit in _customer.unbilled_visits():
            cell_objects = {0: 'visit_date', 1: 'NO_EDIT', 2: 'visit_type', 3: 'notes'}

            MyTreeWidget(
                self.list_of_visits,
                [
                    _visit.visit_date.strftime("%d.%m.%Y"),
                    _customer.name,
                    _visit.visit_type,
                    _visit.notes,
                ],
                cell_objects=cell_objects,
                db_session=self.db_session,
                id=_visit.id,
                class_item=visit.Visit,
                class_instance=_visit
            )


    def _delete_visit(self):
        for _visit in self.list_of_visits.selectedItems():
            _visit.delete()

        self.update_page()