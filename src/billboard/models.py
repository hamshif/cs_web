
import os
from django.db import models

from cs_web import settings

#
class Notice_Model(models.Model):
    """

    """

    creator = models.CharField(max_length=40)
    text = models.CharField(max_length=400)
    time_stamp = models.DateTimeField()
    file_path = models.CharField(max_length=250, blank=True, null=True, default=None)

    def __str__(self):

        return ' '.join(['self.pk: ', str(self.pk), ' self.creator: ', self.creator])

    def as_dict(self):

        return {'id': self.pk, 'creator': self.creator, 'text': self.text, 'file_path' : self.file_path}


# class NoticeFollowup_Model(models.Model):
#     """
#
#     """
#
#     slurm_job_id = models.IntegerField(default=-1)
#     status = models.CharField(max_length=40, blank=True)
#     report = models.CharField(max_length=400, blank=True, null=True)
#
#     def __str__(self):
#
#         return ' '.join(['self.pk: ', self.pk, ' self.slurm_job_id: ', self.slurm_job_id])