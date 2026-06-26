from ai_edge_litert.interpreter import Interpreter

interpreter = Interpreter(model_path="models/plant_disease_model_38.tflite")
interpreter.allocate_tensors()

print("Model loaded successfully!")