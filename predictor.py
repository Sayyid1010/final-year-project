import numpy as np
from PIL import Image

try:
    from tflite_runtime.interpreter import Interpreter
except ImportError:
    try:
        from ai_edge_litert.interpreter import Interpreter
    except ImportError:
        import tensorflow as tf
        Interpreter = tf.lite.Interpreter

class DiseasePredictor:
    def __init__(self):
        self.disease_model = Interpreter(
            model_path="models/plant_disease_model_38.tflite"
        )
        self.disease_model.allocate_tensors()
        self.disease_input = self.disease_model.get_input_details()
        self.disease_output = self.disease_model.get_output_details()

        self.validator_model = Interpreter(
            model_path="models/leaf_validator.tflite"
        )
        self.validator_model.allocate_tensors()
        self.val_input = self.validator_model.get_input_details()
        self.val_output = self.validator_model.get_output_details()

        self.ai_classes = [
            "Apple Black Rot", "Apple Cedar Rust", "Apple Healthy", "Apple Scab",
            "Blueberry Healthy", "Cherry Healthy", "Cherry Powdery Mildew",
            "Corn Cercospora Leaf Spot", "Corn Common Rust", "Corn Healthy",
            "Corn Northern Leaf Blight", "Grape Black Measles", "Grape Black Rot",
            "Grape Healthy", "Grape Leaf Blight", "Orange Citrus Greening",
            "Peach Bacterial Spot", "Peach Healthy", "Pepper Bacterial Spot",
            "Pepper Healthy", "Potato Early Blight", "Potato Healthy",
            "Potato Late Blight", "Raspberry Healthy", "Soybean Healthy",
            "Squash Powdery Mildew", "Strawberry Healthy", "Strawberry Leaf Scorch",
            "Tomato Bacterial Spot", "Tomato Early Blight", "Tomato Healthy",
            "Tomato Late Blight", "Tomato Leaf Mold", "Tomato Mosaic Virus",
            "Tomato Septoria Leaf Spot", "Tomato Spider Mites",
            "Tomato Target Spot", "Tomato Yellow Leaf Curl Virus"
        ]

    def preprocess(self, image):
        img = image.resize((224, 224))
        img_array = np.array(img, dtype=np.float32) / 255.0
        return np.expand_dims(img_array, axis=0)

    def validate_leaf(self, image):
        img_input = self.preprocess(image)
        self.validator_model.set_tensor(
            self.val_input[0]['index'], img_input)
        self.validator_model.invoke()
        prediction = self.validator_model.get_tensor(
            self.val_output[0]['index'])
        classes = ['leaf', 'not_leaf']
        result = classes[np.argmax(prediction)]
        confidence = np.max(prediction) * 100
        return result, confidence

    def predict_disease(self, image):
        img_input = self.preprocess(image)
        self.disease_model.set_tensor(
            self.disease_input[0]['index'], img_input)
        self.disease_model.invoke()
        prediction = self.disease_model.get_tensor(
            self.disease_output[0]['index'])
        result = self.ai_classes[np.argmax(prediction)]
        confidence = np.max(prediction) * 100
        return result, confidence
