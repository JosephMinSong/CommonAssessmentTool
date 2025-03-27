import os
from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.clients.service.logic import interpret_and_calculate
from app.clients.schema import PredictionInput

from app.clients.service.logic import get_current_model, list_all_models, load_model

router = APIRouter(prefix="/model", tags=["model logic"])

@router.get("/get_current_model")
async def current_model():
    return {"name" : get_current_model()}

@router.get("/list_all_models")
async def all_models():
    return list_all_models()

@router.post("/change_model")
async def change_model(model):
    return load_model(model)

@router.post("/predictions")
async def predict(data: PredictionInput):
    return interpret_and_calculate(data.model_dump())