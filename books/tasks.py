
import logging
import time
from random import randint, choice

from celery import shared_task

from books.models import Author, Book
from bookstore.celery import app
from bookstore.telegram_bot import send_message_to_bot

logger = logging.getLogger('django')


#@shared_task
@app.task
def clicked(author_ads_settings_author: str = '<>', author_ads_settings_url: str = '<>'):
    # time.sleep(15)
    # rand_base = randint(0, 1)
    # if rand_base == 0:
    #     base = Author.objects.all()
    # else:
    #     base = Book.objects.all()
    # rand_object = choice(base)
    instance = f'BOOKSTORE {author_ads_settings_author} - {author_ads_settings_url}'
    send_message_to_bot(instance=instance)
    logger.info(instance)