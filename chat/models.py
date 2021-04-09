

from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Message(models.Model):

    author = models.ForeignKey(User, related_name="author_messages", on_delete=models.CASCADE)
    area=models.CharField(max_length=100,null=True)

    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username

    def last_30_messages(area):

        return Message.objects.filter(area=area).order_by('timestamp').all()[:30]
