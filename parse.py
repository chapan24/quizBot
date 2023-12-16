import requests
from bs4 import BeautifulSoup as BS
import sqlite3
from random import randint

answers_mass = []
ans = 0


def get_connection():
    conn = sqlite3.connect('db.db')
    return conn


def start_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS text(
          quest text,
          ans text
        )""")

        conn.commit()


def parse_site(url):
    response = requests.get(url)
    soup = BS(response.text, 'html.parser')
    start_db()
    block_quiz = (soup.find('div', 'entry-content cf')
                  .find_all('p'))

    for task in block_quiz:
        task = task.text.strip()
        if 'Пушкин велик' in task:
            continue
        if 'Составитель' in task:
            continue
        task = task.replace('Ответ: ', '')[3:]
        n_ind = task.index('\n')
        question = task[:n_ind].strip()
        answer = task[n_ind:].strip()
        add_quiz(question, answer)


def add_quiz(question, answer):
    with get_connection() as conn:
        cursor = conn.cursor()
        values = cursor.execute('''SELECT quest, ans FROM text''').fetchall()
        for value in values:
            if value[0] == question and value[1] == answer:
                return False
        cursor.execute('''INSERT INTO text (quest, ans) VALUES(?, ?)''', (question, answer))

        conn.commit()


def get_question():
    with get_connection() as conn:
        cursor = conn.cursor()
        global answers_mass, ans
        cnt = 0

        while cnt != 1:
            ans = randint(0, 39)
            if ans in answers_mass:
                continue
            else:
                cnt = 1
                answers_mass.append(ans)
                question = cursor.execute('''SELECT quest FROM text''').fetchall()[ans][0]
        return question


def get_answer():
    with get_connection() as conn:
        cursor = conn.cursor()
        answer = cursor.execute('''SELECT ans FROM text''').fetchall()[ans][0].lower()

        return answer


def reset():
    global answers_mass
    answers_mass = []

    return answers_mass


parse_site('https://detskiychas.ru/school/pushkin/victorina_biografiya_pushkina/?ysclid=loswj6m18g215772164')
