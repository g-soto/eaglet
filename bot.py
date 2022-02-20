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
        self.client.add_event_handler(self.new_message)
        await self.sql_engine.connect()
        await self.client.start(bot_token=self.token)

    @events.register(events.ChatAction())
    async def new_message(self, event):
        if isinstance(action := event.action_message.action, (MessageActionChatAddUser, MessageActionChatJoinedByLink)):
            if await self.sql_engine.exists_new_players(action.users):
                await event.respond("**Welcome to Highnest Castle, new recruit.**\n"
                                    "\n"
                                    "Send here the pass that appears on your 🏅Me to earn your Royal Guard Cape!"
                                    "(It should look something like this: FLY HIG)\n"
                                    "\n"
                                    "**Please register to @BotnestBot.**\n"
                                    "Type /auth in @BotnestBot to get the code from your @chtwrsbot then forward the code "
                                    "to @BotnestBot.\n"
                                    "\n"
                                    "When you reach lvl 5, go to @BotnestBot to "
                                    "⚜️Squad⚜️-> ⚜️Join Squad -> Eaglet's Eyrie to join the new group and "
                                    "receive orders there.\n"
                                    "\n"
                                    "Now Fly High, recruit!🦅")
            else:
                await event.respond("🎵You know the rules and so do i.🎵")

