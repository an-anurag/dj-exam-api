from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Question(models.Model):
    """
    file,
    """
    QUE_TYPE_CHOICE = (
        ('helping_others', 'Helping others'),
        ('communicational', 'Communicational'),
        ('organizational', 'Organizational'),
    )

    OPTION_CHOICE = (
        ('strongly_agree', 'Strongly agree'),
        ('agree', 'Agree'),
        ('neutral', 'Neutral'),
        ('disagree', 'Disagree'),
        ('strongly_disagree', 'Strongly Disagree'),
    )
    question = models.CharField(max_length=1000)
    selected_option = models.CharField(max_length=30, choices=OPTION_CHOICE, blank=True, null=True)
    que_type = models.CharField(max_length=30, choices=QUE_TYPE_CHOICE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.question


class Result(models.Model):

    score = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user.username)
