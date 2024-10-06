import time
import json
import logging
import os.path

from django.core.exceptions import ValidationError, ObjectDoesNotExist
from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.mail import send_mail

from core import settings
from core.celery import app
from products.models import Product, Category

logger = get_task_logger(__name__)


@shared_task
def create_task_load_file(load_path: str):
    if os.path.isdir(load_path):
        json_files = [os.path.join(load_path, elem) for elem in os.scandir(load_path)]
    else:
        json_files = [load_path, ]
    if json_files:
        logger.info(f"Start import task from {load_path}\n{json_files}.")
        files_imported = 0
        files_error = 0
        for file in json_files:
            if os.path.isfile(file) and file[-5:] == ".json":
                with open(file, 'rb') as f:
                    data = json.load(f)
                    products = []
                    count = 0
                    is_error = False
                    for elem in data:
                        new_product = Product()
                        new_product.name = elem.get("name")
                        new_product.slug = elem.get("slug")
                        new_product.description = elem.get("description", "")
                        new_product.archived = elem.get("archived", False)
                        category_id = elem.get("category_id")
                        try:
                            new_product.category = Category.objects.get(pk=category_id)
                            new_product.full_clean()
                        except ObjectDoesNotExist as err:
                            logging.error(
                                f'{elem} Import error. Category does not exist id={category_id}\n. {err}'
                            )
                            is_error = True
                        except ValidationError as err:
                            logging.error(f'{elem} Import error. Validation failed\n. {err} ')
                            is_error = True
                        else:
                            logging.warning(f'{elem} Import success.')
                            count += 1
                            products.append(new_product)
                if is_error:
                    files_error += 1
                    logger.warning(f"Import {file} failed. There are errors when importing.")
                    move_to = 'import_error'
                else:
                    files_imported += 1
                    Product.objects.bulk_create(products)
                    logger.info(f"Import from {file} was done. {count} objects created")
                    move_to = 'import_done'
                src, filename = os.path.split(file)
                dest = os.path.join(src, move_to)
                os.makedirs(dest, exist_ok=True)
                os.replace(file, os.path.join(dest, filename))
        logger.info(f'Import task finished. Files {files_imported} - Ok, {files_error} - error.')
        send_mail(
            'Import Django-Marketplace',
            f'Import task finished. Files {files_imported} - Ok, {files_error} - error.',
            settings.EMAIL_HOST_USER,
            ['andr73@yahoo.com'],
        )
    else:
        logger.warning('Файлы *.json для импорта не найдены.\n'
                       ' Файлы для импорта с расширением json должны лежать в папке import в корне проекта.')
    return


def task_is_active():
    inspect = app.control.inspect()
    tasks = inspect.active().popitem()[1]  # List of active tasks
    return tasks
