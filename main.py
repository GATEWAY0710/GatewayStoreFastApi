from typing import Union
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from api.controller.user_controller import router as user_router
from api.controller.auth_controller import router as auth_router
from api.controller.profile_controller import router as profile_router
from api.controller.product_controller import router as product_router
from api.controller.stock_entry_controller import router as stock_entry_router
from api.controller.sales_controller import router as sales_router
from api.controller.report_controller import router as report_router
import jwt
from fastapi.staticfiles import StaticFiles
import os

from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"Request: {request.method} {request.url} {await request.body()}")
    response = await call_next(request)
    print(f"Response status: {response.status_code}")
    return response

@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"Request: {request.method} {request.url} {await request.body()}")
    response = await call_next(request)
    print(f"Response status: {response.status_code}")
    return response

@app.exception_handler(HTTPException)
def exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail, "status": False},
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(profile_router, prefix="/profile", tags=["Profile"])
app.include_router(product_router, prefix="/product", tags=["Product"])
app.include_router(stock_entry_router, prefix="/stock_entry", tags=["Stock Entry"])
app.include_router(sales_router, prefix="/sales", tags=["Sales"])
app.include_router(report_router, prefix="/report", tags=["Report"])
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")