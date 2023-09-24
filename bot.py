from uuid import uuid4

from loguru import logger
from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import Application, CommandHandler, InlineQueryHandler, filters

from config import config
from stickers.providers import find_sticker_packs


class Bot:
    def __init__(self):
        self.application = Application.builder().token(config.bot.token).build()

    def _add_handlers(self):
        self.application.add_handler(InlineQueryHandler(self._sticker_finder_handler))
        self.application.add_handler(
            CommandHandler(
                "start",
                self._start,
                filters.Chat(username=config.bot.allowed_usernames)
                if config.bot.allowed_usernames
                else None,
            )
        )

    def start(self):
        logger.info("Adding handlers")
        self._add_handlers()

        logger.info("Starting bot")
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

    async def _start(self, update: Update, *args, **kwargs):
        await update.message.reply_text("Hi! oh great master")

    async def _sticker_finder_handler(self, update: Update, *args, **kwargs):
        if (
            config.bot.allowed_usernames
            and update.effective_user.username not in config.bot.allowed_usernames
        ):
            await update.inline_query.answer(
                [
                    InlineQueryResultArticle(
                        id=uuid4(),
                        title="You are not allowed to use this",
                        input_message_content=InputTextMessageContent("bye bye"),
                    )
                ]
            )
            return

        query = update.inline_query.query
        if not query:
            return

        results = [
            InlineQueryResultArticle(
                id=uuid4(),
                title=sticker_pack.name,
                thumbnail_url=sticker_pack.image_url,
                input_message_content=InputTextMessageContent(sticker_pack.link),
                description=sticker_pack.description,
                url=sticker_pack.link,
            )
            for sticker_pack in find_sticker_packs(query)
        ]
        logger.info(
            f"{update.effective_user.username} is searching for {query}, received {len(results)} results"
        )

        await update.inline_query.answer(results)
