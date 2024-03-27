from django.apps import AppConfig


class DjangoGroupModelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_group_model'

    def ready(self):
        from django.conf import settings
        from django.contrib.auth.backends import ModelBackend
        from django.contrib.auth.models import Permission
        from django.contrib.auth import get_user_model

        def _get_group_permissions(self, user_obj):
            group_model = settings.AUTH_GROUP_MODEL
            related_name_to_group = group_model.split('.')[-1].lower()

            user_groups_field = get_user_model()._meta.get_field(f"{related_name_to_group}s")
            user_groups_query = f"{related_name_to_group}__{user_groups_field.related_query_name()}"
            return Permission.objects.filter(**{user_groups_query: user_obj})


        ModelBackend._get_group_permissions = _get_group_permissions
