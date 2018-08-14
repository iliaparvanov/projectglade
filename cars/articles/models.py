from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
	name = models.CharField(max_length = 30, null = True)
	text = models.CharField(max_length = 3000, null = True)
	author = models.ForeignKey(User, on_delete = models.CASCADE, null = True)
	date = models.DateField(null = True)

	def __str__(self):
		return self.name + ' - ' + str(self.author)
