from typing import Callable
from fastapi import FastAPI
from app.core.settings.app import AppSettings


def create_start_app_handler(
        app: FastAPI,
        settings: AppSettings,
) -> Callable:  # type: ignore
    async def start_app() -> None:
        print('inside start app')
        pass

    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable:  # type: ignore
    async def stop_app() -> None:
        print('inside stop app')
        pass

    return stop_app
