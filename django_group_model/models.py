from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Permission, GroupManager


# This class has been copied from django.contrib.auth.models.Group
# The only additional thing set is abstract=True in meta
# This class should not be updated unless replacing it with a new version from django.contrib.auth.models.Group
class AbstractGroup(models.Model):
    name = models.CharField(_("name"), max_length=150, unique=True)
    permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("permissions"),
        blank=True,
    )

    objects = GroupManager()

    class Meta:
        verbose_name = _("group")
        verbose_name_plural = _("groups")
        abstract = True

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.name,)
