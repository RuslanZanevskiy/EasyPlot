from django.db import models

from django.urls import reverse

from django.contrib.auth.models import User 


class Plot(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE) 
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=4000)
    code = models.TextField()
    likes = models.IntegerField(default=0)
    main_image = models.ImageField(blank=True, null=True, upload_to='plot_images')
    

    def get_absolute_url(self):
        return reverse('plots:detail', kwargs={"pk": self.pk})

    def __str__(self):
        return f'{self.title}'
    
    class Meta:
        ordering = ['likes']
