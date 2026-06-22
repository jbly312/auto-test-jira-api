import json,os,requests, allure

def test_delete_issue(base_url, jira_auth_headers):
    project_key = os.environ.get("JIRA_PROJECT_KEY","TI")
    create_url = f"{base_url}/rest/api/3/issue"


    payload_create = {
        "fields": {
            "project":{"key": project_key},
            "summary":"Task for deletion",
            "issuetype":{"name":"Task"},
        }
    }

    response_create = requests.post(create_url, headers=jira_auth_headers, json=payload_create)

    assert response_create.status_code == 201

    issue_id = response_create.json()["id"]
    issues_key = response_create.json()["key"]
    issues_url = f"{create_url}/{issue_id}"

    try:

        new_summary = f"Task for deletion"

        payload_update = {"fields":{"summary":new_summary}}
        with allure.step(f"Отправка DELETE запроса"):
            allure.attach(
                json.dumps(payload_update, indent=4, ensure_ascii=False),
                name = "Request Body(DELETE)",
                attachment_type=allure.attachment_type.JSON
            )
            response = requests.delete(issues_url, headers=jira_auth_headers)
            assert response.status_code == 204

        with allure.step(f"Отправка get запроса для проверки"):
            response_get = requests.get(issues_url, headers=jira_auth_headers)

            allure.attach(
                json.dumps(payload_create, indent=4, ensure_ascii=False),
                name = "Request Body(GET)",
                attachment_type=allure.attachment_type.JSON
            )
            assert response_get.status_code == 404


    finally:
        with allure.step(f"Очистка данных"):
            requests.delete(issues_url, headers=jira_auth_headers)
