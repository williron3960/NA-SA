from fastapi import FastAPI, Response, status, Form
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String ,DateTime ,Boolean
from typing import List, Optional
import datetime, random, uuid
from requests.utils import requote_uri
from urllib.parse import unquote
import requests

# body
import pg_db
import model
database = pg_db.database
items = pg_db.items

# enable CORS
origins = [
    "*"
]

# fastapi
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event('startup')
async def startup():
    await database.connect()

@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()


@app.post('/set/{key}' )
async def set_value(key : Optional[str] = None, value: Optional[str] =  Form(None) ):
    gDate = datetime.datetime.now()
    if value != None:
        try :
            query = items.insert().values(
                value = value,
                key = key,
                create_at = gDate
            )
            await database.execute(query)
            return 'OK'
        except :
                query = items.update().\
                where(items.c.key == key).\
                values(
                    value = value,
                    create_at = gDate
                )
                await database.execute(query)
                return 'OK'
    else:
        try :
            query = items.insert().values(
                value = str(),
                key = key,
                create_at = gDate
            )
            await database.execute(query)
            return 'OK'
        except :
                query = items.update().\
                where(items.c.key == key).\
                values(
                    value = str(),
                    create_at = gDate
                )
                await database.execute(query)
                return 'OK'

@app.post('/set/' )
async def set_value(key : Optional[str] = Form(None), value: Optional[str] =  Form(None) ):
    gDate = datetime.datetime.now()
    try :
        query = items.insert().values(
            value = value,
            key = str(),
            create_at = gDate
        )
        await database.execute(query)
        return 'OK'
    except :
            query = items.update().\
            where(items.c.key == key).\
            values(
                value = value,
                create_at = gDate
            )
            await database.execute(query)
            return 'OK'


@app.get('/get/{key}' )
async def find_value(key : str = None):
    try :
        query = items.select().where(items.c.key == key )
        query = await database.fetch_one(query)
        value = model.Item(**query).dict()["value"]
        return PlainTextResponse(value, 200)
    except :
        return 'key not found!'

@app.get('/get/' )
async def find_value(key : Optional[str] = Form(None)):
    try :
        query = items.select().where(items.c.key == str() )
        query = await database.fetch_one(query)
        value = model.Item(**query).dict()["value"]
        return PlainTextResponse(value, 200)
    except :
        return 'key not found!'
