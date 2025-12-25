from fastapi import FastAPI
from api.routers.routers import api_router

def create_api():

    app = FastAPI(title='Ecommerce API')

    app.include_router(api_router)

    return app

app = create_api()

