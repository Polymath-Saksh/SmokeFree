from django.db import models
from django.conf import settings

class Team(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='teams')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    def get_members(self):
        return self.members.all()
    def get_member_count(self):
        return self.members.count()
    def get_created_at(self):
        return self.created_at.strftime("%Y-%m-%d %H:%M:%S")
    def get_updated_at(self):
        return self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
    def add_member(self, user):
        self.members.add(user)
        self.save()
    def remove_member(self, user):
        self.members.remove(user)
        self.save()
    def is_member(self, user):
        return self.members.filter(id=user.id).exists()
    
# Create your models here.
