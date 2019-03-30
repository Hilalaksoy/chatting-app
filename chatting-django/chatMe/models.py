from django.db import models
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField

# Create your models here.

# User modeli olusturulmayacak
# User key gerektigi zaman, bu sekilde kullanilabilir
# alan_ismi = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

# profil resimleri icin asagidaki gibi alan kullanilacaktir, Media kullanilmayacak.
# model_image = ImageField(blank=True,null=True,upload_to='thumbnails/[model_adi]')


class Media(models.Model):
	"""Media ögesi ses, resim, video veya herhangi bir dosya olabilir"""
	NOT_DEFINED = 'N'
	AUDIO = 'A'
	IMAGE = 'I'
	VIDEO = 'V'
	MEDIA_TYPE_CHOICES = (
		(NOT_DEFINED, 'Not defined'),
		(AUDIO, 'Audio'),
		(IMAGE, 'Image'),
		(VIDEO, 'Video'),
	)

	name = models.CharField(max_length=64, blank=False, null=False)
	media_type = models.CharField(max_length=1,choices=MEDIA_TYPE_CHOICES,default=NOT_DEFINED)
	file = models.FileField(blank=False,null=False,upload_to='chatMe_media')

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Media element'
