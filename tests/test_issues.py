import os
import json
import pytest
import requests
from models.issue import IssueCreateResponse, IssueGetResponse


def load_test_data():
    with open("data/issues_data.json", "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.mark.parametrize("case", load_test_data(), ids=lambda c: c["scenario_name"])
def test_create_issue_ddt(case, base_url, jira_auth_headers):
    project_key = os.getenv("JIRA_PROJECT_KEY", "TI")
    url = f"{base_url}/rest/api/3/issue"

    payload = {
        "fields": {
            "project": {"key": project_key},
            "summary": case["summary"],
            "issuetype": {"name": "type" in case and case["type"] or "Task"}
        }
    }
    if "type" in case:
        payload["fields"]["issuetype"]["name"] = case["type"]

    # Переменная для хранения ID созданной задачи (чтобы удалить её потом)
    created_issue_id = None

    try:
        response = requests.post(url, json=payload, headers=jira_auth_headers)
        assert response.status_code == case["expected_status"], f"Ошибка: {response.text}"

        if response.status_code == 201:
            response_data = response.json()
            created_issue_id = response_data["id"]  # Запоминаем ID

            # Валидация контракта (POST)
            created_issue = IssueCreateResponse(**response_data)

            # Проверка через GET
            get_response = requests.get(f"{url}/{created_issue.id}", headers=jira_auth_headers)
            issue_details = IssueGetResponse(**get_response.json())
            assert issue_details.fields.summary == case["summary"]

    finally:
        if created_issue_id:
            delete_url = f"{url}/{created_issue_id}"
            delete_response = requests.delete(delete_url, headers=jira_auth_headers)
            assert delete_response.status_code == 204, f"Не удалось удалить задачу после теста: {delete_response.text}"