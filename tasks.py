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

while True:
    schedule.run_pending()
    time.sleep(1)
