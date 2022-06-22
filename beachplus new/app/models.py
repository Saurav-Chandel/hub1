from django.db import models
from django.contrib.auth.models import User 
import django
from django.utils.timezone import now
# Create your models here.

device_category_choices=(
    ('ios','ios'),
    ('Android','Android')
)
hostmatch_selectmode_catchoice=(
    ('public','public'),
    ('private','private')
)
hostmatch_status_catchoice=(
    ('Initiated','Initiated'),
    ('Completed','Completed'),
    ('Cancel','cancel')
)
hostinvitation_status_catchoice=(
    ('Sent','Sent'),
    ('Decline','Decline'),
    ('Attend','Attend')
)
TOKEN_TYPE_CHOICES = (
    ("verification", "Email Verification"),
    ("pwd_reset", "Password Reset"),
)


class Device(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    device_token=models.CharField(max_length=250,unique=True)
    device_type=models.CharField(max_length=250,choices=device_category_choices)
    date_added=models.DateTimeField(default=django.utils.timezone.now)

    def __str__(self):
        return self.user.first_name


class Profile(models.Model):
    user_id=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True,related_name='user01')
    profile_image=models.ImageField(upload_to='profile',blank=True,null=True)
    first_name=models.CharField(max_length=100,null=True,blank=True)
    last_name=models.CharField(max_length=100,null=True,blank=True)
    city=models.CharField(max_length=100,null=True,blank=True)
    state=models.CharField(max_length=100,null=True,blank=True)
    zip=models.CharField(max_length=100,null=True,blank=True)
    cpf_number=models.CharField(max_length=100,null=True,blank=True)
    location=models.CharField(max_length=250,null=True,blank=True)
    matchhost=models.IntegerField(blank=True,null=True,default=0)
    matchplayed=models.IntegerField(blank=True,null=True,default=0)
    matchwon=models.IntegerField(blank=True,null=True,default=0)
    date_added=models.DateTimeField(default=django.utils.timezone.now)

    def __str__(self):
        return self.first_name

class HostMatch(models.Model):
    user_id=models.ForeignKey(Profile,on_delete=models.CASCADE)
    title=models.CharField(max_length=100,blank=True,null=True)
    date=models.DateField()
    time=models.TimeField()
    location=models.CharField(max_length=200,null=True,blank=True)        
    select_mode=models.CharField(max_length=100,blank=True,null=True,choices=hostmatch_selectmode_catchoice)
    status=models.CharField(max_length=200,blank=True,null=True,choices=hostmatch_status_catchoice)
    date_added=models.DateTimeField(default=django.utils.timezone.now)

    def __str__(self):
        return self.user_id.first_name


class HostInvitation(models.Model):
    hostmatch_id=models.ForeignKey(HostMatch,on_delete=models.CASCADE,related_name='hostmatch')
    user_invited=models.ForeignKey(Profile,on_delete=models.CASCADE,null=True,blank=True,related_name='profile')
    status=models.CharField(max_length=200,choices=hostinvitation_status_catchoice,null=True,blank=True)
    date_added=models.DateTimeField(default=django.utils.timezone.now)

    
class TeamPlayers(models.Model):
    host_match=models.ForeignKey(HostMatch,on_delete=models.CASCADE)
    player=models.ForeignKey(Profile,on_delete=models.CASCADE)
    date_added=models.DateTimeField(default=django.utils.timezone.now)

class Team2Players(models.Model):
    host_match=models.ForeignKey(HostMatch,on_delete=models.CASCADE)
    player=models.ForeignKey(Profile,on_delete=models.CASCADE)
    date_added=models.DateTimeField(default=django.utils.timezone.now)


class TeamScore(models.Model):
    host_match=models.ForeignKey(HostMatch,on_delete=models.CASCADE,related_name='host_score')
    round=models.IntegerField()
    team1_player_score=models.IntegerField()
    team2_player_score=models.IntegerField()
    date_added=models.DateTimeField(default=django.utils.timezone.now)

class PlayersRating(models.Model):
    host_match=models.ForeignKey(HostMatch,on_delete=models.CASCADE)
    player=models.ForeignKey(Profile,on_delete=models.CASCADE)
    rating=models.IntegerField(blank=True,null=True)
    date_added=models.DateTimeField(default=django.utils.timezone.now)

class ContactUs(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    first_name=models.CharField(max_length=100,null=True,blank=True)
    subject=models.CharField(max_length=100,null=True,blank=True)
    message=models.CharField(max_length=100,null=True,blank=True)
    email_address=models.EmailField(max_length=254)

    def __str__(self):
        return self.first_name

class AboutUs(models.Model):
    about=models.CharField(max_length=100,blank=True,null=True)
    date_added=models.DateTimeField(default=django.utils.timezone.now)  

    def __str__(self):
        return self.about     

    class Meta:
        ordering = ('-id',)

class PrivacyPolicy(models.Model):
    policy=models.CharField(max_length=100,blank=True,null=True)
    date_added=models.DateTimeField(default=django.utils.timezone.now)  

    def __str__(self):
        return self.policy 

class TermsCondition(models.Model):
    terms=models.CharField(max_length=100,blank=True,null=True)
    date_added=models.DateTimeField(default=django.utils.timezone.now)  

    def __str__(self):
        return self.terms 



class Token(models.Model):
    
    token = models.CharField(max_length=300)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    token_type = models.CharField(
        max_length=20, choices=TOKEN_TYPE_CHOICES
    )
    created_on = models.DateTimeField(default=now, null=True, blank=True)
    expired_on = models.DateTimeField(default=now, null=True, blank=True)