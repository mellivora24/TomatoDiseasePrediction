import numpy as np
import tensorflow as tf
import src.ultis.path as path

class_name = ['Bệnh ghẻ táo',
              'Bệnh thối đen',
              'Bệnh gỉ sắt tuyết tùng',
              'Cây khỏe mạnh',
              'Cây khỏe mạnh',
              'Bệnh phấn trắng',
              'Cây khỏe mạnh',
              'Bệnh đốm lá Cercospora / Đốm lá xám',
              'Bệnh gỉ sắt thông thường',
              'Bệnh cháy lá phương Bắc',
              'Cây khỏe mạnh',
              'Bệnh thối đen',
              'Bệnh Esca (Thối đen)',
              'Bệnh cháy lá (Isariopsis Leaf Spot)',
              'Cây khỏe mạnh',
              'Bệnh vàng lá gân xanh (Greening)',
              'Bệnh đốm vi khuẩn',
              'Cây khỏe mạnh',
              'Bệnh đốm vi khuẩn',
              'Cây khỏe mạnh',
              'Bệnh mốc sương sớm',
              'Bệnh mốc sương muộn',
              'Cây khỏe mạnh',
              'Cây khỏe mạnh',
              'Cây khỏe mạnh',
              'Bệnh phấn trắng',
              'Bệnh cháy lá',
              'Cây khỏe mạnh',
              'Bệnh đốm vi khuẩn',
              'Bệnh mốc sương sớm',
              'Bệnh mốc sương muộn',
              'Bệnh mốc lá',
              'Bệnh đốm lá Septoria',
              'Nhện đỏ hai chấm',
              'Bệnh đốm mục tiêu',
              'Virus xoăn vàng lá cà chua',
              'Virus khảm cà chua',
              'Cây khỏe mạnh']

model = tf.keras.models.load_model(path.resource_path('models/trained_files/model.h5'))

def model_prediction(test_image):
    image = tf.keras.preprocessing.image.load_img(test_image, target_size=(128, 128))
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = np.array([input_arr])

    prediction = model.predict(input_arr)
    result_index = np.argmax(prediction)

    return class_name[result_index]

if __name__ == "__main__":
    img_path = "../../test/test.jpg"
    print(model_prediction(img_path))