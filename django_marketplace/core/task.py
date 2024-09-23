import time
import json
import logging
import os.path

from django.core.exceptions import ValidationError
from celery import shared_task
from celery.utils.log import get_task_logger

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
        logger.info(f"Start import task from {load_path}.")
        for file in json_files:
            if os.path.isfile(file) and file[-5:] == ".json":
                try:
                    with open(file, 'rb') as f:
                        data = json.load(f)
                        products = []
                        count = 0
                        for elem in data:
                            new_product = Product()
                            new_product.name = elem.get("name")
                            new_product.slug = elem.get("slug")
                            new_product.description = elem.get("description", "")
                            new_product.archived = elem.get("archived", False)
                            category_id = elem.get("category_id")
                            new_product.category = Category.objects.get(pk=category_id)
                            try:
                                new_product.full_clean()
                            except ValidationError as e:
                                logging.warning(f'Import error. {elem}\n. {e} ')
                            count += 1
                            products.append(new_product)
                    Product.objects.bulk_create(products)
                    logger.info(f"Import from {file} was done. {count} objects created")
                    src, filename = os.path.split(file)
                    dest = os.path.join(src, "import_done")
                    os.makedirs(dest, exist_ok=True)
                    os.replace(file, os.path.join(dest, filename))
                except Exception as e:
                    logger.error(f'An error occurred while completing the task:\n {e}')
                time.sleep(60*2)
        logger.info(f'Import task finished.')
    else:
        logger.warning('Файлы *.json для импорта не найдены.\n'
                       ' Файлы для импорта с расширением json должны лежать в папке import в корне проекта.')
    return


def task_is_active():
    inspect = app.control.inspect()
    tasks = inspect.active().popitem()[1]  # List of active tasks
    return tasks
