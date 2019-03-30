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
	media_type = models.CharField(max_length=1,choices=MEDIA_TYPE_CHOICES,default=NOT_DEFINED)
	file = models.FileField(blank=False,null=False,upload_to='chatMe_media')

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Media element'


class Group(models.Model):
	group_name=models.CharField(max_length=64)
	group_date=models.DateTimeField(auto_now=True)
	group_admin=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	group_image=models.ForeignKey(Media,on_delete=models.CASCADE)


class Message(models.Model):
	"""Mesaj türü  tek bir kullanıcıya ,bir grup kullanıcıya veya sunucuya bağlı tüm kullanılara gönderilecek şekilde olabilir."""
	NOT_DEFINED = 'N'
	SINGLE_USER = 'S'
	GROUP_USERS = 'G'
	ALL_SERVER  = 'A'
	MESSAGE_TYPE_CHOICES = (
		(NOT_DEFINED, 'Not defined'),
		(SINGLE_USER, 'Single_User'),
		(GROUP_USERS, 'Group_Users'),
		(ALL_SERVER, 'All_Server'),
	)
	message_sender=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='sent_messages',verbose_name="Mesaj Gönderen")
	message_receiver=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='receiver_messages')
	message_content=models.CharField(max_length=150)
	message_date=models.DateTimeField(auto_now=True)
	message_type=models.CharField(max_length=1,choices=MESSAGE_TYPE_CHOICES,default=NOT_DEFINED)
	message_group=models.ForeignKey(Group,on_delete=models.CASCADE)
	message_status=models.BooleanField(default=False)
	message_media=models.ForeignKey(Media,on_delete=models.CASCADE)


class GroupUser(models.Model):
	groupUser_user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	groupUser_group=models.ForeignKey(Group,on_delete=models.CASCADE)
