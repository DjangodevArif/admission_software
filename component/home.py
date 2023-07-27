from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QGridLayout, QMainWindow, QWidget, QFileDialog
from qfluentwidgets import BodyLabel, CaptionLabel, LineEdit, PixmapLabel, PrimaryPushButton, PushButton, TextEdit
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPainter, QPixmap

from PIL import Image

from database.models import Students

from .style_sheet import StyleSheet
from component import resource
from .ui.admission_ui import Ui_MainWindow
from database.db import get_db
from sqlalchemy.orm.session import Session


class HomeWidget(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.setObjectName(text.replace(' ', '-'))
        self.db = get_db()
        self.access: Session = next(self.db)

        # Subclass of frame
        self.gBoxLayout = QGridLayout(self)
        self.ui = Ui_MainWindow()
        w = QMainWindow()
        self.ui.setupUi(w)
        self.gBoxLayout.addWidget(w, 1, Qt.AlignCenter)
        self.gBoxLayout.setContentsMargins(0, 35, 0, 0)

        # Set student_image variable
        self.fname: tuple = None

        # Configure submit button
        self.ui.submit_btn.clicked.connect(self.submit_student_info)
        self.ui.insert_image.clicked.connect(self.preview_image)
        self.list_of_element = [
            self.ui.name_input,
            self.ui.father_name_input,
            self.ui.mother_name_input,
            self.ui.present_address_input,
            self.ui.permanent_address_input,
            self.ui.description_input
        ]

    # get values from ui
    def submit_student_info(self):
        student_name = self.ui.name_input.text()
        student_father = self.ui.father_name_input.text()
        student_mother = self.ui.mother_name_input.text()
        student_present_add = self.ui.present_address_input.text()
        student_permanent_add = self.ui.permanent_address_input.text()
        student_description = self.ui.description_input.toPlainText()
        student_image = self.fname if self.fname != None else None
        new_student = Students(
            name=student_name,
            father_name=student_father,
            mother_name=student_mother,
            present_address=student_present_add,
            permanent_address=student_permanent_add,
            description=student_description,

        )
        if student_image:
            new_student.image = open(student_image[0], 'rb')
        self.access.add(new_student)
        self.access.commit()
        self.access.refresh(new_student)
        self.clean_text()
        # cleaning image
        self.fname = None
        self.ui.image_preview.clear()

    def clean_text(self):
        for item in self.list_of_element:
            item.clear()

    def preview_image(self):
        self.fname = QFileDialog.getOpenFileName(self, 'Open file',
                                                 None, "Image files (*.jpg *.gif)")

        preview_width, preview_height = self.ui.image_preview.size(
        ).width(), self.ui.image_preview.size().height()

        #  KeepAspectRatioByExpanding issue > keep growing by changing photos

        qimage = QPixmap(self.fname[0]).scaled(
            preview_width, preview_height, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)

        self.ui.image_preview.setPixmap(qimage)
