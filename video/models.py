from django.db import models
from django.utils.translation import gettext_lazy as _


class Video(models.Model):
    video_file = models.FileField(upload_to='videos/')
    subtitles = models.TextField(blank=True, null=True)
    processed_file = models.FileField(upload_to='processed_videos/', blank=True, null=True)
    start_time = models.CharField(max_length=10)
    end_time = models.CharField(max_length=10)    
    
    class Meta:
        db_table = 'video_video'
        verbose_name = _('Video')
        verbose_name_plural = _('Videos')

    def __str__(self):
        return self.video_id

