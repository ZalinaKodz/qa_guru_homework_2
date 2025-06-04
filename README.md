### 📦 `Qa_homework_1`

Учебный проект для  QA Guru
---

### 🔧 Стек технологий

* Python 3.10+
* [FastAPI](https://fastapi.tiangolo.com/)
* [Pytest](https://docs.pytest.org/)
* [Requests](https://requests.readthedocs.io/)
* Uvicorn
* Pydantic
* Pytest
* Requests

### 🚀 Как запустить

#### 1. Клонировать репозиторий

```bash
git clone https://github.com/ZalinaKodz/qa_guru_homework_2.git
cd qa_guru_homework_2
```

#### 2. Установить зависимости

```bash
pip install -r requirements.txt
```

#### 3. Запустить FastAPI-сервер

```bash
uvicorn main:app --reload
```

Основной URL: [http://127.0.0.1:8002](http://localhost:8000/api)

#### 4. Запустить тесты

В новом терминале (не останавливая сервер):

```bash
pytest test_smoke.py
```

---

### ✅ Что проверяют тесты:

* Доступность и работоспособность сервиса
* Корректность данных конкретного пользователя
* Обработку запроса на несуществующего пользователя
* Совпадение количества пользователей с параметром per_page
* Корректность подсчёта количества страниц для разных размеров страницы
* Уникальность данных на разных страницах
* Создание нового пользователя
* Обновление существующего пользователя
* Удаление пользователя
* Успешную регистрацию пользователя