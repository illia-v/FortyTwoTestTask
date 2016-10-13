from django.db import models


class Request(models.Model):
    url = models.URLField()
    timestamp = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=20)

    def __unicode__(self):
        return u'%s %s %s' % (self.timestamp.isoformat(),
                              self.method, self.url)
