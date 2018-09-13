from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
	name = models.CharField(max_length = 300, null = True)
	text = models.CharField(max_length = 3000, null = True)
	image = models.ImageField(upload_to='media/', blank = True)
	author = models.ForeignKey(User, on_delete = models.CASCADE, null = True)
	date = models.DateField(null = True)

	def __str__(self):
		return self.name + ' - ' + str(self.author)
