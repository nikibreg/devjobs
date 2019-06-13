import random
import asyncio
from jinja2 import Environment, FileSystemLoader
from sanic import Sanic
from sanic.response import json, html
from templates import render_template
from parsejobs import parse

app = Sanic()

async def getStatements():
    statements = await parse()

@app.route('/')
async def index(request):
    statements = await parse()
    random.shuffle(statements)
    return html(render_template('index.html', statements=statements))

app.run()