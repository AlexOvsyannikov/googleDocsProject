**Начало работы**

Пример формы для парсинга:
https://docs.google.com/forms/d/1SHrWtckuShjPA8npdVEBFGzF4FTJbUsgagrxr92sD7g/

1. Инициализируем класс для получения данных, url - ссылка на нужную Google форму. 
`data_getter = RequestSender(url)`
2. Инициализируем класс Parser для обработки данных. \
`parser = Parser(data_getter)`
3. Запускаем стандартные методы парсера для инициализации.  
`parser.parse_title()`  
`parser.parse_description()`  
`parser.parse_script()`  
`parser.parse_questions()`  
`parser.parse_options()`
4. Инициализируем класс DataSender для предоставления ответов.  
`sender = DataSender(parser=parser, max_time_to_sleep=1, num_of_votes=100, list_of_answers=[
        [
            {
                "name": "Вариант 1",
                "amount": 3,
                "text": None
            },
            {
                "name": "Вариант 2",
                "amount": 10,
                "text": None
            },
            {
                "name": "Вариант 3",
                "amount": 17,
                "text": None
            },
            {
                "name": "",
                "amount": 70,
                "text": "text.provided_data:1;2;3;4;"
            }
        ],
        [
            {
                "name": "Вариант 1",
                "amount": 70,
                "text": None
            },
            {
                "name": "Вариант 2",
                "amount": 10,
                "text": None
            },
            {
                "name": "Вариант 3",
                "amount": 17,
                "text": None
            },
            {
                "name": "Вариант 4",
                "amount": 3,
                "text": None
            }
        ],
        [
            {
                "name": "Вариант 1",
                "amount": 70,
                "text": None
            },
            {
                "name": "Вариант 2",
                "amount": 10,
                "text": None
            },
            {
                "name": "Вариант 3",
                "amount": 17,
                "text": None
            }
        ]
    ])`  
*Важно: указываем в ответы в формате [[Вопрос1], [Вопрос2], ..., [ВопросN]]*  
*Для каждого вопроса нужно предоставить словарь {name: вариант_Ответа,
 amount: количество_голосов_за_этот_вариант, text: развернутый_ответ}*  
 
 5. Запускаем стандартные методы sender-a.  
`sender.get_probs_of_answers()`  
`sender.get_naked_options()`  
6. Запускаем скрипт. 
`sender.send_data()`