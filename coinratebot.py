import requests
import os

from aiogram import Dispatcher, Bot, types, executor

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())


TOKEN = os.getenv('TOKEN')
bot = Bot(TOKEN)
dp = Dispatcher(bot)

# функция получения текущего курса покупки монеты с разных бирж
async def check_rates(coin):

  results = ""

  # Bybit
  try:
      url = f'https://api.bybit.com/v2/public/tickers?symbol={coin}USDT'
      response = requests.get(url)
      response.raise_for_status()
      data = response.json()
      if data['ret_msg'] == 'OK':
          bid_price = float(data['result'][0]['bid_price'])
          results += f'Bybit: {bid_price}\n'
      else:
          results += f'Bybit: монета {coin} не найдена на бирже Bybit.\n'
  except (requests.exceptions.HTTPError, IndexError):
      results += f'Bybit: монета {coin} не найдена на бирже Bybit.\n'

  # Binance
  try:
      url = f'https://api.binance.com/api/v3/ticker/bookTicker?symbol={coin}USDT'
      response = requests.get(url)
      response.raise_for_status()
      data = response.json()
      if 'bidPrice' in data:
          bid_price = data['bidPrice']
          results += f'Binance: {bid_price}\n'
      else:
          results += f'Binance: монета {coin} не найдена на бирже Binance.\n'
  except (requests.exceptions.HTTPError, IndexError):
      results += f'Binance: монета {coin} не найдена на бирже Binance.\n'

  # BingX
  try:
      url = f'https://open-api.bingx.com/openApi/swap/v2/quote/ticker?symbol={coin}-USDT'
      response = requests.get(url)
      response.raise_for_status()
      data = response.json()
      if 'data' in data and data['data']['bidPrice'] != "":
          bid_price = data['data']['bidPrice']
          results += f'BingX: {bid_price}\n'
      else:
          results += f'BingX: монета {coin} не найдена на бирже BingX.\n'
  except (requests.exceptions.HTTPError, IndexError):
      results += f'BingX: монета {coin} не найдена на бирже BingX.\n'

  # Bitget
  try:
      url = f'https://api.bitget.com/api/v2/spot/market/tickers?symbol={coin}USDT'
      response = requests.get(url)
      response.raise_for_status()
      data = response.json()
      if data['msg'] == "success":
          bid_price = data['data'][0]['bidPr']
          results += f'Bitget: {bid_price}\n'
      else:
          results += f'Bitget: монета {coin} не найдена на бирже Bitget.\n'
  except (requests.exceptions.HTTPError, IndexError):
      results += f'Bitget: монета {coin} не найдена на бирже Bitget.\n'

  # Kucoin
  try:
      url = f'https://api.kucoin.com/api/v1/market/orderbook/level1?symbol={coin}-USDT'
      response = requests.get(url)
      response.raise_for_status()
      data = response.json()
      if data['data'] != None:
          bid_price = data['data']['bestBid']
          results += f'Kucoin: {bid_price}\n'
      else:
          results += f'Kucoin: монета {coin} не найдена на бирже Kucoin.\n'
  except (requests.exceptions.HTTPError, requests.exceptions.HTTPError):
      results += f'Kucoin: монета {coin} не найдена на бирже Kucoin.\n'

  return results

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_message('5812314624', f'Юзер @{message.chat.username} c id {message.from_user.id} сейчас использует бота')
    await message.answer("Пришли мне монету (пример: LTC), а я покажу текущий курс покупки на биржах Bybit, Binance, BingX, Bitget, Kucoin.")


@dp.message_handler()
async def cmd_go(message: types.Message):
    await message.answer("дай мне пару секунд...")
    coin = message.text.upper()
    if coin == 'ДЕД':
        results = await check_rates('BTC')
        await bot.send_message(message.chat.id, f'Текущий курс валютной пары BTC/USDT:\n{results}')
    else:
        results = await check_rates(coin)
        await bot.send_message(message.chat.id, f'Текущий курс валютной пары {coin}/USDT:\n{results}')


# Запуск
if __name__ == "__main__":
    executor.start_polling(
        dispatcher=dp,
        skip_updates=True
    )