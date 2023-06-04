from django.db import models
from django.utils.translation import gettext_lazy as _


class VideoConsultation(models.Model):
    duration = models.DurationField(_('duration'))
    consultation_type = models.CharField(_('consultation type'), max_length=255)
    prescription = models.TextField(_('prescription'))
    follow_up_date = models.DateField(_('follow-up date'), null=True, blank=True)
    diagnosis = models.TextField(_('diagnosis'))
    recommendations = models.TextField(_('recommendations'))

    def __str__(self):
        return f"Video Consultation - {self.pk}"


class ChatInteraction(models.Model):
    video_consultation = models.ForeignKey(VideoConsultation, on_delete=models.CASCADE)
    message = models.TextField(_('message'))
    sent_datetime = models.DateTimeField(_('sent date and time'))
    sender = models.CharField(_('sender'), max_length=255)
    attachments = models.FileField(_('attachments'), upload_to='chat_attachments/', null=True, blank=True)

    def __str__(self):
        return f"Chat Interaction - {self.pk}"


class RemoteMonitoring(models.Model):
    sensor_type = models.CharField(_('sensor type'), max_length=255)
    sensor_reading = models.CharField(_('sensor reading'), max_length=255)
    reading_datetime = models.DateTimeField(_('reading date and time'))
    sensor_location = models.CharField(_('sensor location'), max_length=255)
    alert_threshold = models.CharField(_('alert threshold'), max_length=255)
    alert_message = models.TextField(_('alert message'), null=True, blank=True)

    def __str__(self):
        return f"Remote Monitoring - {self.pk}"
