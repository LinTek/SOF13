# encoding: utf-8
from django.db import models


class Micro:
    value = 'micro'
    max_count = 10
    description = 'Microbygge - 2500 kr/lag (max %d personer)' % max_count


class Makro:
    value = 'makro'
    max_count = 25
    description = 'Makrobygge - 3000-4000 kr/lag (max %d personer)' % max_count


SIZE_SET = (Micro, Makro)
SIZE_TYPES = dict((c.value, c) for c in SIZE_SET)
SIZE_CHOICES = ((c.value, c.description) for c in SIZE_SET)


class CortegeContribution(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = 'kårtegebidrag'

    def __unicode__(self):
        return unicode(self.name)

    name = models.CharField('Lagnamn', max_length=50)
    contact_name = models.CharField('Namn kontaktperson', max_length=40)
    contact_email = models.EmailField('E-postadress kontaktperson', max_length=40)

    needs_generator = models.BooleanField('Behöver elverk')
    size_type = models.CharField('Typ av bygge', choices=SIZE_CHOICES, max_length=10, default=1)
    materials = models.TextField('Material')
    color = models.TextField('Färg', blank=True)
    other = models.TextField('Övrigt', blank=True)

    idea = models.TextField('Byggidé')
    participant_count = models.PositiveSmallIntegerField('Antal personer som ska deltaga')
    tickets_count = models.PositiveSmallIntegerField('Antal förköpsbiljetter')
