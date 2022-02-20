import yaml
from telethon.sync import TelegramClient, events
from telethon.tl.types import MessageActionChatAddUser, MessageActionChatJoinedByLink

from SQL import SQL

class Eaglet:
    def __init__(self):
        with open("settings.yml", "rt") as yml_file:
            settings = yaml.load(yml_file, yaml.SafeLoader)
        # noinspection PyTypeChecker
        self.client = TelegramClient(session=settings["session"],
                                     api_id=settings["api_id"], api_hash=settings["api_hash"], connection_retries=None)
        self.token = settings["token"]
        self.sql_engine = SQL()
        self.run_until_disconnected = self.client.run_until_disconnected

    async def disconnect(self):
        await self.client.disconnect()

    async def start(self):
        self.client.add_event_handler(self.new_action)
        await self.sql_engine.connect()
        await self.client.start(bot_token=self.token)

    @events.register(events.ChatAction())
    async def new_action(self, event):
        if isinstance(action := event.action_message.action, (MessageActionChatAddUser, MessageActionChatJoinedByLink)):
            if await self.sql_engine.exists_new_players(action.users):
                await event.respond(f"**Welcome to {(await event.get_chat()).title}**\n"
                                    f"\n"
                                    f"There is some rules:\n"
                                    f"1. Leave [Xhitz](tg://user?id=604636308) alone😌")
            else:
                await event.respond("🎵You know the rules and so do i.🎵")

