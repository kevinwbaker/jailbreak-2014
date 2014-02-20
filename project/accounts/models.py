from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):

    user = models.OneToOneField(User, related_name='profile')

    profile_completed = models.BooleanField(default=False)

    @property
    def has_team(self):
        return self.team is not None

    def __unicode__(self):
        return 'Profile for %s' % self.user.email


def user_post_save_callback(sender, instance, created, *args, **kwargs):
    ''' Creates a UserProfile object whenever a user object is created. '''
    if created:
        UserProfile.objects.create(user=instance)
models.signals.post_save.connect(user_post_save_callback, sender=User, dispatch_uid='accounts.models')
