from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)
    

def test_base_url():
    # Test root URL
    response = client.get("/")
    assert response.status_code == 404


def test_base_random_str():
    # Test random/misspelled string inputted as endpoint
    response = client.get("/abcdefg")
    assert response.status_code == 404


def test_subapp_random_str():
    # Test random/misspelled string inputted as endpoint
    response = client.get("/lab/abcdefg")
    assert response.status_code == 404     


def test_health():
    # Test health endpoint
    response = client.get("/lab/health")
    assert response.status_code == 200


def test_hello():
    # Test hello endpoint with required parameter
    response = client.get("/lab/hello?name=YourName")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello YourName"}


def test_hello_param():
    # Parameter "name" spelled wrong
    response = client.get("/lab/hello?nam=YourName")
    assert response.status_code == 422


def test_hello_no_name():
    # Test missing parameter entry
    response = client.get("/lab/hello")
    assert response.status_code == 422


# Bulk prediction tests
def test_bulk_predict():
    # Test predict endpoint
    with TestClient(app) as lifespanned_client:
        response = lifespanned_client.post("/lab/bulk-predict/",
            json={"houses": [
                    {"MedInc": 7.3252,
                    "HouseAge": 32.0,
                    "AveRooms": 6.984127,
                    "AveBedrms": 2.023810,
                    "Population": 392.0,
                    "AveOccup": 2.755556,
                    "Latitude": 37.78,
                    "Longitude": -122.23},
                    {"MedInc": 8.3252,
                    "HouseAge": 41.0,
                    "AveRooms": 6.984127,
                    "AveBedrms": 1.023810,
                    "Population": 322.0,
                    "AveOccup": 2.555556,
                    "Latitude": 37.88,
                    "Longitude": -122.23},
                    {"MedInc": 5.3252,
                    "HouseAge": 80.0,
                    "AveRooms": 6.984127,
                    "AveBedrms": 1.023810,
                    "Population": 352.0,
                    "AveOccup": 2.555556,
                    "Latitude": 37.98,
                    "Longitude": -122.23}
                ]})
        assert response.status_code == 200
        assert type(response.json()["predictions"]) is list


def test_bulk_predict_extra_param():
    # Test extra parameter sent to predict endpoint
    with TestClient(app) as lifespanned_client:
        response = lifespanned_client.post("/lab/bulk-predict/",
            json={"houses": [
                    {"MedInc": 7.3252,
                    "HouseAge": 32.0,
                    "AveRooms": 6.984127,
                    "AveBedrms": 2.023810,
                    "Population": 392.0,
                    "AveOccup": 2.755556,
                    "Latitude": 37.78,
                    "Longitude": -122.23,
                    "Should": "Not Be Here"},
                    {"MedInc": 8.3252,
                    "HouseAge": 41.0,
                    "AveRooms": 6.984127,
                    "AveBedrms": 1.023810,
                    "Population": 322.0,
                    "AveOccup": 2.555556,
                    "Latitude": 37.88,
                    "Longitude": -122.23},
                    {"MedInc": 5.3252,
                    "HouseAge": 80.0,
                    "AveRooms": 6.984127,
                    "AveBedrms": 1.023810,
                    "Population": 352.0,
                    "AveOccup": 2.555556,
                    "Latitude": 37.98,
                    "Longitude": -122.23}
                ]})
        assert response.status_code == 422
        assert response.json()["detail"][0]["msg"] == "Extra inputs are not permitted"


