from qfluentwidgets.components.widgets.button import ToolButton
from component import resource
from component.ui.table_bottom_ui import Ui_TableBottom
from database.db import get_db
from database.models import Students
from PyQt5.QtCore import QSize, QModelIndex, Qt
from PyQt5.QtGui import QPixmap, QIcon, QColor, QPainter, QPalette
from PyQt5.QtWidgets import (
    QLabel,
    QHeaderView,
    QAbstractScrollArea,
    QSizePolicy,
    QGridLayout,
    QAction,
    QPushButton, QFrame, QHBoxLayout, QStyleOptionViewItem,
    QTableWidgetItem, QWidget, QVBoxLayout)
from qfluentwidgets.components.widgets.table_view import (TableItemDelegate,
                                                          TableWidget,
                                                          isDarkTheme)
from qfluentwidgets import FluentIcon as FIF
from sqlalchemy_file.storage import StorageManager


class PrintWidget(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.setObjectName(text.replace(' ', '-'))
        self.db = get_db()
        self.access = next(self.db)
        # self.label = QLabel(text, self)
        # self.label.setAlignment(Qt.AlignCenter)

        # Subclass of object
        # self.gBoxLayout = QGridLayout(self)
        # self.ui = Ui_MainWindow()
        # w = QMainWindow()
        # self.ui.setupUi(w)
        # self.gBoxLayout.addWidget(w, 1, Qt.AlignCenter)
        # self.gBoxLayout.setContentsMargins(0, 35, 0, 0)

        # Subclass of frame
        # self.ui = Ui_main_widget()
        # self.gBoxLayout = QGridLayout(self)
        # self.main = QWidget()
        # self.ui.setupUi(self.main)
        # self.gBoxLayout.addWidget(self.main, 1, Qt.AlignCenter)
        # self.gBoxLayout.setContentsMargins(0, 35, 0, 0)

        # fetch data
        students = self.access.query(Students).all()

        # Set up the model
        self.tableView = TableWidget(self)
        self.tableView.setWordWrap(False)
        self.tableView.setRowCount(len(students))
        self.tableView.setColumnCount(7)

        # add action button in colum
        # self.tembtn = QPushButton(self)
        # self.tableView.setCellWidget(0, 1, self.tembtn)

        header = self.tableView.horizontalHeader()
        # header.setSectionResizeMode(5, QHeaderView.Stretch)

        for i, student_info in enumerate(students):
            for j, data in enumerate([
                student_info.image,
                str(student_info.id),
                student_info.name,
                student_info.father_name,
                student_info.mother_name,
                student_info.present_address,
                student_info
            ]):
                if j == 0:
                    if data:
                        # self.tableItem = QTableWidgetItem(
                        #     data.filename, 5)
                        # self.tableView.setItem(i, j, self.tableItem)
                        self.tempLabel = QLabel(self)

                        file = StorageManager.get_file(
                            "default/"+data.file_id)
                        qimage = QPixmap(file.get_cdn_url()).scaled(
                            80, 80, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)

                        self.tempLabel.setPixmap(qimage)
                        self.tableView.setCellWidget(i, j, self.tempLabel)
                        self.tableView.setColumnWidth(j, 80)
                    else:
                        self.tempLabel = QLabel(self)
                        qimage = QPixmap("resource/No-image-found.jpg").scaled(
                            80, 80, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)

                        self.tempLabel.setPixmap(qimage)
                        self.tableView.setCellWidget(i, j, self.tempLabel)
                        self.tableView.setColumnWidth(j, 80)
                elif j == 6:
                    self.tembtn = ToolButton(self)
                    # self.tembtn.setObjectName(u"Edit")
                    self.tembtn.setIcon(FIF.EDIT)

                    self.tembtn.resize(10, 10)
                    self.tableView.setCellWidget(0, j, self.tembtn)
                else:
                    self.tableItem = QTableWidgetItem(
                        data)
                    self.tableView.setItem(i, j, self.tableItem)

        self.tableView.verticalHeader().hide()
        self.tableView.setHorizontalHeaderLabels(
            ["Photo", 'Id', 'Name', 'Father name', 'Mother name', 'Present address', "Action"])
        self.tableView.resizeColumnsToContents()

        # self.setStyleSheet("background-color: rgb(32, 32, 32)")
        self.tableView.setItemDelegate(CustomTableItemDelegate(self.tableView))
        # self.tableView.initStyleOption(3)

        # Table bottom action
        self.tableActionWidget = QWidget()
        self.tableAction = Ui_TableBottom()
        self.tableAction.setupUi(self.tableActionWidget)

        self.hBoxLayout = QGridLayout(self)
        self.hBoxLayout.addWidget(self.tableView)
        self.hBoxLayout.addWidget(self.tableActionWidget)
        self.hBoxLayout.setContentsMargins(0, 33, 0, 0)


class CustomTableItemDelegate(TableItemDelegate):
    """ Custom table item delegate """

    def initStyleOption(self, option: QStyleOptionViewItem, index: QModelIndex):
        super().initStyleOption(option, index)

        # if index.column() != 3:
        #     return

        if isDarkTheme():
            option.palette.setColor(QPalette.Text, Qt.white)
            option.palette.setColor(
                QPalette.HighlightedText, QColor("#7a4fbf"))
        else:
            option.palette.setColor(QPalette.Text, Qt.black)
            option.palette.setColor(
                QPalette.HighlightedText, QColor("#7a4fbf"))

    def paint(self, painter, option, index):
        super().paint(painter, option, index)
        painter.save()
        painter.setPen(Qt.NoPen)
        painter.setRenderHint(QPainter.Antialiasing)

        # set clipping rect of painter to avoid painting outside the borders
        painter.setClipping(True)
        painter.setClipRect(option.rect)

        # call original paint method where option.rect is adjusted to account for border
        option.rect.adjust(0, self.margin, 0, -self.margin)

        # draw highlight background
        isHover = self.hoverRow == index.row()
        isPressed = self.pressedRow == index.row()
        isAlternate = index.row() % 2 == 0 and self.parent().alternatingRowColors()
        isDark = isDarkTheme()

        c = 255 if isDark else 0
        alpha = 0

        if index.row() not in self.selectedRows:
            if isPressed:
                alpha = 9 if isDark else 6
            elif isHover:
                alpha = 10
            elif isAlternate:
                # customized
                alpha = 17
        else:
            if isPressed:
                alpha = 15 if isDark else 9
            elif isHover:
                alpha = 10
            else:
                alpha = 17

            # draw indicator
            if index.column() == 0 and self.parent().horizontalScrollBar().value() == 0:
                self._drawIndicator(painter, option, index)

        painter.setBrush(QColor(c, c, c, alpha))
        self._drawBackground(painter, option, index)

        painter.restore()
        super().paint(painter, option, index)
