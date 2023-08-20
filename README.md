# fapi
## Проект для обучения FastAPI (Python)

### Разработка учебного проекта

## Использованные технологии:
- Python 3.11
- FastAPI 0.100.1

## Инструменты:
- pip 23.2
- PyCharm 2022.1 (Community Edition)

## venv (pip list)  
- annotated-types      0.5.0      
- anyio                3.7.1      
- certifi              2023.7.22  
- click                8.1.7      
- colorama             0.4.6      
- dnspython            2.4.2      
- email-validator      2.0.0.post2
- fastapi              0.101.1
- h11                  0.14.0
- httpcore             0.17.3
- httptools            0.6.0
- httpx                0.24.1
- idna                 3.4
- itsdangerous         2.1.2
- Jinja2               3.1.2
- MarkupSafe           2.1.3
- orjson               3.9.5
- pip                  23.2.1
- pydantic             2.2.1
- pydantic_core        2.6.1
- pydantic-extra-types 2.0.0
- pydantic-settings    2.0.3
- python-dotenv        1.0.0
- python-multipart     0.0.6
- PyYAML               6.0.1
- setuptools           65.5.0
- sniffio              1.3.0
- starlette            0.27.0
- typing_extensions    4.7.1
- ujson                5.8.0
- uvicorn              0.23.2
- watchfiles           0.19.0
- websockets           11.0.3


## Использованный материал
- [Документация (Официальный сайт FastAPI)]([https://www.djangoproject.com/](https://fastapi.tiangolo.com/ru/tutorial/first-steps/))
- [YouTube](https://www.youtube.com/watch?v=7IdfnjXsdN4&list=PLeLN0qH0-mCVQKZ8-W1LhxDcVlWtTALCS&index=1)

### Helper (Набор команд и настроек для разработки проекта)

#### Установка виртуальной среды
python -m venv venv

#### Активация виртуальной среды
venv\Scripts\activate.bat

#### Установка FastAPI 
##### ключ [all] - все необходимые модули
pip install fastapi[all]

#### Создание проекта
Создаем файл main.py

#### Запуск сервера разработки
uvicorn main:app --reload
