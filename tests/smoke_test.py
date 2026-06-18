import requests


def test_jira_connection(base_url, jira_auth_headers):
    # Эндпоинт возвращает информацию о текущем пользователе (о тебе)
    url = f"{base_url}/rest/api/3/myself"

    response = requests.get(url, headers=jira_auth_headers)

    assert response.status_code == 200, f"Ошибка авторизации: {response.status_code} - {response.text}"

    user_data = response.json()
    print(f"\nУспешное подключение! Привет, {user_data.get('displayName')}")