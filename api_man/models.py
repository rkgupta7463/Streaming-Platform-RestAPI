from django.db import models
from django.utils.text import slugify
from urllib.parse import urljoin
from django.contrib.sites.models import Site

# Create your models here.
class Country(models.Model):
    country_code=models.CharField(max_length=10,unique=True)
    name=models.CharField(max_length=50)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def serializer(self):
        dic={}
        dic['code']=self.country_code
        dic['name']=self.name
        return dic
    
class AvaiablePlatformServiceByCountry(models.Model):
    name=models.CharField(max_length=50)
    slug=models.SlugField()
    platform_home_url=models.URLField()
    platform_themeColorCode=models.CharField(max_length=55)
    streamingOptionTypes=models.JSONField(null=True,blank=True)
    country=models.ForeignKey(Country,on_delete=models.CASCADE,related_name="countries")
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Platform {self.name} is service avaiable on {self.country.name}"
    

    # def save(self, *args, **kwargs):
    #     if not self.slug:  # Only generate slug if it's not already set
    #         self.slug = slugify(self.name)
    #     super().save(*args, **kwargs)

    def detail_serializer(self):
        dic={}
        dic['name']=self.name
        dic['slug']=self.slug
        dic['platform_home_url']=self.platform_home_url
        dic['platform_themeColorCode']=self.platform_themeColorCode
        dic['streamingOptionTypes']=self.streamingOptionTypes
        dic['country']=self.country.serializer()
        dic['imageSets']=[imageset.serializer_imgset() for imageset in self.platforms.all()]
        return dic


def get_full_path(file_url: str, use_https: bool = False):
    """
    Build full file URL using current site domain.

    :param file_url: Relative file path (e.g., '/media/uploads/file.jpg')
    :param use_https: Whether to use HTTPS (default False → HTTP)
    :return: Full absolute URL
    """
    if not file_url:
        return None

    current_site = Site.objects.get_current()
    protocol = "https" if use_https else "http"
    domain = current_site.domain  # e.g., "example.com"

    return urljoin(f"{protocol}://{domain}", file_url)


class PlatformImage(models.Model):
    lightThemeImage=models.ImageField(upload_to="platform/img/lightThemeImage/",null=True,blank=True)
    darkThemeImage=models.ImageField(upload_to="platform/img/darkThemeImage/",null=True,blank=True)
    whiteImage=models.ImageField(upload_to="platform/img/whiteImage/",null=True,blank=True)
    platform=models.ForeignKey(AvaiablePlatformServiceByCountry,on_delete=models.CASCADE,related_name="platforms")
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Platform {self.platform.name} is service avaiable on {self.platform.country.name}"

    def serializer_imgset(self):
        dic={}
        dic['lightThemeImage']=get_full_path(self.lightThemeImage.url) if self.lightThemeImage else None
        dic['darkThemeImage']=get_full_path(self.darkThemeImage.url) if self.darkThemeImage else None
        dic['whiteImage']=get_full_path(self.whiteImage.url) if self.whiteImage else None
        return dic
