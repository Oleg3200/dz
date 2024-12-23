# 1. Клонирование репозитория

Склонируйте репозиторий с исходным кодом и тестами:

```
git clone <URL репозитория>
cd <директория проекта>
```

# 2. Установка зависимостей при запуске

```
pip install subprocess

```

# Создайте виртуальное окружение

```bash
# Активируйте виртуальное окружение
python -m venv venv
# Для Windows:
venv\Scripts\activate
# Для MacOS/Linux:
source venv/bin/activate
```


# 3. Структура проекта
Проект содержит следующие файлы и директории:
```bash
unittests.py              # файл для тестирования
config.xml             # конфигурационный файл 
hw2.py                  # файл с программой
plantuml.jar           # plantuml
file.puml             # файл с выводом программы 
```

# 4. Запуск проекта
```bash
py hw2.py config.xml     # py название файла <файл с конфигом>
```


# 5. Тестирование с моим репозитеорием 
Вывод программы
```
@startuml
!define RECTANGLE class
package "Commits" {
    RECTANGLE "Initial commit" as 763ab86{
        + 763ab86414f001d11383f969e2ac1622ae630d8a
    }
    RECTANGLE "commit1" as 15bb8d5{
        + 15bb8d5eb138d2a03e08f065da959ea1319de79f
    }
    763ab86 --> 15bb8d5
    RECTANGLE "commit2" as 5324bbd{
        + 5324bbde5207691ca36861ca78a2a206e1ccaab2
    }
    15bb8d5 --> 5324bbd
    RECTANGLE "commit3" as cf9886d{
        + cf9886d615d0801e99f1c27c77e7db0c77c0bb67
    }
    5324bbd --> cf9886d
    RECTANGLE "commit4" as 2299184{
        + 2299184ef2b5c9fdf63c4c14af5c48e8ca083bb4
    }
    cf9886d --> 2299184
}
@enduml
```
Сгенерированный uml
![image](https://github.com/user-attachments/assets/3cbaac73-c29d-42b3-a084-624acbf6a914)

Коммиты на гите
![image](https://github.com/user-attachments/assets/18c2323e-52e9-4641-b9d6-e5b5cb2f86f2)


