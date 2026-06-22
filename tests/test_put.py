import json,os,requests, allure



def test_update_issue(base_url, jira_auth_headers):
    project_key = os.getenv("JIRA_PROJECT_KEY", "TI")
    create_url = f"{base_url}/rest/api/3/issue"

    payload_create = {
        "fields": {
            "project": {"key": project_key},
            "summary": "Task for Updation Test",
            "issuetype": {"name": "Task"}
        }
    }

    response_create = requests.post(create_url, headers=jira_auth_headers, json=payload_create)
    assert response_create.status_code == 201

    issue_id = response_create.json()["id"]
    issues_key = response_create.json()["key"]
    issues_url = f"{create_url}/{issue_id}"

    try:

        new_summary = f"Task for Updation Test"
        payload_update = {"fields": {"summary": new_summary}}

        with allure.step(f"Отправка PUT запроса"):
            allure.attach(
                json.dumps(payload_update, indent=4, ensure_ascii=False),
                name="Request Body(PUT)",
                attachment_type=allure.attachment_type.JSON
            )
            response = requests.put(issues_url, headers=jira_auth_headers, json=payload_update)
            assert response.status_code == 204

        with allure.step(f"Отправка GET запроса для проверки"):
            response_get = requests.get(issues_url, headers=jira_auth_headers)
            assert response_get.status_code == 200

            allure.attach(
                json.dumps(response_get.json(), indent=4, ensure_ascii=False),
                name="Request Body(GET)",
                attachment_type=allure.attachment_type.JSON
            )
            assert response_get.json()["fields"]["summary"] == new_summary

    finally:
        with allure.step(f"Очистка данных"):
            requests.delete(issues_url, headers=jira_auth_headers)

