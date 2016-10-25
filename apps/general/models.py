from django.db import models


class ActionOnInstance(models.Model):
    ACTION_CHOICES = (
        (1, 'creation'),
        (2, 'editing'),
        (3, 'deletion')
    )

    app_name = models.CharField(max_length=50)
    model_name = models.CharField(max_length=50)
    model_id = models.PositiveIntegerField(null=True)
    instance = models.TextField()
    action = models.PositiveSmallIntegerField(choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '%s %s `%s.%s.%d`' % (
            self.timestamp.isoformat(),
            self.get_action_display(),
            self.app_name,
            self.model_name,
            self.model_id
        )
