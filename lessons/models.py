from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=200)
    preview = models.ImageField(upload_to='previews/')
    description = models.TextField()

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    preview = models.ImageField(upload_to='lesson_previews/')
    video_link = models.URLField()

    def __str__(self):
        return self.title
