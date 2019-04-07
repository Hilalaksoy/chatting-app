from .models import *
import hashlib
import urllib

def get_chat(sender, receiver):
    messages = list(Message.objects.filter(sender=sender, receiver=receiver))
    messages += list(Message.objects.filter(sender=receiver, receiver=sender))
    messages.sort(key=lambda m: m.date )
    return messages

def get_group_chat(id):
    messages = Group.objects.filter(id=id)[0].message_set.order_by('date').all()
    return messages

def gravatar_url(email, size=50):
	return "https://www.gravatar.com/avatar/%s?%s" % (hashlib.md5(email.lower().encode('utf-8')).hexdigest(), urllib.parse.urlencode({'d':'identicon', 's':str(size)}))
