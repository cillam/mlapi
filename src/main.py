from contextlib import AsyncExitStack

from fastapi import FastAPI

from src.housing_predict import lifespan_mechanism, sub_application_housing_predict

description = """
Lab 3 app is a FastAPI application that supports the following endpoints:
* lab/health
* lab/hello
* lab/predict
* /docs
* /openapi.json
* lab/docs
* lab/openapi.json
"""

async def main_lifespan(app: FastAPI):
    async with AsyncExitStack() as stack:
        # Manage the lifecycle of sub_app
        await stack.enter_async_context(
            lifespan_mechanism(sub_application_housing_predict)
        )
        yield


app = FastAPI(lifespan=main_lifespan, description=description)


app.mount("/lab", sub_application_housing_predict)


# /docs endpoint is defined by FastAPI automatically
# /openapi.json returns a json object automatically by FastAPI
