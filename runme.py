import asyncio
import logging

from bot import Eaglet

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARNING)


async def main(bot):
    await bot.start()
    await bot.run_until_disconnected()


if __name__ == '__main__':
    main_bot = Eaglet()
    try:
        asyncio.run(main(main_bot))
    except KeyboardInterrupt:
        asyncio.run(main_bot.disconnect())
