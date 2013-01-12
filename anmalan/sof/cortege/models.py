# encoding: utf-8
from django.db import models

SIZE_TYPES = (('micro', 'Microbygge'), ('makro', 'Makrobygge'))


class CortegeContribution(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = 'kårtegebidrag'

    def __unicode__(self):
        return unicode(self.name)

    name = models.CharField('Lagnamn', max_length=50)
    contact_name = models.CharField('Namn kontaktperson', max_length=40)
    contact_email = models.EmailField('E-postadress kontaktperson', max_length=40)

    needs_generator = models.BooleanField('Behöver elverk')
    size_type = models.CharField('Typ av bygge', choices=SIZE_TYPES, max_length=10, default=1)
    materials = models.TextField('Material')
    color = models.TextField('Färg', blank=True)
    other = models.TextField('Övrigt', blank=True)

    idea = models.TextField('Byggidé')
    participant_count = models.PositiveSmallIntegerField('Antal personer som ska deltaga')
    tickets_count = models.PositiveSmallIntegerField('Antal biljetter')
