from logging import exception
from types import CoroutineType
from typing import Counter
import discord
from discord import channel
from discord import client
from discord.ext import commands
from discord.ext.commands.core import command
import os
import json
from discord.message import Message
import requests
from bs4 import BeautifulSoup
from discord.ext import tasks



with open(r'./Data/api_key.json') as f:
    api_key = json.load(f)

Ruby  = commands.Bot(command_prefix= '#')
Ruby.remove_command('help')

client = discord.Client()

# Personal channel which bot is working

@Ruby.command()
async def help(ctx):
    with open(r'./Data/ruby_commands.json') as f:
        list_of_commands = json.load(f)

    embed = discord.Embed(
    title="List of commands",
    description="Ruby's commands",
    color=discord.Color.dark_orange()
    )
    for keys in list_of_commands.keys():
        embed.add_field(name=keys, value=list_of_commands[keys])
    await ctx.send(embed=embed)

@Ruby.command()
async def ping(ctx):
    await ctx.send("Pong")
    
@Ruby.command()
async def weather(ctx,city = 'Ho Chi Minh', country = None):
    r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city},{country},&units=metric&appid={api_key['api_key']}")
    json_data = r.json()
    weather = json_data['weather'][0]['main']
    description = json_data['weather'][0]['description']
    temp = json_data['main']['temp']
    icon = "http://openweathermap.org/img/wn/" + json_data['weather'][0]['icon'] + "@2x.png"
    feels_like = json_data['main']['feels_like']
    location = json_data['sys']['country']
    embed = discord.Embed(
        title="Current Weather",
        description=f"{city.upper()}",
        color=discord.Color.dark_blue()
    )
    embed.set_thumbnail(url=icon)
    embed.add_field(name=weather, value=description, inline=False)
    embed.add_field(name="Temperature", value=f"{temp}\u2103", inline=False)
    embed.add_field(name="Feels like", value=feels_like)
    embed.add_field(name="Country", value=location)
    print(json.dumps(json_data, indent=4, sort_keys=True))
    await ctx.send(embed=embed)

@weather.error
async def weather_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("That is not a valid city or counter code")

@Ruby.command()
async def news(ctx):
    URL = "https://vnexpress.net/"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    hot_news = soup.find("div", class_="wrapper-topstory-folder wrapper-topstory-folder-v2 wrapper-topstory-home flexbox width_common")
    first_new = hot_news.find("article", class_= "item-news full-thumb article-topstory")
    title = first_new.find("h3", class_= "title-news")
    description = first_new.find("p", class_ = "description")
    ref = title.find("a").get('href')
    embed = discord.Embed(
    title="News",
    description="Top news in Vnexpress.vn",
    color=discord.Color.dark_blue()
    )
    embed.add_field(name='Title', value=title.text)
    embed.add_field(name='Description', value=description.text)
    embed.add_field(name='Link', value=ref)
    await ctx.send(embed=embed)

@Ruby.command()
async def get_time(ctx):
    r = requests.get(f"http://worldtimeapi.org/api/timezone/Asia/Ho_Chi_Minh")
    json_data = r.json()
    print(json_data)


    
###############################################################################
# Event

@Ruby.event
async def on_ready():
    print("Bot ready")
    await Ruby.wait_until_ready()
    print(Ruby.users)
    

Ruby.run('ODcxODA2MzQ5NzA3NzM5MTg2.YQgq7w.udpPpHThdt3Ue0DNYBiVtuzjLbY')


