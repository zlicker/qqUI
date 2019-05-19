import sys
import time
import os

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtChart import *
from customTableModel import CustomTableModel
from itertools import cycle

#COLORS = cycle(["#2196f3", "#f44336", "#4caf50", "#ffeb3b",
COLORS = cycle(["#f44336", "#4caf50", "#ffeb3b",
          "#00bcd4", "#9c27b0", "#795548", "#673ab7"])

class TableWidget(QWidget):
    SERIES = []
    def __init__(self, parent=None):

        super(TableWidget, self).__init__(parent)

        self.resize(960, 480)

        #![1] Create tableView
        self.model = CustomTableModel()
        tableView = QTableView()
        tableView.setModel(self.model)
        tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        #tableView.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        tableView.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        #![2] Creat self.chart & Adding Animations
        self.chart = QChart()
        self.chart.setAnimationOptions(QChart.AllAnimations)

        #![3] Creat Series1
        self.creatSeries("Series 1")
        self.SERIES.append("Series 1")
        #########################################
        #series = QScatterSeries()
        #series.setName("Series 1")
        #mapper = QVXYModelMapper(self)
        #mapper.setXColumn(0)
        #mapper.setYColumn(1)
        #mapper.setSeries(series)
        #mapper.setModel(self.model)
        #self.chart.addSeries(series)

        #seriesColorHex = next(COLORS)
        #series.setColor(QColor(seriesColorHex))

        #seriesColorHex = "#" + str(hex(series.pen().color().rgb()))[-6:]
        #self.model.addMapping(seriesColorHex, QRect(0, 0, 2, self.model.rowCount()))
        #########################################

        #! Adjust axis's range dynamically
        self.model.valueChanged.connect(self.setAxisRange)

        self.chart.createDefaultAxes()
        self.xaxis = self.chart.axisX()
        self.yaxis = self.chart.axisY()
        #self.xaxis = QValueAxis()
        #self.xaxis.setRange(0, 1)
        #self.yaxis = QValueAxis()
        #self.yaxis.setRange(0, 1)
        #self.chart.addAxis(self.xaxis, Qt.AlignBottom)
        #self.chart.addAxis(self.yaxis, Qt.AlignLeft)
        chartView = QChartView(self.chart)
        chartView.setRenderHint(QPainter.Antialiasing)

        #! Create button layout
        addRowsButton = QPushButton('Add Rows')
        addRowsButton.clicked.connect(self.addRow)

        addColumnsButton = QPushButton('Add Series')
        addColumnsButton.clicked.connect(self.addColumn)

        readButton = QPushButton('Read')
        readButton.clicked.connect(self.readData)

        saveButton = QPushButton('Save')
        saveButton.clicked.connect(self.saveData)

        #! Create main layout
        self.mainLayout = QGridLayout()
        self.mainLayout.addWidget(tableView, 0, 1, 1, 2)
        self.mainLayout.addWidget(addRowsButton, 1, 1)
        self.mainLayout.addWidget(addColumnsButton, 1, 2)
        self.mainLayout.addWidget(readButton, 2, 1)
        self.mainLayout.addWidget(saveButton, 2, 2)
        self.mainLayout.addWidget(chartView, 0, 0, 3, 1)

        self.mainLayout.setColumnStretch(0, 6)
        self.mainLayout.setColumnStretch(1, 2)
        self.mainLayout.setColumnStretch(2, 2)


        self.setLayout(self.mainLayout)

    def addRow(self):
        row = self.model.rowCount()
        self.model.insertRows(row)

    def addColumn(self, serieName=None):
        column = self.model.columnCount()
        self.model.insertColumns(column, 2)

        #! Show an input Dialog
        if serieName is None:
            currentSeriesNumber = 'Series ' + str(int(self.model.columnCount()/2))

            serieName, ok = QInputDialog.getText(self, "Please input new series' name",
                "Series Name: ", QLineEdit.Normal, currentSeriesNumber)

        self.creatSeries(serieName)
        self.SERIES.append(serieName)

    def readData(self):
        filePathList, _ = QFileDialog.getOpenFileNames(self, 'Please Choose a File', './')
        for file in filePathList:
            _, fileName = os.path.split(file)
            fileName, _ = os.path.splitext(fileName)
            self.addColumn(fileName)
            curColumn = self.model.columnCount()
            with open(file, 'r') as fh:
                for row, line in enumerate(fh.readlines()):
                    datas = line.split()
                    print(datas)
                    print(row, curColumn)
                    #self.model.m_data[row][curColumn-2]=5
                    if len(datas)>1:
                        self.model.m_data[row][curColumn-2] = float(datas[0])
                        self.model.m_data[row][curColumn-1] = float(datas[1])


    def saveData(self):
        currentTime = time.strftime("%Y-%m-%d %H:%M", time.localtime())
        try:
            os.mkdir(currentTime)
        except FileExistsError:
            pass

        for i, file in enumerate(self.SERIES):
            curAbsPath = os.getcwd()
            filePath = curAbsPath + '/' + currentTime + '/' + file
            #! The file will be created automatically if the file doesn't existed.
            with open(filePath, 'w') as fh:
                for row in range(self.model.rowCount()):
                    for column in range(2*i, 2*i+2):
                        data = self.model.m_data[row][column]
                        if isinstance(data, QVariant):
                            data = ''
                        fh.write(str(data) + '\t')
                    fh.write('\n')


    def setAxisRange(self):
        self.xaxis.setRange(self.model.xMin-.2, self.model.xMax+.2)
        self.yaxis.setRange(self.model.yMin-.2, self.model.yMax+.2)

    def creatSeries(self, serieName):
        x = self.model.columnCount()-2
        y = x+1

        series = QScatterSeries()
        series.setName(serieName)
        mapper = QVXYModelMapper(self)
        mapper.setModel(self.model)
        mapper.setXColumn(x)
        mapper.setYColumn(y)
        mapper.setSeries(series)
        mapper.setModel(self.model)

        color = next(COLORS)
        seriesColorHex = QColor(color)
        seriesColorHex.setAlphaF(0.5)
        series.setColor(seriesColorHex)
        ########################################
        #series.setColor(QColor(seriesColorHex))
        #series.setBrush(QColor(seriesColorHex))
        #series.setPen(QColor(seriesColorHex))
        ########################################

        self.chart.addSeries(series)
        #self.model.addMapping(color, QRect(x, 0, 2, self.model.rowCount()))

        self.chart.createDefaultAxes()
        self.xaxis = self.chart.axisX()
        self.yaxis = self.chart.axisY()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    obj = TableWidget()
    obj.show()
    sys.exit(app.exec_())