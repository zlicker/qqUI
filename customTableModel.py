import sys
import random

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class CustomTableModel(QAbstractTableModel):
    dataChanged = pyqtSignal(QModelIndex, QModelIndex)
    valueChanged = pyqtSignal()
    m_mapping = {}
    m_columnCount = 2
    m_rowCount = 15

    m_data = []

    inf = float('inf')
    xMin, xMax, yMin, yMax = inf, -inf, inf, -inf

    def __init__(self, parent=None):

        super(CustomTableModel, self).__init__(parent)

        for i in range(self.m_rowCount):
            datas = []
            for k in range(self.m_columnCount):
                datas.append(QVariant())
                #if(k%2==0):
                #    datas.append(50*i + random.randint(0, 20))
                #else:
                #    datas.append(random.randint(0, 100))
            self.m_data.append(datas)
        
    #! Three method must be reimplemented when subclass QAbstractTableModel
    def rowCount(self, index=QModelIndex()):
        return len(self.m_data)

    def columnCount(self, index=QModelIndex()):
        return len(self.m_data[0])

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role!= Qt.DisplayRole:
            return QVariant()

        if orientation==Qt.Horizontal:
            if section%2 == 0:
                return "P / (Pa)"
            else:
                return "V / (m/s)"
        else:
            return int(section+1)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return self.m_data[index.row()][index.column()]
        elif role == Qt.EditRole:
            return self.m_data[index.row()][index.column()]
        elif role == Qt.BackgroundColorRole:
            for color, rect in self.m_mapping.items():
                if rect.contains(index.column(), index.row()):
                    return QColor(color)
        return QVariant()

    #! Reimplement 'setData()' to make cell editable and 'flags()' to return a value
    #! containing 'Qt.ItemIsEditable'
    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and role == Qt.EditRole:
            if self.is_digit(value):
                value = float(value)
                self.m_data[index.row()][index.column()] = value
                self.dataChanged[QModelIndex, QModelIndex].emit(index, index)

                if index.column() % 2 == 0:
                    if value < self.xMin and value != 0:
                        self.xMin = value
                    if value > self.xMax:
                        self.xMax = value
                else:
                    if value < self.yMin and value != 0:
                        self.yMin = value
                    if value > self.yMax:
                        self.yMax = value
                self.valueChanged.emit()

                return True
            else:
                return False
        else:
            return False

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        return QAbstractTableModel.flags(self, index) | Qt.ItemIsEditable
        #return Qt.ItemFlags(QAbstractTableModel.flags(self, index) | Qt.ItemIsEditable)

    #! Reimplement the function of Inserting and Removing row to insert and remove rows
    def insertRows(self, position, rows=1, index=QModelIndex()):
        self.beginInsertRows(QModelIndex(), position, position+rows-1)
        for row in range(rows):
            self.m_data.append([])
            for column in range(self.columnCount()):
                self.m_data[position+row].append(QVariant())

        self.endInsertRows()

    def insertColumns(self, position, columns=1, index=QModelIndex()):
        self.beginInsertColumns(QModelIndex(), position, position+columns-1)
        for column in range(columns):
            for row in self.m_data:
                row.append(QVariant())
        self.endInsertColumns()

    def addMapping(self, color, area):
        self.m_mapping[color] = QRect(area)

    def is_digit(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def showModel(self):
        for row in self.m_data:
            print(row)


if __name__ == '__main__':
    obj = CustomTableModel()