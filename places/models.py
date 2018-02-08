from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.template.defaultfilters import slugify


# Create your models here.
class Category(models.Model):
    name = models.CharField(verbose_name='Category', max_length=100, null=False, blank=False)
    icon = models.ImageField(upload_to='media/uploads/category_icons/')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class SubCategory(models.Model):
    name = models.CharField(verbose_name="Subcategory", max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Subcategories"


class City(models.Model):
    name = models.CharField(verbose_name="City Name", max_length=40)
    slug = models.SlugField(blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(City, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Cities'


class Place(models.Model):
    name = models.CharField(verbose_name="Place", max_length=200, null=False, blank=False)
    web_site_link = models.CharField(verbose_name="Web-Site", max_length=200, null=True, default='null')
    address = models.CharField(max_length=500, null=False, blank=False)
    description=models.TextField(blank=True,null=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    lat = models.FloatField(verbose_name="Latitude", default=0)
    lng = models.FloatField(verbose_name="Longitude", default=0)
    slug = models.SlugField(unique=True,blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name+str(self.lat)+str(self.lng))
        super(Place, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Places'

def get_str_interval(time1,time2):
    from datetime import time
    if time1 and time2:
        return time.strftime(time1,'%H:%M')+' - '+time.strftime(time2,'%H:%M');

class Schedule(models.Model):
    place = models.OneToOneField(Place, on_delete=models.CASCADE, primary_key=True)
    # Open_<name of day of week> = the number of minutes from midnight
    # until the opening of the institution
    opens_on_mondays = models.TimeField(blank=True,null=True)
    opens_on_tuesdays = models.TimeField(blank=True,null=True)
    opens_on_wednesdays = models.TimeField(blank=True,null=True)
    opens_on_thursdays = models.TimeField(blank=True,null=True)
    opens_on_fridays = models.TimeField(blank=True,null=True)
    opens_on_saturdays = models.TimeField(blank=True,null=True)
    opens_on_sundays = models.TimeField(blank=True,null=True)
    closes_on_mondays = models.TimeField(blank=True,null=True)
    closes_on_tuesdays = models.TimeField(blank=True,null=True)
    closes_on_wednesdays = models.TimeField(blank=True,null=True)
    closes_on_thursdays = models.TimeField(blank=True,null=True)
    closes_on_fridays = models.TimeField(blank=True,null=True)
    closes_on_saturdays = models.TimeField(blank=True,null=True)
    closes_on_sundays = models.TimeField(blank=True,null=True)

    class Meta:
        verbose_name_plural = 'Schedules'
    def to_list(self):
        return filter(lambda x:x[1] and x[2], [
         ('monday',self.opens_on_mondays,self.closes_on_mondays),
         ('tuesday',self.opens_on_tuesdays,self.closes_on_tuesdays),
        ('wednesday',self.opens_on_wednesdays,self.closes_on_wednesdays),
         ('thursday',self.opens_on_thursdays,self.closes_on_thursdays),
        ('friday',self.opens_on_fridays,self.closes_on_fridays),
        ('saturday',self.opens_on_saturdays,self.closes_on_saturdays),
        ('sunday',self.opens_on_sundays,self.closes_on_sundays),
        ])

    def is_opened(place, now):
        place_schedule = Schedule.objects.get(place=place)
        day_of_week = now.isoweekday()
        if day_of_week == 1:
            today_opens = place_schedule.opens_on_mondays
            today_closes = place_schedule.closes_on_mondays
        elif day_of_week == 2:
            today_opens = place_schedule.opens_on_tuesdays
            today_closes = place_schedule.closes_on_tuesdays
        elif day_of_week == 3:
            today_opens = place_schedule.opens_on_wednesdays
            today_closes = place_schedule.closes_on_wednesdays
        elif day_of_week == 4:
            today_opens = place_schedule.opens_on_thursdays
            today_closes = place_schedule.closes_on_thursdays
        elif day_of_week == 5:
            today_opens = place_schedule.opens_on_fridays
            today_closes = place_schedule.closes_on_fridays
        elif day_of_week == 6:
            today_opens = place_schedule.opens_on_saturdays
            today_closes = place_schedule.closes_on_saturdays
        else:
            today_opens = place_schedule.opens_on_sundays
            today_closes = place_schedule.closes_on_sunday
        return today_opens <= now.time() < today_closes


class PlacePhoneNumber(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    number = PhoneNumberField(blank=True)

    class Meta:
        verbose_name_plural = 'Phone Numbers of Place'
        verbose_name = 'Phone Numbers of Place'


class Feature(models.Model):
    name = models.CharField(max_length=30)
    icon = models.ImageField(upload_to='media/uploads/features_icons/')

    class Meta:
        verbose_name_plural = 'Features'
        verbose_name = 'Feature'


class PlaceFeature(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Place Features'
        verbose_name = 'Place Features'


class PlacePhoto(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    photo = models.ImageField()

    def save(self, *args, **kwargs):
        self.photo.upload_to = 'media/uploads/place-photos/' + self.place.slug
        super(PlacePhoto, self).save(*args, **kwargs)
