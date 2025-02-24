from keras.api.models import load_model

model_path="/home/bagus/Documents/Coding-TA/model-api-skripsi/models/potato_model.h5"
model = load_model(model_path)

model.summary()
print(f"Output layer shape: {model.output_shape}")

