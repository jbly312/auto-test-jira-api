import os
import base64
from locust import HttpUser, task, between
from dotenv import load_dotenv
import random
# Загружаем доступы из нашего .env
load_dotenv()

class JiraAmbitiousUser(HttpUser):
    # Время ожидания между действиями виртуального пользователя (от 1 до 3 секунд)
    wait_time = between(1, 3)

    def on_start(self):
        email = os.getenv("JIRA_EMAIL")
        api_token = os.getenv("JIRA_API_TOKEN")
        self.project_key = os.getenv("JIRA_PROJECT_KEY", "TI")

        # Кодируем доступы в Base64
        auth_str = f"{email}:{api_token}"
        auth_base64 = base64.b64encode(auth_str.encode("utf-8")).decode("utf-8")

        # Прописываем заголовки для этой сессии пользователя
        self.client.headers.update({
            "Authorization": f"Basic {auth_base64}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    @task(7)  # Вес 7 (70% всех запросов)
    def view_myself_profile(self):
        """Имитируем просмотр профиля / доски"""
        with self.client.get("/rest/api/3/myself", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Jira тормозит или упала: {response.status_code}")

    @task(3)  # Вес 3 (30% всех запросов)
    def create_scrum_issue(self):
        """Имитируем создание задачи со случайным ID для реалистичности"""
        random_id = random.randint(1000, 9999)
        payload = {
            "fields": {
                "project": {"key": self.project_key},
                "summary": f"Load Test: Нагрузочный тикет #{random_id}",
                "issuetype": {"name": "Task"}
            }
        }
        with self.client.post("/rest/api/3/issue", json=payload, name="/rest/api/3/issue [POST]",
                              catch_response=True) as response:
            if response.status_code == 201:
                response.success()
            else:
                response.failure(f"Ошибка: {response.status_code}")