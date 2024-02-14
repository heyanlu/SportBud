from django.db import models
from django.utils import timezone
import uuid
from users.models import Profile
from django.contrib.auth import get_user_model



class Activity(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    featured_image = models.ImageField(null=True, blank=True, default="default1.png")
    tags = models.ManyToManyField('Tag', blank=True)
    vote_ratio = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    vote_total = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    participants = models.ManyToManyField(Profile, blank=True, related_name='events')
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    scheduled_date = models.DateTimeField()
    registration_deadline = models.DateTimeField(null=True) 
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    def __str__(self):
        return self.title 
    
    class Meta:
        ordering = ['-vote_ratio', '-vote_total']
        
    @property
    def reviewers(self):
        queryset = self.review_set.all().value_list('owner__id', flat=True)
        return queryset 
        
    @property   
    def getVoteCount(self):
        reviews = self.review_set.all()
        upVotes = reviews.filter(value='up').count()
        totalVotes = reviews.count()
        
        ratio = (upVotes / totalVotes) * 100
        self.vote_total = totalVotes 
        self.vote_ratio = ratio 
        self.save()
        
        return ratio
    
    
class Submission(models.Model):
    participant = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name="submissions")
    activity = models.ForeignKey(Activity, on_delete=models.SET_NULL, null=True)
    details = models.TextField(null=True, blank=False)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return str(self.event) + ' --- ' + str(self.participant)
     

class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
      
    # class Meta:
    #     unique_together = [['owner', 'activity']]
        
    def __str__(self):
        return self.value 


class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.name