import asyncio
import discord
import numpy as np

from datetime import datetime, timedelta
from discord.ext import commands
from pybit.unified_trading import HTTP
from talipp.indicators import RSI


TOKEN = (
    'MTI1NDcxMTg4MjUxODg4ODU4Mg.GbUn-P.NRkAtV2tfzAvBUFaHTsv5TNmBiLNq4x1qkIDSY'
)
RSI_SETTINGS = {
    'period': 14,
    'interval': 60
}

# Discord API Bot
intents = discord.Intents(messages=True, message_content=True)
bot = commands.Bot(command_prefix='!', intents=intents)
# Bybit API session
session = HTTP(testnet=True)


def get_kline_data(periods, interval):
    """ Fetch Bybit API data, return completed candles (ommit current).

    Parameters:
        periods (int): Number of candles to import (includind the current one)
        interval (int): Timeframe of candlestick chart (60M = 1H)

    Return: 
        numpy.ndarray: [Timestamp, Open, High, Low, Close, Volume, Turnover]
    """
    data = session.get_kline(
        category='linear',
        symbol='SOLUSDT',
        interval=interval,
        limit=periods
    )
    data = np.asarray(data['result']['list'][::-1]).astype(float)
    data = data[:-1]
    print(data)
    return data


def calc_RSI(periods, interval):
    """ Calculate RSI indicator

    Parameters:
        periods (int): Number of candles to calculate RSI
        interval (int): Timeframe of candlestick chart (60M = 1H)

    Return: 
        float: The RSI value for the last candle.
    """
    data = get_kline_data(periods + 2, interval) # +1 for RSI, +1 for current 
    close = data[:, 4] 
    rsi = RSI(period=periods, input_values=close)
    return rsi[-1]


@bot.event
async def on_ready():
    print(f'Successfully logged in as {bot.user} (id: {bot.user.id})')


@bot.command()
async def start(ctx):
    await ctx.send('You have signed up for SOL/USDT signals.')
    await ctx.send('When the RSI reaches extreme values we will let you know')
    bot.loop.create_task(check_RSI(ctx))


async def check_RSI(ctx):
    """ Calculate RSI at the beginning of each hour.
    Send alert if RSI value is extreme (above 70 or below 30)
    """
    while not bot.is_closed():
        now = datetime.now()
        # delta should keep the consistency with RSI_SETTINGS['interval']
        delta = timedelta(
            hours=1,
            minutes=-now.minute, 
            seconds=-now.second, 
            microseconds=-now.microsecond,
        ).total_seconds()
        delta += 1 # compenstation for sleep inaccuracy 
        await asyncio.sleep(delta) 

        rsi = calc_RSI(RSI_SETTINGS['period'], RSI_SETTINGS['interval'])
        if rsi > 70:
            await ctx.send(f'The RSI is so high: {rsi:.2f}.')
        if rsi < 30:
            await ctx.send(f'The RSI is so low: {rsi:.2f}.')
        #await ctx.send('The time is {:%H:%M:%S}.'.format(datetime.now()))


bot.run(TOKEN)