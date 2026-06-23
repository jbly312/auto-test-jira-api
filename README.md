# auto-test-jira-api

Фреймворк автоматизированного тестирования API Jira (Atlassian Cloud) на Python с использованием pytest, Allure и Locust.

---

## Стек технологий

| Инструмент | Назначение |
|---|---|
| Python 3.x | Основной язык |
| pytest | Тест-раннер |
| requests | HTTP-клиент для Jira REST API |
| pydantic | Модели данных запросов/ответов и валидация |
| python-dotenv | Управление переменными окружения |
| allure-pytest | Формирование тест-репортов |
| locust | Нагрузочное тестирование |
| GitHub Actions | CI/CD пайплайн |

---

## Структура проекта

```
auto-test-jira-api/
├── .github/
│   └── workflows/          # CI/CD пайплайны (GitHub Actions)
├── data/                   # Тестовые данные (JSON-пейлоады, фикстуры)
├── models/                 # Pydantic-модели сущностей Jira
├── performance/            # Сценарии нагрузочного тестирования (Locust)
├── tests/                  # Функциональные API-тесты (pytest)
├── allure-results/         # Сырой вывод Allure (генерируется автоматически)
├── cleanup_jira.py         # Утилита: массовое удаление задач из нагрузочных тестов
├── pytest.ini              # Конфиг pytest (pythonpath = .)
├── requirements.txt        # Зависимости Python
└── .gitignore
```

---

## Предварительные требования

- Python 3.10+
- Экземпляр Jira Cloud с доступом к API
- API-токен Jira — сгенерировать можно по адресу: https://id.atlassian.com/manage-profile/security/api-tokens

---

## Установка

**1. Клонировать репозиторий**

```bash
git clone https://github.com/jbly312/auto-test-jira-api.git
cd auto-test-jira-api
```

**2. Создать и активировать виртуальное окружение**

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

**3. Установить зависимости**

```bash
pip install -r requirements.txt
```

**4. Настроить переменные окружения**

Создать файл `.env` в корне проекта:

```env
JIRA_BASE_URL=https://your-domain.atlassian.net
JIRA_EMAIL=your-email@example.com
JIRA_API_TOKEN=your_api_token_here
JIRA_PROJECT_KEY=TI
```


---

## Запуск тестов

**Запустить все функциональные тесты**

```bash
pytest tests/
```

**Запустить с генерацией Allure-репорта**

```bash
pytest tests/ --alluredir=allure-results
allure serve allure-results
```

**Запустить конкретный тест-файл**

```bash
pytest tests/test_issues.py -v
```

---

## Нагрузочное тестирование

Нагрузочные тесты реализованы с помощью Locust и находятся в директории `performance/`.

```bash
locust -f performance/locustfile.py --host=https://your-domain.atlassian.net
```

После запуска открыть http://localhost:8089 для настройки и старта нагрузочного теста.

---

## Утилита очистки

Нагрузочные тесты создают задачи в Jira с префиксом `Load Test`. После прогона используй `cleanup_jira.py` для их удаления:

```bash
python cleanup_jira.py
```

Скрипт ищет задачи по условию `summary ~ "Load Test*"` в указанном проекте и удаляет их через Jira REST API v3.

---

## CI/CD

Проект включает GitHub Actions workflow в директории `.github/workflows/`. Тесты запускаются автоматически при push и pull request. Allure-репорты можно настроить для публикации как артефакт воркфлоу.

Необходимые секреты для настройки в настройках репозитория GitHub:

```
JIRA_BASE_URL
JIRA_EMAIL
JIRA_API_TOKEN
JIRA_PROJECT_KEY
```

---

## Справочник переменных окружения

| Переменная | Описание | Пример |
|---|---|---|
| `JIRA_BASE_URL` | Базовый URL экземпляра Jira Cloud | `https://myteam.atlassian.net` |
| `JIRA_EMAIL` | Email для аутентификации в Jira | `user@example.com` |
| `JIRA_API_TOKEN` | API-токен Jira  | `ATATxxxxxxxx` |
| `JIRA_PROJECT_KEY` | Ключ проекта Jira для тестовых данных | `TI` |

---

## Примечания

- Аутентификация использует HTTP Basic Auth с Base64-кодированием пары `email:api_token`.
- Все обращения к API направляются на Jira REST API v3 (`/rest/api/3/`).
- В `pytest.ini` прописан `pythonpath = .` — это позволяет корректно импортировать локальные модули без их установки через pip.
