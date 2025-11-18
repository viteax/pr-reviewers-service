# Сервис назначения ревьюеров для Pull Request'ов "Puller"

Puller - сервис, автоматически назначающий ревьюеров на Pull Request'ы (PR),
а также позволяющий осуществлять управление командами и участниками.

## Стек технологий

- ⚡ [**FastAPI**](https://fastapi.tiangolo.com) для Python бэкенда.
    - 🔍 [Pydantic](https://docs.pydantic.dev), используется FastAPI, для валидации данных.
- ✅ Тесты с помощью [Pytest](https://pytest.org).

## Как поднять?

- С помощью docker-compose up

```bash
git clone https://github.com/viteax/pr-reviewers-service.git
cd pr-reviewers-service
docker-compose up

```

- Linux, скрипт одной копипастой (нужна утилита make) 

```bash
git clone https://github.com/viteax/pr-reviewers-service.git
cd pr-reviewers-service
make

```

- Linux, без make

```bash
git clone https://github.com/viteax/pr-reviewers-service.git
cd pr-reviewers-service
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
fastapi dev app/main.py --port 8080

```

- Windows

```powershell
git clone https://github.com/viteax/pr-reviewers-service.git
cd pr-reviewers-service
py -m venv .venv
.\.venv\Scripts\activate
python.exe -m pip install --upgrade pip
pip install -r .\requirements.txt
fastapi dev .\app\main.py --port 8080

```

Объяснение команд:

- Клонировать репозиторий

```bash
git clone https://github.com/viteax/pr-reviewers-service.git
```

- Зайти в новоиспеченную папку

```bash
cd pr-reviewers-service
```

- Запустить утилиту make, исполняющую скрипт Makefile, в котором
прописано создание виртуального окружения, подтяжка зависимостей
и поднятие сервиса

```bash
make
```

После этого виртуальное окружение будет создано, зависимости подтянуты,
а сервис будет висеть на `localhost:8080`

Также стоит упомянуть, что на ручке `/docs` можно будет увидеть автоматически
сгенерированную документацию Swagger UI

## Запуск тестов

Запуск тестов осуществляется с помощью python модуля pytest,
но перед этим надо активировать виртуальное окружение

- Windows

```powershell
.\venv\Scripts\activate
```

- Linux

```bash
source .venv/bin/activate
```

- Запуск тестов

```bash
pytest
```
