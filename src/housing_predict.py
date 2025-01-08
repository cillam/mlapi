import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from joblib import load
from redis import asyncio
from datetime import datetime
from pydantic import BaseModel, ConfigDict, ValidationInfo, field_validator
from numpy import array
import os 


logger = logging.getLogger(__name__)
model = None

# Select redis URL based on environment
REDIS_URL = os.getenv("REDIS_URL")
if REDIS_URL is not None:
    LOCAL_REDIS_URL = REDIS_URL
else:
    LOCAL_REDIS_URL = "redis://localhost:6379/0" 


@asynccontextmanager
async def lifespan_mechanism(app: FastAPI):
    logging.info("Starting up  API")

    # Load the Model on Startup
    global model
    model = load("model_pipeline.pkl")

    # Load the Redis Cache
    HOST_URL = LOCAL_REDIS_URL  
    redis = asyncio.from_url(HOST_URL, encoding="utf8", decode_responses=True)

    FastAPICache.init(RedisBackend(redis), prefix=<PREFIX>)

    yield

    logging.info("Shutting down API")


# Create instance of subapplication
sub_application_housing_predict = FastAPI(lifespan=lifespan_mechanism)


# Define input model for single prediction
class HousingPrediction(BaseModel):
    MedInc: float
    HouseAge: float
    AveRooms: float
    AveBedrms: float
    Population: float
    AveOccup: float
    Latitude: float
    Longitude: float

    # Forbid extra inputs
    model_config = ConfigDict(extra='forbid')

    # Validate lat/long fields
    @field_validator('Latitude', 'Longitude')
    @classmethod
    def check_latlong(cls, v: float, info: ValidationInfo) -> float:
        if info.field_name == 'Latitude':
            if not -90 <= v <= 90:
                raise ValueError(f'Invalid value for {info.field_name}') 
        if info.field_name == 'Longitude':
            if not -180 <= v <= 180:
                raise ValueError(f'Invalid value for {info.field_name}')
        return v


# Define output model for single prediction
class Output(BaseModel):
    prediction: float


# Define input model for multiple predictions
class MultiplePredictions(BaseModel):
    houses: list[HousingPrediction]

    # Format data as matrix
    def feature_array(self):
        feature_vals = []
        for house in self.houses:
            house_features = house.model_dump()
            feature_values = array([x for x in house_features.values()])
            feature_vals.append(feature_values)
        feature_vals = array(feature_vals)
        return feature_vals

# Define output model for multiple predictions
class ListOutput(BaseModel):
    predictions: list[float]


@sub_application_housing_predict.get("/health")
async def health():
    """
    Check health status.
    Args:
        None
    Returns:
       Dynamic structure of
       {
            "time": <CURRENT DATE/TIME>
        }
    """
    return {"time": datetime.now().isoformat()}


@sub_application_housing_predict.get("/hello")
async def hello(name: str):
    """
    Say hello to user by name.
    Args:
        name (str, required)
    Returns:
        Properly formatted JSON string = 
        {
            "message": "Hello <VALUE>"
        }
    """
    greeting = f"Hello {name}"
    return {"message": greeting}


@sub_application_housing_predict.post("/predict", response_model=Output)
@cache()
async def predict(data: HousingPrediction):
    """
    Obtain prediction for house value.
    Args:
        MedInc (float, required)
        HouseAge (float, required)
        AveRooms (float, required)
        AveBedrms (float, required)
        Population (float, required)
        AveOccup (float, required)
        Latitude (float, required): Must be in the range of -90 to 90.
        Longitude (float, required): Must be in the range of -180 to 180.
    Returns:
        Properly formatted JSON string = 
        {
            "prediction": <AVG HOUSE VALUE>
        }
    """
    features = data.model_dump()
    feature_values = array([x for x in features.values()]).reshape(-1, 8)
    prediction = model.predict(feature_values)[0]
    return {"prediction": prediction}


@sub_application_housing_predict.post("/bulk-predict", response_model=ListOutput)
@cache()
async def multi_predict(data: MultiplePredictions):
    """
    Obtain list of predictions for house values.
    Args:
        houses: 
            {MedInc (float, required)
            HouseAge (float, required)
            AveRooms (float, required)
            AveBedrms (float, required)
            Population (float, required)
            AveOccup (float, required)
            Latitude (float, required): Must be in the range of -90 to 90.
            Longitude (float, required): Must be in the range of -180 to 180.}
    Returns:
        Properly formatted JSON string = 
        {
            "predictions": <List of AVG HOUSE VALUES>
        }
    """
    features = data.feature_array()
    predictions = model.predict(features)
    return {"predictions": predictions.tolist()}
