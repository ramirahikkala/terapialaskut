from PySide2.QtWidgets import (
    QWidget,)
import PySide2.QtWidgets as qt
from PySide2 import QtCore, QtGui


class MyTreeWidget(qt.QTreeWidgetItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.setFlags(self.flags() | QtCore.Qt.ItemIsEditable)
        self.cell_objects = kwargs.get('cell_objects')
        self.db_session = kwargs.get('db_session')
        self.id = kwargs.get('id')
        self.class_item = kwargs.get('class_item')
        self.class_instance = kwargs.get('class_instance')

    def setData(self, *args, **kwargs):

        _customer = (
            self.db_session.query(self.class_item)
            .filter(self.class_item.id == self.id)
            .first()
        )
        name = self.cell_objects[args[0]]
        value = args[2]

        # Prevent editing
        if name == 'NO_EDIT':
            return

        if name == 'active':
            if args[2].lower() in ['false', 'ei', 'no']:
                value = False
            else:
                value = True

        if name in ['kelakorvaus', 'hour_price']:
            value = float(value.replace(',', '.'))

        if 'date' in name:
            from dateutil import parser
            value = parser.parse(value)

        setattr(_customer, name, value)

        self.db_session.commit()
        super().setData(*args, **kwargs)

    def delete(self):
        self.db_session.delete(self.class_instance)
        self.db_session.commit()
