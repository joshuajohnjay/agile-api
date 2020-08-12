from fastapi.testclient import TestClient
import pytest
from agile_api.main import app

client = TestClient(app)

pytest.value_id = 0
pytest.principle_id = 0

### Value API Tests
def test_get_value_id_1():
    response = client.get("/values/1")
    assert response.status_code == 200
    assert response.json() == {'title': 'Individuals and Interactions Over Processes and Tools', 'description': 'Valuing people more highly than processes or tools is easy to understand because it is the people who respond to business needs and drive the development process.', 'id': 1}

def test_post_value():
    obj = {'title': 'testing title', 'description': 'testing description'}
    response = client.post("/values/", json = obj)
    assert response.status_code == 200
    json_response = response.json()
    pytest.value_id = json_response['id']
    assert json_response['title'] == 'testing title'
    assert json_response['description'] == 'testing description'

def test_put_value():
    obj = {'title': 'testing title update', 'description': 'testing description update'}
    response = client.put("/values/"+str(pytest.value_id), json = obj)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response['title'] == 'testing title update' 
    assert json_response['description'] == 'testing description update'

def test_delete_value():
    response = client.delete("/values/"+str(pytest.value_id))
    assert response.status_code == 200
    json_response = response.json()
    assert json_response['id'] == pytest.value_id

### Principle API Tests
def test_get_principle_id_1():
    response = client.get("/principles/1")
    assert response.status_code == 200
    assert response.json() == {"title":"Customer satisfaction through early and continuous software delivery","description":"Customers are happier when they receive working software at regular intervals, rather than waiting extended periods of time between releases.","id":1}

def test_post_principle():
    obj = {'title': 'testing title', 'description': 'testing description'}
    response = client.post("/principles/", json = obj)
    assert response.status_code == 200
    json_response = response.json()
    pytest.principle_id = json_response['id']
    assert json_response['title'] == 'testing title'
    assert json_response['description'] == 'testing description'

def test_put_principle():
    obj = {'title': 'testing title update', 'description': 'testing description update'}
    response = client.put("/principles/"+str(pytest.principle_id), json = obj)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response['title'] == 'testing title update' 
    assert json_response['description'] == 'testing description update'

def test_delete_principle():
    response = client.delete("/principles/"+str(pytest.principle_id))
    assert response.status_code == 200
    json_response = response.json()
    assert json_response['id'] == pytest.principle_id