import argparse
import uvicorn
import os
from fastapi import FastAPI
from pymongo import MongoClient
from starlette.middleware.cors import CORSMiddleware
from app.core.config import get_app_settings
from app.routes.api_routes import router


def get_application() -> FastAPI:
    settings = get_app_settings()
    # create app
    application = FastAPI(**settings.fastapi_kwargs)
    # middleware
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # error handlers

    # api routes
    application.include_router(
        router=router,
        tags=["api"],
        prefix="/api"
    )

    return application


# app instance
app = get_application()


@app.on_event("startup")
async def startup_event():
    # create mongodb connection
    # read from env variables
    mongo_host=os.getenv('MONGO_HOST')
    mongo_port=os.getenv('MONGO_PORT')
    print(f'mongo_host: {mongo_host}, mongo_port: {mongo_port}')
    client = MongoClient(
        f'mongodb://{mongo_host}:{mongo_port}/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.2.6')
    db = client['carpooldb']
    app.state.db = db


@app.on_event("shutdown")
async def shutdown_event():
    # close mongodb connection
    app.state.db.client.close()


"""
usage:
uvicorn main:app
"""
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", help="application host", required=True, type=str)
    parser.add_argument("--port", help="application port", required=True, type=int)
    args = vars(parser.parse_args())
    uvicorn.run(app, host=args['host'], port=args['port'])
