import os
import shutil
import uuid
from fastapi import APIRouter, HTTPException, Form, UploadFile
from application.use_case.models.base_response import BaseResponse
from application.use_case.models.product import CreateProductResponse, CreateProduct, UpdateProduct, GetResponse, List
from infrastructure.dependency import Container

UPLOAD_DIR = "uploads"

router = APIRouter()

@router.post("", response_model=CreateProductResponse)
def create(name: str = Form(), description: str = Form(), image: UploadFile = None) -> BaseResponse:
    product_service = Container.product_service()

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    image_path = None
    if image:
        file_ext = os.path.splitext(image.filename)[1]
        filename = f"{uuid.uuid4()}{file_ext}"
        image_path = os.path.join(UPLOAD_DIR, filename)

        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        request = CreateProduct(
            name=name,
            description=description,
            image=image_path
        )

    response = product_service.create(product=request)
    if not response.status:
        raise HTTPException(status_code=response._status_code, detail=response.message)
    return response

@router.put("", response_model=CreateProductResponse)
def update(name: str = Form(), description: str = Form(), image: UploadFile = None) -> BaseResponse:
    product_service = Container.product_service()

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    image_path = None
    if image:
        file_ext = os.path.splitext(image.filename)[1]
        filename = f"{uuid.uuid4()}{file_ext}"
        image_path = os.path.join(UPLOAD_DIR, filename)

        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        request = UpdateProduct(
            description=description
        )
        if image_path:
            request.image = image_path

    response = product_service.update( name= name, product=request)
    if not response.status:
        raise HTTPException(status_code=response._status_code, detail=response.message)
    return response

@router.get("/product", response_model=GetResponse)
def get(name: str) -> BaseResponse:
    product_service = Container.product_service()
    response = product_service.get_by_name(name=name)
    if not response.status:
        raise HTTPException(status_code=response._status_code, detail=response.message)
    return response

@router.get("", response_model=List)
def list() -> BaseResponse:
    product_service = Container.product_service()
    response = product_service.list()
    if not response.status:
        raise HTTPException(status_code=response._status_code, detail=response.message)
    return response