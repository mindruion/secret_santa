import datetime
import time

import requests
import schedule
from sqlmodel import select, Session

from main import updater, User, engine

session = Session(engine)


def quotes():
    results = session.query(User).count()
    res = requests.get(f'https://goquotes-api.herokuapp.com/api/v1/random/{results}?type=tag&val=motivational')
    if res.status_code == 200:
        statement = select(User)
        users = session.exec(statement)
        for i, u in enumerate(users):
            updater.bot.send_message(u.id, f"\n*"
                                           f"{res.json()['quotes'][i]['text']}"
                                           f"*"
                                           f"\n"
                                           f"\nBy {res.json()['quotes'][i]['author']}",
                                     parse_mode='markdown')


def job():
    statement = select(User)
    results = session.exec(statement)

    today = datetime.date.today()
    future = datetime.date(today.year, 12, 31)
    diff = future - today
    for i in results:
        if i.secret_santa_id:
            statement = select(User).where(User.id == i.secret_santa_id)
            results = session.exec(statement)
            user = results.first()
            try:
                updater.bot.send_message(i.id, f" \n*"
                                               f"Au mai ramas {diff.days} zile pina la anul nou."
                                               f"\nGrabeste-te sa cumperi ceva pentru \"{user.alias}\" 🔥🔥"
                                               f"*",
                                         parse_mode='markdown')
            except Exception as e:
                print(e)

        else:
            try:
                updater.bot.send_message(i.id, f" \n*"
                                               f"Au mai ramas {diff.days} zile pina la anul nou. "
                                               f"\nScrie-mi start pentru a seta pe cineva cu-i sa-i fii Santa  🔥🔥"
                                               f"*",
                                         parse_mode='markdown')
            except Exception as e:
                print(e)


schedule.every().day.at("18:00").do(job)  # timezone utz (chisinau timezone is 20:00)
schedule.every().day.at("6:00").do(quotes)  # timezone utz (chisinau timezone is 08:00)

while True:
    schedule.run_pending()
    time.sleep(1)
