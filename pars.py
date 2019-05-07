import postgresql
import requests
import time
import json

create_new_table = True
m_post = 20
n_minute = 1
url = 'https://api.github.com/gists'
db = postgresql.open('postgres:1@localhost:5434/postgres')

def get_gists():
    response = requests.get(url)
    result = json.loads(response.content)
    return result

if create_new_table:
    try:
        db.execute('CREATE TABLE gists ("id" SERIAL PRIMARY KEY, "gist" TEXT NULL DEFAULT NULL , "datetime" TIMESTAMP DEFAULT NOW())')
    except:
        print('таблмца не создалась')

his_string = ''
total_update = 0  # колличество обновлений
while True:
    result = get_gists()
    for id, post in enumerate(result):
        if his_string == post['git_pull_url']:
            total_update = id
        if id < m_post:
            db.execute("INSERT INTO gists (gist) VALUES('" + str(post['git_pull_url']).replace(' ', '') + "')")
    his_string = result[0]['git_pull_url']  # сохраняем крайний гист
    print(str(total_update))
    time.sleep(60 * n_minute)