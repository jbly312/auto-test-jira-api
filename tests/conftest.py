import os
import base64
import pytest
from dotenv import load_dotenv

# Загружаем переменные из файла .env при старте тестов
load_dotenv()


@pytest.fixture(scope="session")
def base_url():
    url = os.getenv("JIRA_BASE_URL")
    if not url:
        raise ValueError("JIRA_BASE_URL не задан в .env файле")
    return url


@pytest.fixture(scope="session")
def jira_auth_headers():
    email = os.getenv("JIRA_EMAIL")
    api_token = os.getenv("JIRA_API_TOKEN")

    if not email or not api_token:
        raise ValueError("JIRA_EMAIL или JIRA_API_TOKEN не заданы в .env файле")

    # Кодируем "email:token" в Base64, как требует Jira Cloud
    auth_str = f"{email}:{api_token}"
    auth_bytes = auth_str.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

    return {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }