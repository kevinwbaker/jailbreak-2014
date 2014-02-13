from django.db import models

class Team(models.Model):
    '''Team taking part'''

    TCD = 'tcd'
    NUIG = 'nuig'
    UCC = 'ucc'
    UCD = 'ucd'
    UNIVERSITIES = (
        (TCD, 'TCD'),
        (NUIG, 'NUIG'),
        (UCC, 'ucc'),
        (UCD, 'ucd'),
    )
    
    slug = models.SlugField()
    name = models.CharField(max_length=128)
    photo = models.FileField(upload_to='teams')
    sponsor_link = models.URLField()
    description = models.TextField()
    source = models.CharField(max_length=4, choices=UNIVERSITIES)

    long_position = models.DecimalField(max_digits=8, decimal_places=3)
    lat_position = models.DecimalField(max_digits=8, decimal_places=3)

    def __unicode__(self):
        return self.name
