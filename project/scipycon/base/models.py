from django.db import models


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

    # Status of the program
    status = models.CharField(max_length=255, choices=STATUS_CHOICES)

    def __unicode__(self):
        return '%s %s' % (self.name, self.turn)

    def get_full_name(self):
        return self.__unicode__()


class Timeline(models.Model):
    """Timeline of the program
    """

    # Event with which this timeline is associated
    event = models.OneToOneField(Event)

    # Start of registration for the program
    registration_start = models.DateTimeField(blank=True, null=True)

    # End of registration for the program
    registration_end = models.DateTimeField(blank=True, null=True)

    # Start of Call for Papers
    cfp_start = models.DateTimeField(blank=True, null=True)

    # End of Call for Papers
    cfp_end = models.DateTimeField(blank=True, null=True)

    # Accepted papers announced
    accepted_papers_announced = models.DateTimeField(blank=True, null=True)

    # Deadline to submit proceedings paper
    proceedings_paper_deadline = models.DateTimeField(blank=True, null=True)

    # Start of the actual program
    event_start = models.DateTimeField(blank=True, null=True)

    # End of the actual program
    event_end = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return '%s %s' % (self.event.name, self.event.turn)


class ScopedBase(models.Model):
    """Base model which is in turn inherited by other models
    which needs to be scoped.
    """

    # Scope of entity in which it is visible
    scope = models.ForeignKey(Event)

    class Meta:
        abstract = True


class Paid(models.Model):
    event_start = models.DateTimeField(blank=True, null=True)
