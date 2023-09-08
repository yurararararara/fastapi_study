from fastapi.testclient import TestClient
from main import app
# 엔드포인트들을 테스트해서 예상한 결과를 반환하는지 확인
client = TestClient(app)

def test_get_all_blogs():
    response = client.get("/blog/all")
    assert response.status_code == 400
# assert는 프로그래밍에서 특정 조건이 참인지 확인하기 위해 사용
def test_auth_error():
    response = client.post("/token",
                           data = {"username" : "", "password": ""})
    access_token = response.json().get("access_token")
    assert access_token == None
    message = response.json().get("detail")[0].get("msg")
    assert message == "Field required"
    
def test_auth_success():
    response = client.post("/token",
                           data = {"username" : "test", "password": "test"})
    access_token = response.json().get("access_token")
    assert access_token

def test_post_article():
    auth = client.post("/token",
                           data = {"username" : "test", "password": "test"})
    access_token = auth.json().get("access_token")

    assert access_token

    response = client.post(
        "/article/",
        json = {
            "title": "Test article",
            "content" : "Test content",
            "published" : True,
            "creator_id": 1
        },
        headers= {
            "Authorization" : "bearer " + access_token
        }
    )
    assert response.status_code == 200
    # 추가된 article title이 Test article과 동일한지 확인
    assert response.json().get("title") == "Test article"