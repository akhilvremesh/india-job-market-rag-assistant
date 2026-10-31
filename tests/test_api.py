from fastapi.testclient import TestClient

from app import main


client = TestClient(main.app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_salary_prediction_endpoint(monkeypatch):
    # Replace the real model with a small predictable stand-in.
    class FakeModel:
        def predict(self, input_row):
            return [4.5]

    monkeypatch.setattr(main, "salary_model", FakeModel())

    response = client.post(
        "/predict/salary",
        json={
            "job_title": "Python Data Analyst",
            "key_skills": "Python, SQL",
            "functional_area": "Data Analytics",
            "role": "Data Analyst",
            "location": "Bengaluru",
            "role_category": "Programming & Design",
            "industry": "IT-Software",
            "experience_mid_years": 2.5,
        },
    )

    assert response.status_code == 200
    assert response.json()["predicted_salary_lpa"] == 4.5


def test_resume_endpoint_rejects_non_pdf():
    response = client.post(
        "/match/resume",
        files={"file": ("resume.txt", b"not a PDF", "text/plain")},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Please upload a PDF file."