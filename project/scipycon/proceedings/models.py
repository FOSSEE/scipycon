from django.db import models
from django.contrib.auth.models import User

from project.scipycon.base import models as base_models


class Paper(base_models.ScopedBase):
    """Data model for storing proceedings paper.
    """

    # Title of the paper
    title = models.CharField(max_length=200)

    # Abstract to be published with the paper
    abstract = models.TextField()

    # Body text of the paper
    body = models.TextField()

    # Authors
    authors = models.ManyToManyField(User)


class Attachments(models.Model):
    """Stores attachments for papers.
    """

    # Attachment for generating paper
    attachments = models.FileField(upload_to='attachments/%Y/%m/%d')

    # The paper to which this attachment belongs to
    paper = models.ForeignKey(Paper)
