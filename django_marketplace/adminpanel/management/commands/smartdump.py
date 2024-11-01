import gzip
import os
import warnings

from django.apps import apps
from django.core import serializers
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.core.management.utils import parse_apps_and_model_labels
from django.db import DEFAULT_DB_ALIAS, connections, router
from django.conf import settings

try:
    import bz2

    has_bz2 = True
except ImportError:
    has_bz2 = False

try:
    import lzma

    has_lzma = True
except ImportError:
    has_lzma = False


class ProxyModelWarning(Warning):
    pass


class Command(BaseCommand):
    help = (
        "Output the contents of the database as a fixture of the given format "
        "(using each model's default manager unless --all is specified)."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "args",
            metavar="app_label[.ModelName]",
            nargs="*",
            help=(
                "Restricts dumped data to the specified app_label or "
                "app_label.ModelName."
            ),
        )
        parser.add_argument(
            "--format",
            default="json",
            help="Specifies the output serialization format for fixtures.",
        )
        parser.add_argument(
            "--indent",
            type=int,
            help="Specifies the indent level to use when pretty-printing output.",
        )
        parser.add_argument(
            "--database",
            default=DEFAULT_DB_ALIAS,
            choices=tuple(connections),
            help="Nominates a specific database to dump fixtures from. "
            'Defaults to the "default" database.',
        )
        parser.add_argument(
            "-e",
            "--exclude",
            action="append",
            default=[],
            help="An app_label or app_label.ModelName to exclude "
            "(use multiple --exclude to exclude multiple apps/models).",
        )
        parser.add_argument(
            "--natural-foreign",
            action="store_true",
            dest="use_natural_foreign_keys",
            help="Use natural foreign keys if they are available.",
        )
        parser.add_argument(
            "--natural-primary",
            action="store_true",
            dest="use_natural_primary_keys",
            help="Use natural primary keys if they are available.",
        )
        parser.add_argument(
            "-a",
            "--all",
            action="store_true",
            dest="use_base_manager",
            help=(
                "Use Django's base manager to dump all models stored in the database, "
                "including those that would otherwise be filtered or modified by a "
                "custom manager."
            ),
        )
        parser.add_argument(
            "--pks",
            dest="primary_keys",
            help="Only dump objects with given primary keys. Accepts a comma-separated "
            "list of keys. This option only works when you specify one model.",
        )
        parser.add_argument(
            "-o", "--output", help="Specifies DIR to which the output is written."
        )
        parser.add_argument(
            "-x", "--ext",
            dest="extension",
            default="json",
            help="Specifies file extension for output.",
        )

    def handle(self, *app_labels, **options):
        format = options["format"]
        indent = options["indent"]
        using = options["database"]
        excludes = options["exclude"]
        output = options["output"]
        show_traceback = options["traceback"]
        use_natural_foreign_keys = options["use_natural_foreign_keys"]
        use_natural_primary_keys = options["use_natural_primary_keys"]
        use_base_manager = options["use_base_manager"]
        pks = options["primary_keys"]
        ext = options["extension"]

        if pks:
            primary_keys = [pk.strip() for pk in pks.split(",")]
        else:
            primary_keys = []

        excluded_models, excluded_apps = parse_apps_and_model_labels(excludes)

        if not app_labels:
            if primary_keys:
                raise CommandError("You can only use --pks option with one model")
            app_list = dict.fromkeys(
                app_config
                for app_config in apps.get_app_configs()
                if app_config.models_module is not None
                and app_config not in excluded_apps
            )
        else:
            if len(app_labels) > 1 and primary_keys:
                raise CommandError("You can only use --pks option with one model")
            app_list = {}
            for label in app_labels:
                try:
                    app_label, model_label = label.split(".")
                    try:
                        app_config = apps.get_app_config(app_label)
                    except LookupError as e:
                        raise CommandError(str(e))
                    if app_config.models_module is None or app_config in excluded_apps:
                        continue
                    try:
                        model = app_config.get_model(model_label)
                    except LookupError:
                        raise CommandError(
                            "Unknown model: %s.%s" % (app_label, model_label)
                        )

                    app_list_value = app_list.setdefault(app_config, [])

                    # We may have previously seen an "all-models" request for
                    # this app (no model qualifier was given). In this case
                    # there is no need adding specific models to the list.
                    if app_list_value is not None and model not in app_list_value:
                        app_list_value.append(model)
                except ValueError:
                    if primary_keys:
                        raise CommandError(
                            "You can only use --pks option with one model"
                        )
                    # This is just an app - no model qualifier
                    app_label = label
                    try:
                        app_config = apps.get_app_config(app_label)
                    except LookupError as e:
                        raise CommandError(str(e))
                    if app_config.models_module is None or app_config in excluded_apps:
                        continue
                    app_list[app_config] = None

        if use_natural_foreign_keys:
            models = serializers.sort_dependencies(
                app_list.items(), allow_cycles=True
            )
        else:
            # There is no need to sort dependencies when natural foreign
            # keys are not used.
            models = []
            for app_config, model_list in app_list.items():
                if model_list is None:
                    models.extend(
                        [(app_config.label + '.' + model.__name__, model)
                         for model in app_config.get_models()]
                    )
                    # models.extend(app_config.get_models())
                else:
                    models.extend(
                        [(app_config.label + '.' + model.__name__, model)
                         for model in model_list]
                    )
        options_for_dumpdata = dict(options)
        options_for_dumpdata.pop("extension")
        for app_dot_model, model in models:
            if model in excluded_models:
                continue
            if model._meta.proxy and model._meta.proxy_for_model not in models:
                warnings.warn(
                    "%s is a proxy model and won't be serialized."
                    % model._meta.label,
                    category=ProxyModelWarning,
                )
            if not model._meta.proxy and router.allow_migrate_model(using, model):
                if use_base_manager:
                    objects = model._base_manager
                else:
                    objects = model._default_manager

                queryset = objects.using(using).order_by(model._meta.pk.name)
                if primary_keys:
                    queryset = queryset.filter(pk__in=primary_keys)
                if queryset.order_by().count():
                    if output:
                        file_path = output + app_dot_model.replace('.', '_')
                    else:
                        file_path = str(settings.BASE_DIR) + app_dot_model.replace('.', '_')
                    file_path += '.' + options["extension"]
                    print(file_path)
                    options_for_dumpdata['output'] = file_path
                    app_labels = [app_dot_model,]
                    call_command("dumpdata", *app_labels, **options_for_dumpdata)
