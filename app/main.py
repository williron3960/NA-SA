from fastapi import FastAPI, Response, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String ,DateTime ,Boolean
from typing import List, Optional
import datetime, random, uuid

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

@app.post('/set/{value}' )
async def set_value(value: str):
    gDate = datetime.datetime.now()
    try :
        query = items.insert().values(
            value = value,
            create_at = gDate
        )
        await database.execute(query)
        return {
            'value' : value
        }
    except :
        query = items.update().\
        where(items.c.value == value).\
        values(
            value = value,
            create_at = gDate
        )
        await database.execute(query)
        return {
            'value' : value + '_updated'
        }

@app.get('/get/{value}' )
async def find_value(value : str):
    query = items.select().where(items.c.value == value )
    return await database.fetch_one(query)
