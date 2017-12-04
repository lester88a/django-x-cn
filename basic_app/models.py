from django.db import models
from django.core.urlresolvers import reverse
#from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
# class School(models.Model):
#     name = models.CharField(max_length=256)
#     principal = models.CharField(max_length=256)
#     location = models.CharField(max_length=256)
#     #slug = models.SlugField(max_length=100, unique=True)
#
#     def __str__(self):
#         return self.name
#
#     # def slug(self):
#     #     return slugify(self.name)
#
#     def get_absolute_url(self):
#         #return reverse('detail',kwargs={'slug':self.slug,'pk':self.pk,'id':self.id})
#         return reverse('detail',kwargs={'pk':self.pk})
#
# class Student(models.Model):
#     name = models.CharField(max_length=256)
#     age = models.PositiveSmallIntegerField()
#     School = models.ForeignKey(School,related_name='students')
#
#     def __str__(self):
#         return self.name

class Genre (models.Model):
    name = models.CharField(max_length=128,unique=True)
    #movies = models.ManyToManyField(Movie,related_name='movies')

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('detail',kwargs={'pk':self.pk})

class Movie (models.Model):
    title = models.CharField(max_length=128,unique=True)
    year = models.PositiveSmallIntegerField()
    runtime = models.PositiveSmallIntegerField()
    country = models.CharField(max_length=128)
    language = models.CharField(max_length=128)
    imgurl = models.URLField(verbose_name='Image URL')
    downloadurl = models.CharField(max_length=256,verbose_name='Download URL')
    genres = models.ManyToManyField(Genre,related_name='movies')
    #genre = models.ForeignKey(Genre,related_name='genres')
    date = models.DateField()
    rate = models.FloatField(max_length=4)
    desc = models.CharField(max_length=256,verbose_name='Description',)
    dateadded = models.DateField(default=timezone.now,verbose_name='Date Added')

    def __str__(self):
        return str(self.title + ' ' + str(self.year))

    def get_absolute_url(self):
        return reverse('detail',kwargs={'pk':self.pk})


class UserProfileInfo(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    user = models.OneToOneField(User)

    #additional field
    firstname = models.CharField(max_length=128,verbose_name='First Name',blank=True)
    lastname = models.CharField(max_length=128,verbose_name='Last Name',blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    birthday = models.DateField(verbose_name='Birthday')
    city = models.CharField(max_length=128,verbose_name='City',blank=True)
    province = models.CharField(max_length=128,verbose_name='Province',blank=True)
    country = models.CharField(max_length=128,verbose_name='County',blank=True)
    profile_pic = models.ImageField(upload_to='static/images',verbose_name='Profile Picture',blank=True)
    wechat = models.CharField(max_length=128,unique=True,verbose_name='WeChat',blank=True)
    qq = models.IntegerField(unique=True,verbose_name='QQ',blank=True)
    mobile = models.CharField(max_length=15,unique=True,blank=True)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('profile',kwargs={'pk':self.pk})

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

    post_save.connect(create_user_profile, sender=User)
