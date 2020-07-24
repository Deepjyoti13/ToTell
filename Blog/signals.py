from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


from .models import Writer

def writer_profile(sender, instance, created, **kwargs):
	if created:
		group = Group.objects.get(name='Bloggers')
		instance.groups.add(group)
		Writer.objects.create(
			user=instance,
			username=instance.username,
			email=instance.email,
			)
		print('Profile created!')

post_save.connect(writer_profile, sender=User)