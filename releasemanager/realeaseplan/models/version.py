from django.db import models
from datetime import datetime, timedelta


class Version(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)       # e.g. "Swift"
    number = models.FloatField()                                        # e.g. 18.1
    version_type = models.ForeignKey('VersionType', default=0)
    parent_version = models.ForeignKey('Version', null=True, blank=True,
                                       help_text="In case of a non-major version, select the version that this is patching.")
    released = models.BooleanField(default=False)
    notes = models.TextField()

    def __str__(self):
        s = "{0} {1}".format(self.parent_version or "", self.version_type.resolve_template(self.number))
        if not self.parent_version:
            return self.version_type.resolve_template(self.number)
        return s.format(self.number)


class VersionType(models.Model):
    name = models.CharField(max_length=20, null=True, blank=True, help_text='blank for using the version number as is')
    template = models.CharField(max_length=30, null=True, blank=True,
                                help_text='e.g. "CU{0}", "PR{0}". Leave blank for using the version number as is.')
    level = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    def resolve_template(self, *args):
        tmplt = self.template if "{0}" in self.template else self.template + "{0}"
        return tmplt.format(args)


class VersionDate(models.Model):
    version = models.ForeignKey(Version)
    date_type = models.ForeignKey('VersionDateType')
    date = models.DateField(default=datetime.now() + timedelta(months=2))

    def __str__(self):
        return "{0}: {1}".format(self.date_type, self.date)


class VersionDateType(models.Model):
    name = models.CharField(max_length=20, null=True, blank=True)
    order = models.PositiveSmallIntegerField(null=True, blank=True, help_text="Optional. Use for enforce order, for example: dev -> test -> release")
    is_final = models.BooleanField(default=False)

    def __str__(self):
        return self.name
