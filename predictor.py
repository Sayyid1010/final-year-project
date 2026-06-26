import numpy as np
from ai_edge_litert.interpreter import Interpreter
from PIL import Image

class DiseasePredictor:
    def __init__(self):

        # Load disease model
        self.disease_model = Interpreter(
            model_path="models/plant_disease_model_38.tflite"
        )
        self.disease_model.allocate_tensors()
        self.disease_input = self.disease_model.get_input_details()
        self.disease_output = self.disease_model.get_output_details()

        # Load validator model
        self.validator_model = Interpreter(
            model_path="models/leaf_validator.tflite"
        )
        self.validator_model.allocate_tensors()
        self.val_input = self.validator_model.get_input_details()
        self.val_output = self.validator_model.get_output_details()

        # ⚠️ YOU MUST REPLACE THIS WITH YOUR TRAINING CLASS ORDER
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

    # -------------------------
    # PREPROCESS IMAGE
    # -------------------------
    def preprocess(self, image):
        image = image.resize((224, 224))
        image = np.array(image, dtype=np.float32) / 255.0
        image = np.expand_dims(image, axis=0)
        return image

    # -------------------------
    # VALIDATE LEAF
    # -------------------------
    def validate_leaf(self, image):
        img = self.preprocess(image)

        self.validator_model.set_tensor(
            self.val_input[0]['index'], img
        )
        self.validator_model.invoke()

        output = self.validator_model.get_tensor(
            self.val_output[0]['index']
        )

        output = np.squeeze(output)

        index = int(np.argmax(output))
        confidence = float(np.max(output)) * 100

        classes = ["leaf", "not_leaf"]

        return classes[index], confidence

    # -------------------------
    # PREDICT DISEASE
    # -------------------------
    def predict_disease(self, image):
        img = self.preprocess(image)

        self.disease_model.set_tensor(
            self.disease_input[0]['index'], img
        )
        self.disease_model.invoke()

        output = self.disease_model.get_tensor(
            self.disease_output[0]['index']
        )

        output = np.squeeze(output)

        index = int(np.argmax(output))
        confidence = float(np.max(output)) * 100

        # safety check
        if confidence < 60:
            return "Uncertain prediction", confidence

        if index >= len(self.ai_classes):
            return "Unknown class", confidence

        result = self.ai_classes[index]

        return result, confidence