from fastapi import FastAPI, HTTPException, UploadFile
from model.carbon_emission import (getCarbonEmission,
                                   getCarbonEmissionSegmentation)
from model.model_classification import predict_image_clf
from model.model_segmentation import predict_image_sgmnt
from PIL import Image

THRESHOLD = 0.85

app = FastAPI()

model_name = "BREEZE Food Recognition"
model_version = "v1.0.1"

@app.get("/")
async def index():
    """Landing Page"""
    return "Welcome to BREEZE Food Recognition"

@app.post("/predict")
async def predict(image: UploadFile):
    """Predicting Image"""
    # check form data
    if not image:
        raise HTTPException(status_code=422, detail="Image field cannot be blank.")

    # check image type
    if "image" not in image.content_type:
        raise HTTPException(status_code=400, detail="File must be an image")

    # opening image
    img = Image.open(image.file)

    # predict using classification model
    predicted_class_clf, confidence_clf = predict_image_clf(img)

    ingredients = []
    total_emission = 0

    # check threshold
    if confidence_clf < THRESHOLD:
        predicted_class_clf = None
        confidence_clf = 0
        classes_segmentation = predict_image_sgmnt(img)
        ingredients, total_emission = getCarbonEmissionSegmentation(classes_segmentation)
    else:
        ingredients, total_emission = getCarbonEmission(predicted_class_clf)

    return {
        "name": model_name,
        "version": model_version,
        "filename": image.filename,
        "food_name": predicted_class_clf,
        "confidence": str(round(confidence_clf, 3)),
        "ingredients": ingredients,
        "total_emissions": round(total_emission, 3),
    }