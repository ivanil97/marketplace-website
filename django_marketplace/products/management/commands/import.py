import os

from django.core.management import BaseCommand

from core.settings import BASE_DIR
from core.task import create_task_load_file, task_is_active


class Command(BaseCommand):
    help = "Import json-files to Product Model"

    def handle(self, *args, **options):
        if task_is_active():
            print(f"Import already is working. Can't start new one.")
            return None
        path_to_json = os.path.join(BASE_DIR, 'import')
        file = options["filename"]
        if file:
            path_to_json = os.path.join(path_to_json, file)
            if not (os.path.isfile(path_to_json) and file[-5:] == ".json"):
                print(f"File {path_to_json} is not json-file or not exist")
                return None
        create_task_load_file.delay(path_to_json)

    def add_arguments(self, parser):
        parser.add_argument(
            "filename",
            type=str,
            nargs='?',
            default=None,
            help="load no Product model the specified file",
        )
