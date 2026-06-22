import os
import base64
import requests
from dotenv import load_dotenv

load_dotenv()


def bulk_cleanup():
    base_url = os.getenv("JIRA_BASE_URL")
    project_key = os.getenv("JIRA_PROJECT_KEY", "TI")

    email = os.getenv("JIRA_EMAIL")
    api_token = os.getenv("JIRA_API_TOKEN")
    auth_str = f"{email}:{api_token}"
    auth_base64 = base64.b64encode(auth_str.encode("utf-8")).decode("utf-8")

    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    # Используем новый эндпоинт, который требует Atlassian
    search_url = f"{base_url}/rest/api/3/search/jql"
    jql = f"project = {project_key} AND summary ~ 'Load Test*'"

    print("Ищем мусорные задачи в Jira...")
    response = requests.get(search_url, params={"jql": jql, "maxResults": 100}, headers=headers)

    if response.status_code != 200:
        print(f"Ошибка поиска: {response.status_code} - {response.text}")
        return

    response_data = response.json()

    issues = response_data.get("results", [])

    if not issues:
        issues = response_data.get("issues", [])

    print(f"Найдено задач для удаления: {len(issues)}")
    print(f"Найдено задач для удаления: {len(issues)}")

    # ВРЕМЕННЫЙ ПРИНТ ДЛЯ ОТЛАДКИ СТРУКТУРЫ
    if issues:
        print("\n СТРУКТУРА ПЕРВОЙ ЗАДАЧИ ИЗ ОТВЕТА JIRA:")
        import json
        print(json.dumps(issues[0], indent=2, ensure_ascii=False))
        print("-" * 50)

    # Безопасное удаление
        # Безопасное удаление по ID
        deleted_count = 0
        for issue in issues:
            if isinstance(issue, dict):
                # Забираем 'id', так как Atlassian вернул только его
                issue_id = issue.get("id")

                if issue_id:
                    # Отправляем запрос на удаление по ID задачи
                    delete_url = f"{base_url}/rest/api/3/issue/{issue_id}"
                    del_res = requests.delete(delete_url, headers=headers)

                    if del_res.status_code == 204:
                        print(f"[-] Задача с ID {issue_id} успешно удалена.")
                        deleted_count += 1
                    else:
                        print(f"[!] Не удалось удалить ID {issue_id}: {del_res.status_code}")

        print(f"\nОчистка завершена! Всего удалено задач: {deleted_count}")


if __name__ == "__main__":
    bulk_cleanup()