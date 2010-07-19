from django.db import models
from django.core.management.validation import max_length


class Event(models.Model):
    """Data model which holds the data related to the scope or the event.
    """

    # Different states the Event can be in
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )

    # Scope of the program, used as a URL prefix
    scope = models.CharField(max_length=255)

    # Name of the program
    name = models.CharField(max_length=255)

    # Event specific i.e version of the event
    turn = models.CharField(max_length=255)

    # Time associated with the program
    timeline = models.OneToOneField(Timeline)

    # Status of the program
    status = models.CharField(max_length=255, choices=STATUS_CHOICES)


class Timeline(models.Model):
    """Timeline of the program
    """

    # Start of registration for the program
    registration_start = models.DateTimeField()

    # End of registration for the program
    registration_end = models.DateTimeField()

    # Start of Call for Papers
    cfp_start = models.DateTimeField()

    # End of Call for Papers
    cfp_end = models.DateTimeField()

    # Accepted papers announced
    accepted_papers_announced = models.DateTimeField()

    # Deadline to submit proceedings paper
    proceedings_paper_deadline = models.DateTimeField()

    # Start of the actual program
    event_start = models.DateTimeField()

    # End of the actual program
    event_end = models.DateTimeField()


class ScopedBase(models.Model):
    """Base model which is in turn inherited by other models
    which needs to be scoped.
    """

    # Scope of entity in which it is visible
    scope = models.ForeignKey(Scope)

    class Meta:
        abstract = True
