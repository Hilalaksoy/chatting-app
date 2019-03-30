from django.db import models
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField
from django.conf import settings

# Create your models here.

# User modeli olusturulmayacak
# User key gerektigi zaman, bu sekilde kullanilabilir
# alan_ismi = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

# profil resimleri icin asagidaki gibi alan kullanilacaktir, Media kullanilmayacak.
# model_image = ImageField(blank=True,null=True,upload_to='thumbnails/[model_adi]')


class Media(models.Model):
	"""Media ögesi ses, resim, video veya herhangi bir dosya olabilir."""
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
	media_type = models.CharField(max_length=1, choices=MEDIA_TYPE_CHOICES, default=NOT_DEFINED)
	file = models.FileField(blank=False, null=False, upload_to='chatMe_media')

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Media element'


class UserProfileImage(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile_image', on_delete=models.CASCADE)
	image = ImageField(blank=True, null=True, upload_to='thumbnails/users')

class Group(models.Model):
	name = models.CharField(max_length=64)
	create_date = models.DateTimeField(auto_now=True)
	admin = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='managed_groups', on_delete=models.CASCADE)
	image = ImageField(blank=True, null=True, upload_to='thumbnails/groups')
	users = models.ManyToManyField(settings.AUTH_USER_MODEL)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Chat group'


class Message(models.Model):
	"""Mesaj türü  tek bir kullanıcıya ,bir grup kullanıcıya veya sunucuya bağlı tüm kullanılara gönderilecek şekilde olabilir."""
	NOT_DEFINED = 'N'
	SINGLE_USER = 'S'
	GROUP_CONVERSATION = 'G'
	ALL_USERS  = 'A'
	MESSAGE_DESTINATION_CHOICES = (
		(NOT_DEFINED, 'not_defined'),
		(SINGLE_USER, 'Single user'),
		(GROUP_CONVERSATION, 'Group'),
		(ALL_USERS, 'All users'),
	)

	sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
	receiver = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE, related_name='receiver_messages')
	group = models.ForeignKey(Group, null=True, on_delete=models.CASCADE)
	type = models.CharField(max_length=1, choices=MESSAGE_DESTINATION_CHOICES, default=NOT_DEFINED)
	content = models.CharField(max_length=512)
	date = models.DateTimeField(auto_now=True)
	media = models.ForeignKey(Media, null=True, on_delete=models.CASCADE)
	has_been_read = models.BooleanField(default=False)
