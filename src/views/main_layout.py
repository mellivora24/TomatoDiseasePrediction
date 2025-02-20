import webbrowser
from PyQt5.uic import loadUi
import src.ultis.path as path
from PyQt5.QtWidgets import QMainWindow
import src.models.prediction as prediction

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(964, 582)
        self.ui = loadUi('../design/PlantDiseasePrediction.ui', self)

        self.ui.predicted_res.setText("")
        self.ui.predicting_btn.clicked.connect(self.predict)
        self.ui.moreInfor_btn.clicked.connect(self.more_info)

    def predict(self):
        result = prediction.model_prediction(path.resource_path("../test/test.jpg"))
        self.ui.predicted_res.setText(result)

    def more_info(self):
        if self.ui.predicted_res.text() != "":
            webbrowser.open("https://www.google.com/search?q=" + self.ui.predicted_res.text())
