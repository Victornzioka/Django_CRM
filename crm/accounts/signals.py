from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group

from .models import Customer

#this is a function that sends a signal to automatically create a profile after each user is created in the database
def customer_profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='customer')
        instance.groups.add(group)

        Customer.objects.create(
            user=instance,
            Name=instance.username,
        )
        print("Profile created!")

post_save.connect(customer_profile, sender=User)