def test_bulk_predict_missing_param():
    # Test missing parameter
    with TestClient(app) as lifespanned_client:
        response = lifespanned_client.post("/lab/bulk-predict/",
            json={"houses": [
                    {"MedInc": 7.3252,
                    "HouseAge": 32.0,
                    "AveRooms": 6.984127,
                    "AveBedrms": 2.023810,
                    "Population": 392.0,
                    "Latitude": 37.78,
                    "Longitude": -122.23},
                    {"MedInc": 8.3252,
                    "HouseAge": 41.0,
                    "AveRooms": 6.984127,
                    "AveBedrms": 1.023810,
                    "Population": 322.0,
                    "AveOccup": 2.555556,
                    "Latitude": 37.88,
                    "Longitude": -122.23},
                    {"MedInc": 5.3252,
                    "HouseAge": 80.0,
                    "AveRooms": 6.984127,
                    "AveBedrms": 1.023810,
                    "Population": 352.0,
                    "AveOccup": 2.555556,
                    "Latitude": 37.98,
                    "Longitude": -122.23}
                ]})
        assert response.status_code == 422
        assert response.json()["detail"][0]["msg"] == "Field required"


def test_bulk_predict_bad_type():
    # Test bad input
    with TestClient(app) as lifespanned_client:
        response = lifespanned_client.post("/lab/bulk-predict/",
            json={"houses": [
                    {"MedInc": "This is a string",
                    "HouseAge": 32.0,
                    "AveRooms": 6.984127,
                    "AveBedrms": 2.023810,
                    "Population": 392.0,
                    "AveOccup": 2.755556,
                    "Latitude": 37.78,
                    "Longitude": -122.23},
                    {"MedInc": 8.3252,
                    "HouseAge": 41.0,
                    "AveRooms": 6.984127,
                    "AveBedrms": 1.023810,
                    "Population": 322.0,
                    "AveOccup": 2.555556,
                    "Latitude": 37.88,
                    "Longitude": -122.23},
                    {"MedInc": 5.3252,
                    "HouseAge": 80.0,
                    "AveRooms": 6.984127,
                    "AveBedrms": 1.023810,
                    "Population": 352.0,
                    "AveOccup": 2.555556,
                    "Latitude": 37.98,
                    "Longitude": -122.23}
                ]})
        assert response.status_code == 422
        assert response.json()["detail"][0]["msg"] == "Input should be a valid number, unable to parse string as a number"


def test_bulk_lat_pos():
    # Test out-of-range latitude
    with TestClient(app) as lifespanned_client:
        response = lifespanned_client.post("/lab/bulk-predict/",
            json={"houses": [
                    {"MedInc": 7.3252,
                    "HouseAge": 32.0,
                    "AveRooms": 6.984127,
                    "AveBedrms": 2.023810,
                    "Population": 392.0,
                    "AveOccup": 2.755556,
                    "Latitude": 97,
                    "Longitude": -122.23},
                    {"MedInc": 8.3252,
                    "HouseAge": 41.0,
                    "AveRooms": 6.984127,
                    "AveBedrms": 1.023810,
                    "Population": 322.0,
                    "AveOccup": 2.555556,
                    "Latitude": 37.88,
                    "Longitude": -122.23},
                    {"MedInc": 5.3252,
                    "HouseAge": 80.0,
                    "AveRooms": 6.984127,
                    "AveBedrms": 1.023810,
                    "Population": 352.0,
                    "AveOccup": 2.555556,
                    "Latitude": 37.98,
                    "Longitude": -122.23}
                ]})
        data = response.json()
        assert response.status_code == 422
        assert data["detail"][0]["msg"] == "Value error, Invalid value for Latitude"


def test_bulk_lat_neg():
    # Test out-of-range latitude
    with TestClient(app) as lifespanned_client:
        response = lifespanned_client.post("/lab/bulk-predict/",
            json={"houses": [
                    {"MedInc": 7.3252,
                    "HouseAge": 32.0,
                    "AveRooms": 6.984127,
                    "AveBedrms": 2.023810,
                    "Population": 392.0,
                    "AveOccup": 2.755556,
                    "Latitude": -97,
                    "Longitude": -122.23},
                    {"MedInc": 8.3252,
                    "HouseAge": 41.0,
                    "AveRooms": 6.984127,
                    "AveBedrms": 1.023810,
                    "Population": 322.0,
                    "AveOccup": 2.555556,
                    "Latitude": 37.88,
                    "Longitude": -122.23},
                    {"MedInc": 5.3252,
                    "HouseAge": 80.0,
                    "AveRooms": 6.984127,
                    "AveBedrms": 1.023810,
                    "Population": 352.0,
                    "AveOccup": 2.555556,
                    "Latitude": 37.98,
                    "Longitude": -122.23}
                ]})
        data = response.json()
        assert response.status_code == 422
        assert data["detail"][0]["msg"] == "Value error, Invalid value for Latitude"


