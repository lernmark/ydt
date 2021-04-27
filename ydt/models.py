from django.db import models

class Todo(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(default=None, blank=True, null=True, max_length=100)
    author = models.CharField(default=None, blank=True, null=True, max_length=100)
    responsible = models.CharField(default=None, blank=True, null=True, max_length=100)
    created_at = models.DateTimeField('Created', auto_now_add=True)
    update_at = models.DateTimeField('Updated', auto_now=True)
    isCompleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title
