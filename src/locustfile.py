from locust import HttpUser, task, between
import os

class ModelPredictUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def send_prediction_request(self):
        with open("gold.jpeg", "rb") as img_file:
            files = {"file": ("gold.jpeg", img_file, "image/jpeg")}

            with self.client.post("/predict", files=files, catch_response=True) as response:
                if response.status_code == 200:
                    response.success()
                else:
                    response.failure(f"Status Code: {response.status_code}")
