from fastapi.testclient import TestClient

from antispoof.api.main import app

client = TestClient(app)


def test_openapi_declares_error_response_schema_for_check():
    response = client.get("/openapi.json")

    assert response.status_code == 200

    payload = response.json()

    check_endpoint = payload["paths"]["/check"]["post"]
    responses = check_endpoint["responses"]

    assert "400" in responses
    assert "500" in responses
    assert responses["400"]["content"]["application/json"]["schema"]["$ref"] == (
        "#/components/schemas/ErrorResponse"
    )
    assert responses["500"]["content"]["application/json"]["schema"]["$ref"] == (
        "#/components/schemas/ErrorResponse"
    )


def test_openapi_declares_error_response_schema_for_benchmark():
    response = client.get("/openapi.json")

    assert response.status_code == 200

    payload = response.json()

    benchmark_endpoint = payload["paths"]["/benchmark"]["get"]
    responses = benchmark_endpoint["responses"]

    assert "404" in responses
    assert "500" in responses
    assert responses["404"]["content"]["application/json"]["schema"]["$ref"] == (
        "#/components/schemas/ErrorResponse"
    )
    assert responses["500"]["content"]["application/json"]["schema"]["$ref"] == (
        "#/components/schemas/ErrorResponse"
    )


def test_openapi_contains_error_response_schema():
    response = client.get("/openapi.json")

    assert response.status_code == 200

    payload = response.json()

    schemas = payload["components"]["schemas"]

    assert "ErrorResponse" in schemas
    assert "ErrorDetail" in schemas


def test_openapi_error_response_schema_exposes_only_standardized_fields():
    response = client.get("/openapi.json")

    assert response.status_code == 200

    payload = response.json()

    schema = payload["components"]["schemas"]["ErrorResponse"]
    properties = schema["properties"]

    assert set(properties.keys()) == {"request_id", "correlation_id", "error"}


def test_openapi_error_detail_schema_exposes_only_standardized_fields():
    response = client.get("/openapi.json")

    assert response.status_code == 200

    payload = response.json()

    schema = payload["components"]["schemas"]["ErrorDetail"]
    properties = schema["properties"]

    assert set(properties.keys()) == {"code", "message"}
