# tests/test_main.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_generate_content_no_files():
    response = client.post("/generate", data={"text_prompt": "Create a song for PacMan background music"})
    assert response.status_code == 200
    data = response.json()
    assert "description" in data
    assert "audio_url" in data
    # assert "album_image_url" in data


def test_generate_content_with_files():
    audio_file = ("audio", ("RoadLessTraveled.mp3", open("tests/RoadLessTraveled.mp3", "rb"), "audio/mpeg"))
    image_file = ("image", ("sample_image.png", open("tests/sample_image.png", "rb"), "image/png"))

    response = client.post("/generate", data={"text_prompt": "Create a happy song"}, files=[audio_file, image_file])
    assert response.status_code == 200
    data = response.json()
    assert "description" in data
    assert "audio_url" in data
    assert "album_image_url" in data


def test_list_user_requests():
    # Simulate a request to list files for a user (requires a previous interaction)
    response = client.get("/requests")
    assert response.status_code == 200
    data = response.json()
    assert "requests" in data
