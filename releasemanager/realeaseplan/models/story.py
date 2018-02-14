from django.db import models
from realeaseplan.models.team import Team
from realeaseplan.models.version import Version
from realeaseplan.models.lookups import Person

STORY_LINK_TEMPLATE = "http://dbm-jira:8080/browse/{0}"

STORY_STATUS_CHOICES = (
    ('ReleaseBacklog', 'Release Backlog'),
    ('Ready4Dev', 'Ready4Dev'),
    ('InProgress', 'In Progress'),
    ('Done', 'Done'),
    ('Trash', 'Trash'),
)


class Story(models.Model):
    name = models.CharField(max_length=300)
    details = models.TextField()
    version = models.ForeignKey(Version, null=True, blank=True)
    teams = models.ManyToManyField(Team, through="StoryToTeam")
    links = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STORY_STATUS_CHOICES, null=True, blank=True)
    project_manager = models.ForeignKey(Person, null=True, blank=True)
    dev_manager = models.ForeignKey(Person, null=True, blank=True)

    def __str__(self):
        return self.name

    def links_html(self):
        # ST-1406, ST-809 will produce the following html:
        # <a href="http://dbm-jira:8080/browse/ST-1406">ST-1406</a>, <a href="http://dbm-jira:8080/browse/ST-809">ST-809</a>
        ', '.join('<a href="{link}">{text}</a>'.format(link=STORY_LINK_TEMPLATE.format(l), text=l) for l in self.links.split(','))

    class Meta:
        verbose_name_plural = "Stories"


class StoryToTeam(models.Model):
    team = models.ForeignKey(Team)
    story = models.ForeignKey(Story)
    points = models.FloatField()

    def __str__(self):
        return self.points

    class Meta:
        unique_together = ("team", "story")
