# Plant Disease Prediction

This project is a machine learning application designed to predict plant diseases from images. It uses a pre-trained YOLO v11 model to classify images of plant leaves into various disease categories or identify them as healthy. The application is built with Python and utilizes the PyQt5 framework for the graphical user interface (GUI).

## Features

- **Image Classification**: Predicts the disease of a plant based on an input image.
- **Graphical User Interface**: Provides an easy-to-use interface for users to upload images and view predictions.
- **Disease Information**: Allows users to search for more information about the predicted disease.

## Technologies Used

- **Python**: The main programming language used for the application.
- **YOLO**: Used for loading and running the pre-trained machine learning model.
- **PyQt5**: Used for creating the GUI.
- **NumPy**: Used for numerical operations on image data.
- **Webbrowser**: Used to open a web browser for searching more information about the predicted disease.

## How to Run

1. Install the required dependencies using `pip`.
2. Run the application using the command `python src/app.py`.
3. Use the GUI to upload an image and get the disease prediction.
