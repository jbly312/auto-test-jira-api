import os
import json
import pytest
import requests
from models.issue import IssueCreateResponse, IssueGetResponse
import allure


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

    created_issue_id = None

    try:

        with allure.step("Отправка POST запроса на создание задачи"):
            allure.attach(
                json.dumps(payload, indent=4, ensure_ascii=False),
                name="Request Body (POST)",
                attachment_type=allure.attachment_type.JSON
            )

            response = requests.post(url, json=payload, headers=jira_auth_headers)

            allure.attach(
                json.dumps(response.json() if response.text else {}, indent=4, ensure_ascii=False),
                name=f"Response Body (POST) - Status {response.status_code}",
                attachment_type=allure.attachment_type.JSON
            )

        # Проверяем ожидаемый статус из тест-данных
        assert response.status_code == case["expected_status"], f"Ошибка: {response.text}"

        if response.status_code == 201:
            response_data = response.json()
            created_issue_id = response_data["id"]

            with allure.step("Валидация контракта ответа (POST)"):
                created_issue = IssueCreateResponse(**response_data)

            with allure.step("Отправка GET запроса для проверки созданной задачи"):
                get_response = requests.get(f"{url}/{created_issue.id}", headers=jira_auth_headers)

                allure.attach(
                    json.dumps(get_response.json() if get_response.text else {}, indent=4, ensure_ascii=False),
                    name=f"Response Body (GET) - Status {get_response.status_code}",
                    attachment_type=allure.attachment_type.JSON
                )

                issue_details = IssueGetResponse(**get_response.json())
                assert issue_details.fields.summary == case["summary"]

    except Exception as e:
        allure.attach(str(e), name="Exception Info", attachment_type=allure.attachment_type.TEXT)
        raise e

    finally:
        if created_issue_id:
            with allure.step(f"Очистка данных: Удаление задачи {created_issue_id}"):
                delete_response = requests.delete(f"{url}/{created_issue_id}", headers=jira_auth_headers)
                allure.attach(
                    f"Status Code: {delete_response.status_code}",
                    name="Delete Response Status",
                    attachment_type=allure.attachment_type.TEXT
                )