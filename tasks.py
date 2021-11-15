import datetime
import time

import schedule
from sqlmodel import select, Session

from main import updater, User, engine

session = Session(engine)


def job():
    statement = select(User)
    results = session.exec(statement)

    today = datetime.date.today()
    future = datetime.date(today.year, 12, 31)
    diff = future - today
    for i in results:
        statement = select(User).where(User.secret_santa_id == i.id)
        results = session.exec(statement)
        user = results.first()
        if user:
            updater.bot.send_message(i.id, f" \n ️  *"
                                           f"Au mai ramas {diff.days} zile pina la anul nou,"
                                           f"grabeste-te sa cumperi ceva pentru {user.alias} 🔥🔥"
                                           f"*",
                                     parse_mode='markdown')


schedule.every().day.at("18:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