def test_bulk_long_pos():
    # Test out-of-range longitude
        with TestClient(app) as lifespanned_client:
            response = lifespanned_client.post("/lab/bulk-predict/",
                json={"houses": [
                        {"MedInc": 7.3252,
                        "HouseAge": 32.0,
                        "AveRooms": 6.984127,
                        "AveBedrms": 2.023810,
                        "Population": 392.0,
                        "AveOccup": 2.755556,
                        "Latitude": 37.78,
                        "Longitude": -122.23},
                        {"MedInc": 8.3252,
                        "HouseAge": 41.0,
                        "AveRooms": 6.984127,
                        "AveBedrms": 1.023810,
                        "Population": 322.0,
                        "AveOccup": 2.555556,
                        "Latitude": 37.88,
                        "Longitude": -122.23},
                        {"MedInc": 5.3252,
                        "HouseAge": 80.0,
                        "AveRooms": 6.984127,
                        "AveBedrms": 1.023810,
                        "Population": 352.0,
                        "AveOccup": 2.555556,
                        "Latitude": 37.98,
                        "Longitude": 190}
                    ]})
            assert response.status_code == 422
            assert response.json()["detail"][0]["msg"] == "Value error, Invalid value for Longitude"


def test_bulk_long_neg():
    # Test out-of-range longitude
        with TestClient(app) as lifespanned_client:
            response = lifespanned_client.post("/lab/bulk-predict/",
                json={"houses": [
                        {"MedInc": 7.3252,
                        "HouseAge": 32.0,
                        "AveRooms": 6.984127,
                        "AveBedrms": 2.023810,
                        "Population": 392.0,
                        "AveOccup": 2.755556,
                        "Latitude": 37.78,
                        "Longitude": -122.23},
                        {"MedInc": 8.3252,
                        "HouseAge": 41.0,
                        "AveRooms": 6.984127,
                        "AveBedrms": 1.023810,
                        "Population": 322.0,
                        "AveOccup": 2.555556,
                        "Latitude": 37.88,
                        "Longitude": -122.23},
                        {"MedInc": 5.3252,
                        "HouseAge": 80.0,
                        "AveRooms": 6.984127,
                        "AveBedrms": 1.023810,
                        "Population": 352.0,
                        "AveOccup": 2.555556,
                        "Latitude": 37.98,
                        "Longitude": -190}
                    ]})
            assert response.status_code == 422
            assert response.json()["detail"][0]["msg"] == "Value error, Invalid value for Longitude"


# Single prediction tests
def test_predict():
    # Test predict endpoint
    with TestClient(app) as lifespanned_client:
        response = lifespanned_client.post("/lab/predict/",
            json={"MedInc": 8.3252,
                "HouseAge": 41.0,
                "AveRooms": 6.984127,
                "AveBedrms": 1.023810,
                "Population": 322.0,
                "AveOccup": 2.555556,
                "Latitude": 37.88,
                "Longitude": -122.23})
        assert response.status_code == 200
        assert type(response.json()["prediction"]) is float


def test_predict_extra_param():
    # Test extra parameter sent to predict endpoint
    with TestClient(app) as lifespanned_client:
        response = lifespanned_client.post("/lab/predict/",
            json={"MedInc": 8.3252,
                "HouseAge": 41.0,
                "AveRooms": 6.984127,
                "AveBedrms": 1.023810,
                "Population": 322.0,
                "AveOccup": 2.555556,
                "Latitude": 37.88,
                "Longitude": -122.23,
                "Should": "not be here"})
        assert response.status_code == 422
        assert response.json()["detail"][0]["msg"] == "Extra inputs are not permitted"


