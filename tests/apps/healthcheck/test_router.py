def test_healthcheck(client):
    response = client.get('/healthcheck/status/')
    assert response is not None
    assert response.status_code == 200
    assert response.json() == {'status': 'OK'}
