import cv2
import requests
import webbrowser
import numpy as np
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QTimer  # Thêm QTimer để tạo lịch tự động
from src.ultis.camera import CameraThread
import src.models.prediction as prediction

disease_info = {
    "Bệnh ghẻ táo": "Triệu chứng: Xuất hiện đốm màu nâu, sần sùi trên lá và quả.\nBiện pháp: Cắt tỉa cành nhiễm bệnh, sử dụng thuốc gốc đồng.",
    "Bệnh thối đen": "Triệu chứng: Quả và lá bị thâm đen, có mùi hôi.\nBiện pháp: Loại bỏ phần bị bệnh, cải thiện thoát nước.",
    "Bệnh gỉ sắt tuyết tùng": "Triệu chứng: Xuất hiện đốm vàng cam trên lá.\nBiện pháp: Sử dụng thuốc diệt nấm phù hợp.",
    "Bệnh phấn trắng": "Triệu chứng: Xuất hiện lớp bột trắng trên lá.\nBiện pháp: Dùng thuốc trừ nấm hoặc dung dịch baking soda pha loãng.",
    "Bệnh đốm lá Cercospora / Đốm lá xám": "Triệu chứng: Lá có đốm tròn, viền nâu.\nBiện pháp: Cắt tỉa lá bệnh, phun thuốc sinh học.",
    "Bệnh gỉ sắt thông thường": "Triệu chứng: Xuất hiện các đốm vàng nâu trên lá.\nBiện pháp: Sử dụng thuốc trừ nấm, giữ khoảng cách giữa cây trồng.",
    "Bệnh cháy lá phương Bắc": "Triệu chứng: Lá có đốm nhỏ màu nâu hoặc đen, lan rộng nhanh.\nBiện pháp: Giữ cây khô ráo, cắt bỏ lá bị bệnh.",
    "Bệnh Esca (Thối đen)": "Triệu chứng: Thân và lá cây bị thối đen, làm cây suy yếu.\nBiện pháp: Kiểm soát độ ẩm và loại bỏ cây nhiễm bệnh.",
    "Bệnh cháy lá (Isariopsis Leaf Spot)": "Triệu chứng: Lá xuất hiện các đốm tròn màu nâu, viền sẫm.\nBiện pháp: Giữ khoảng cách trồng, dùng thuốc trừ nấm.",
    "Bệnh vàng lá gân xanh (Greening)": "Triệu chứng: Lá bị vàng, méo mó, cây còi cọc.\nBiện pháp: Phòng trừ rầy chổng cánh, sử dụng giống kháng bệnh.",
    "Bệnh đốm vi khuẩn": "Triệu chứng: Xuất hiện các đốm nước, lá dễ rụng.\nBiện pháp: Tăng cường thông gió, tránh tưới quá nhiều nước.",
    "Bệnh mốc sương sớm": "Triệu chứng: Xuất hiện vết nâu, viền vàng trên lá.\nBiện pháp: Xử lý bằng thuốc trừ nấm Mancozeb.",
    "Bệnh mốc sương muộn": "Triệu chứng: Lá bị úng nước, chuyển màu nâu sẫm.\nBiện pháp: Hạn chế độ ẩm, sử dụng thuốc phòng trừ.",
    "Bệnh mốc lá": "Triệu chứng: Lá có lớp mốc trắng, cây yếu dần.\nBiện pháp: Cắt bỏ lá bệnh, giữ độ ẩm thấp.",
    "Bệnh đốm lá Septoria": "Triệu chứng: Xuất hiện đốm tròn, viền nâu trên lá.\nBiện pháp: Loại bỏ lá bệnh, sử dụng thuốc gốc đồng.",
    "Nhện đỏ hai chấm": "Triệu chứng: Lá chuyển vàng, có mạng nhện nhỏ.\nBiện pháp: Dùng dầu neem hoặc thuốc trừ sâu sinh học.",
    "Bệnh đốm mục tiêu": "Triệu chứng: Xuất hiện đốm tròn tối màu trên lá.\nBiện pháp: Kiểm soát độ ẩm, sử dụng thuốc bảo vệ thực vật.",
    "Virus xoăn vàng lá cà chua": "Triệu chứng: Lá xoăn, vàng, cây kém phát triển.\nBiện pháp: Tiêu diệt bọ phấn, trồng giống kháng bệnh.",
    "Virus khảm cà chua": "Triệu chứng: Xuất hiện vệt khảm trên lá.\nBiện pháp: Nhổ bỏ cây nhiễm bệnh, kiểm soát côn trùng.",
    "Cây khỏe mạnh": "Cây của bạn không có dấu hiệu bệnh!"
}

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(964, 582)
        self.ui = loadUi('../design/PlantDiseasePrediction.ui', self)

        self.ui.result_infor.setText("")
        self.ui.predicted_res.setText("")
        self.ui.predicting_btn.clicked.connect(self.predict)
        self.ui.moreInfor_btn.clicked.connect(self.more_info)

        self.camera_thread = CameraThread()
        self.camera_thread.frame_signal.connect(self.update_frame)
        self.camera_thread.start()

        self.auto_predict_timer = QTimer(self)
        self.auto_predict_timer.timeout.connect(self.predict)
        self.auto_predict_timer.start(15000)

    def update_frame(self, frame):
        """ Cập nhật ảnh từ camera lên giao diện """
        self.ui.realtime_img.setPixmap(QPixmap.fromImage(frame))

    def predict(self):
        """ Dự đoán bệnh cây từ ảnh camera """
        pixmap = self.ui.realtime_img.pixmap()
        if pixmap is None:
            return

        qimg = pixmap.toImage()
        buffer = qimg.bits()
        buffer.setsize(qimg.byteCount())

        img_array = np.array(buffer).reshape(qimg.height(), qimg.width(), 4)
        img_array = cv2.cvtColor(img_array, cv2.COLOR_BGRA2RGB)
        img_resized = cv2.resize(img_array, (224, 224))

        result = prediction.model_prediction(img_resized)
        scaled_pixmap = pixmap.scaled(300, 250)

        self.ui.predicted_img.setPixmap(scaled_pixmap)
        self.ui.predicted_res.setText(result)

        requests.get(f"https://sgp1.blynk.cloud/external/api/update?token=ATIa0ZEmi0ouwZwlDqBKWwPI858HoEcv&V8={result}")

        if result == "Cây khỏe mạnh":
            self.ui.result_infor.setText("Bạn không cần phải lo lắng, cây của bạn đang khỏe mạnh!")
        else:
            self.ui.result_infor.setText(disease_info[result])

    def more_info(self):
        """ Mở Google tìm kiếm thông tin về bệnh cây đã dự đoán """
        if self.ui.predicted_res.text() != "":
            webbrowser.open("https://www.google.com/search?q=" + self.ui.predicted_res.text())