def test_predict_missing_param():
    # Test missing parameter
    with TestClient(app) as lifespanned_client:
        response = lifespanned_client.post("/lab/predict/",
            json={"MedInc": 8.3252,
                "HouseAge": 41.0,
                "AveRooms": 6.984127,
                "AveBedrms": 1.023810,
                "Population": 322.0,
                "Latitude": 37.88,
                "Longitude": -122.23})
        assert response.status_code == 422
        assert response.json()["detail"][0]["msg"] == "Field required"


def test_predict_bad_type():
    # Test bad input
    with TestClient(app) as lifespanned_client:
        response = lifespanned_client.post("/lab/predict/",
            json={"MedInc": "This is a string",
                "HouseAge": 41.0,
                "AveRooms": 6.984127,
                "AveBedrms": 1.023810,
                "Population": 322.0,
                "AveOccup": 2.555556,
                "Latitude": 37.88,
                "Longitude": -122.23})
        assert response.status_code == 422
        assert response.json()["detail"][0]["msg"] == "Input should be a valid number, unable to parse string as a number"


def test_lat_pos():
    # Test out-of-range latitude
    with TestClient(app) as lifespanned_client:
        response = lifespanned_client.post("/lab/predict/",
            json={"MedInc": 8.3252,
                "HouseAge": 41.0,
                "AveRooms": 6.984127,
                "AveBedrms": 1.023810,
                "Population": 322.0,
                "AveOccup": 2.555556,
                "Latitude": 97,
                "Longitude": -122.23})
        data = response.json()
        assert response.status_code == 422
        assert data["detail"][0]["msg"] == "Value error, Invalid value for Latitude"


def test_lat_neg():
    # Test out-of-range latitude
    with TestClient(app) as lifespanned_client:
        response = lifespanned_client.post("/lab/predict/",
            json={"MedInc": 8.3252,
                "HouseAge": 41.0,
                "AveRooms": 6.984127,
                "AveBedrms": 1.023810,
                "Population": 322.0,
                "AveOccup": 2.555556,
                "Latitude": -97,
                "Longitude": -122.23})
        data = response.json()
        assert response.status_code == 422
        assert data["detail"][0]["msg"] == "Value error, Invalid value for Latitude"


def test_long_pos():
    # Test out-of-range longitude
    with TestClient(app) as lifespanned_client:
        response = lifespanned_client.post("/lab/predict/",
            json={"MedInc": 8.3252,
                "HouseAge": 41.0,
                "AveRooms": 6.984127,
                "AveBedrms": 1.023810,
                "Population": 322.0,
                "AveOccup": 2.555556,
                "Latitude": 37.88,
                "Longitude": 190})
        assert response.status_code == 422
        assert response.json()["detail"][0]["msg"] == "Value error, Invalid value for Longitude"


def test_long_neg():
    # Test out-of-range longitude
    with TestClient(app) as lifespanned_client:
        response = lifespanned_client.post("/lab/predict/",
            json={"MedInc": 8.3252,
                "HouseAge": 41.0,
                "AveRooms": 6.984127,
                "AveBedrms": 1.023810,
                "Population": 322.0,
                "AveOccup": 2.555556,
                "Latitude": 37.88,
                "Longitude": -190})
        assert response.status_code == 422
        assert response.json()["detail"][0]["msg"] == "Value error, Invalid value for Longitude"


# Documentation tests
def test_docs():
    # Test docs endpoint
    response = client.get("/docs")
    assert response.status_code == 200


def test_subapp_docs():
    # Test docs endpoint
    response = client.get("/lab/docs")
    assert response.status_code == 200


def test_openapi():
    # Test openapi.json endpoint
    response = client.get("/openapi.json")
    assert response.status_code == 200


def test_subapp_openapi():
    # Test openapi.json endpoint
    response = client.get("/lab/openapi.json")
    assert response.status_code == 200
