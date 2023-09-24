from uuid import uuid4

from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import (
    Updater,
    Filters,
    CallbackContext,
    InlineQueryHandler,
    CommandHandler,
)

from config import config
from loguru import logger

from stickers.providers import find_sticker_packs


class Bot:
    def __init__(self):
        self.updater = Updater(token=config.bot.token, use_context=True)

    def _add_handlers(self):
        self.updater.dispatcher.add_handler(
            InlineQueryHandler(self._sticker_finder_handler, run_async=True)
        )

        self.updater.dispatcher.add_handler(
            CommandHandler(
                "start",
                lambda update, _: update.message.reply_text("Hi! oh great master"),
                Filters.chat(username=config.bot.allowed_usernames)
                if config.bot.allowed_usernames
                else None,
                run_async=True,
            )
        )

    def start(self):
        logger.info("Adding handlers")
        self._add_handlers()

        logger.info("Starting bot")
        self.updater.start_polling()
        self.updater.idle()

    def _sticker_finder_handler(self, update: Update, _: CallbackContext):
        if (
            config.bot.allowed_usernames
            and update.effective_user.username not in config.bot.allowed_usernames
        ):
            update.inline_query.answer(
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
                thumb_url=sticker_pack.image_url,
                input_message_content=InputTextMessageContent(sticker_pack.link),
                description=sticker_pack.description,
                url=sticker_pack.link,
            )
            for sticker_pack in find_sticker_packs(query)
        ]
        logger.info(
            f"{update.effective_user.username} is searching for {query}, received {len(results)} results"
        )

        update.inline_query.answer(results)
