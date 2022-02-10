from tkinter.tix import Tree
from django.db import models

EVENT_CHOICES = (
    ('technical', 'Technical'),
    ('workshop', 'Workshop'),
    ('informal', 'Informal'),
    ('exhibition', 'Exhibition'),
    ('talk', 'Talk'),
    ('panel_discussion', 'Panel Discussion'),
    ('initiative', 'Initiative'),
    ('entrepreneurial', 'Entrepreneurial'),
)

EVENT_PARTICIPATION = (
    ('individual', 'Individual Event'),
    ('team', 'Team Event'),
)


class Brochure(models.Model):
    name = models.CharField(max_length=100, verbose_name='Document name', null=False, blank=False)
    type = models.CharField(max_length=30, choices=EVENT_CHOICES+(('schedule_file', 'schedule_file'),), default='technical', verbose_name='Event Type')
    file = models.FileField(upload_to='brochures/', null=False, blank=False, verbose_name='File')

    def __str__(self):
        return self.name


class Event(models.Model):
    # Event Details
    name = models.CharField(max_length=50, verbose_name="Event Name", unique=True, blank=False, null=False)
    type = models.CharField(max_length=30, choices=EVENT_CHOICES, default='event', verbose_name='Event Type')
    speaker = models.CharField(max_length=50, null=True, blank=True, verbose_name="If Talk mention speaker's name (Else leave empty)")
    designation = models.CharField(max_length=50, null=True, blank=True, verbose_name="Speaker Designation (only for Talk)")
    description = models.TextField(max_length=5000, null=True, blank=True, verbose_name="Event Description (Write more for speaker description)")
    prize = models.CharField(max_length=100, verbose_name="Prize Money (Rs.)", null=True, blank=True, default="Prizes worth Rs.")
    external_link = models.URLField(max_length=500, null=True, blank=True, verbose_name="External Link for Registration")
    venue = models.CharField(max_length=50, null=True, blank=True, verbose_name="Event Venue")
    featured = models.BooleanField(verbose_name="Display on home page", default=False, blank=True)

    # Event Registration Details
    participation_type = models.CharField(max_length=25, choices=EVENT_PARTICIPATION, default='individual', verbose_name="Participation Type")
    min_team_size = models.IntegerField(verbose_name="Minimum Team Size (leave unchanged for individual event)", default=1)
    max_team_size = models.IntegerField(verbose_name="Maximum Team Size (leave unchanged for individual event)", default=1)
    registration_open = models.BooleanField(verbose_name="Registrations Open", default=True, blank=True)
    submission_link = models.URLField(max_length=500, null=True, blank=True, verbose_name="Event submission link")

    # Event Dates
    date = models.DateField(verbose_name="Event Date (Leave unchanged if the date is not decided)", null=False, blank=False, default="2023-01-01")
    time = models.TimeField(null=False, blank=False, verbose_name="Event Time")
    end_date = models.DateField(verbose_name="Event end Date", null=False, blank=False, default="2023-01-01")
    end_time = models.TimeField(null=False, blank=False, verbose_name="Event end Time")
    event_started = models.BooleanField(verbose_name="Event started", default=False, blank=True)
    
    # Streaming Links
    meet_link = models.URLField(max_length=500, null=True, blank=True, verbose_name="meet Link for streaming")
    youtube_link = models.URLField(max_length=500, null=True, blank=True, verbose_name="youtube Link for streaming")
    webx_link = models.URLField(max_length=500, null=True, blank=True, verbose_name="webX Link for streaming")

    # Event Uploads
    image = models.ImageField(upload_to="images/", verbose_name="Cover Image(prefer uploading square images)(for speakers upload images with more padding, i.e, face in the center)", blank=False, null=False)
    rulebook = models.FileField(upload_to="rulebooks/", null=True, blank=True, verbose_name="Rulebook File")
    material_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Material Name")
    material = models.FileField(upload_to="supplementaryMaterials/", null=True, blank=True, verbose_name="Supplementary Material")

    def __str__(self):
        return self.name


class Contacts(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)

    class Meta:
        verbose_name_plural = "Contacts"


class Panel(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='panel')
    name = models.CharField(max_length=50)
    designation = models.CharField(max_length=50)
    image = models.ImageField(upload_to="images/panelist/", verbose_name="Panelist image", blank=True, null=True)

    class Meta:
        verbose_name_plural = "Panel"

class EventSponsors(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="event_sponsors")
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Name")
    image = models.ImageField(upload_to="images/sponsors/", null=True, blank=True, verbose_name="Sponser Image (upload rectangular images)")
    website = models.URLField(max_length=1000, null=True, blank=True, verbose_name="Link to Sponsors Website")
    class Meta:
        verbose_name_plural = "Sponsors"
