import random
from typing import Optional

from fastapi import FastAPI, Request, Depends
from sqlmodel import SQLModel, create_engine, Session, select, Field, Relationship
from telegram.ext import Updater

app = FastAPI()


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    alias: str
    exclude_id: str
    secret_santa_id: Optional[int] = Field(default=None, foreign_key="user.id")
    secret_santa: "User" = Relationship()


sqlite_url = f"postgresql://point:point@165.22.80.225:5438/point"

engine = create_engine(sqlite_url, echo=True)


async def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


updater = Updater("2142480007:AAG_VYXS4P8f-0IWJwhJWXCFCO5NyWBV0Xw")


@app.on_event("startup")
async def startup_event():
    await init_db()
    # users = [
    #     User(
    #         id=1419525126,
    #         alias='Java',
    #         exclude_id=1145691161,
    #     ),
    #     User(
    #         id=1145691161,
    #         alias='Pavlik',
    #         exclude_id=1419525126,
    #     ),
    #     User(
    #         id=1690526936,
    #         alias='Iulicika (Hr - ISD)',
    #         exclude_id=730014397,
    #     ),
    #     User(
    #         id=730014397,
    #         alias='Python god',
    #         exclude_id=1690526936,
    #     ),
    #     User(
    #         id=465806107,
    #         alias='Frontendshik',
    #         exclude_id=473684260,
    #     ),
    #     User(
    #         id=473684260,
    #         alias='Inacika (simpals)',
    #         exclude_id=465806107,
    #     ),
    #     User(
    #         id=1294049219,
    #         alias='Glorita (Top Tester)',
    #         exclude_id=665682607,
    #     ),
    #     User(
    #         id=665682607,
    #         alias='Rijic (Top Sales Manager (software))',
    #         exclude_id=1294049219,
    #     ),
    #     User(
    #         id=787956385,
    #         alias='Penis mare (pokeristu)',
    #         exclude_id=1145691161,
    #     ),
    # ]




@app.post("/")
async def root(request: Request, session: Session = Depends(get_session)):
    data = await request.json()
    statement = select(User).where(User.id == data['message']['from'].get('id'))
    results = session.exec(statement)
    user = results.first()

    if not user:
        updater.bot.send_message(data['message']['chat']['id'], "Intrus")

    if user.secret_santa:
        updater.bot.send_message(user.id, f"*Esti secret santa pentru {user.secret_santa.alias}*",
                                 parse_mode='markdown')

    statement = select(User).where(User.id.not_in([
        data['message']['chat']['id'], user.exclude_id
    ]), User.secret_santa_id._is(None))  # noqa
    results = session.exec(statement)

    if list(results):
        updater.bot.send_message(data['message']['chat']['id'], "Intrus")

    choice = random.choice(list(results))
    choice.secret_santa_id = choice.id
    session.add(choice)
    session.commit()
    updater.bot.send_message(user.id, f" \n ↘️  *Felicitatus domnu, esti secret santa pentru*  ↙️ "
                                      f" \n        🎁🎁🎁 \" *{choice.alias}* \" 🎁🎁🎁\n ",
                             parse_mode='markdown')
    return {"message": "Hello World"}
