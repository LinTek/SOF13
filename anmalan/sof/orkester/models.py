# encoding: utf-8
"""
models.py

This file declares models for the orchestra-app. These models are later used
in the system when creating objects or generating forms for them.

If you add or remove fields from a model, forms and such will probably
update automatically. However, you will probably need to generate a new
database migration since the database structure are generated using this file.
"""
import os

from django.db import models
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify

from sof.conf.settings_orchestra import DEFAULT_FROM_EMAIL

## Constants for choices. The first in each tuple is the DB-value, the second
## is the display_name used in forms (and django admin and stuff).

# These are used for some questions. Using choices instead of BooleanFields
# for yes/no questions to be consistent with yes/no/maybe-questions.
YES = 'yes'
NO = 'no'

YESNO = [(YES, 'Ja'), (NO, 'Nej')]
YESNO_MAYBE = [(YES, 'Ja'), ('maybe', 'Kanske'), (NO, 'Nej')]
YESNO_NOT_NEEDED = [(YES, 'Ja'), ('maybe', 'Klarar oss utan om det kniper'), (NO, 'Nej')]

# Days and ticket types
ARRIVAL_DAYS = [('thursday', 'Torsdag'), ('friday', 'Fredag')]

TICKET_TYPES = [('thursday', 'Torsdag - Söndag (625 kr)'),
                ('friday',   'Fredag - Söndag (575 kr)')]

# Each choice must be a two-tuple. In this case we want the same value in
# DB as in the forms, so generate tuples for all items in the list
TSHIRT_SIZES = [(s, s) for s in ('XS', 'S', 'M', 'L', 'XL', 'XXL', '3XL', '4XL')]


def boolify(value):
    if value == YES:
        return True
    if value == NO:
        return False
    return None


def _get_filename(orchestra, filename):
    """
    Helper-function for generating a filename without non-ascii chars.
    The resulting filename will be an all-ASCII version of the orchestra
    name with the same file extension as in the original file.
    """
    return "%s.%s" % (slugify(orchestra.orchestra_name), filename.split('.')[-1])


def image_filename(orchestra, filename):
    """
    Generates a directory/filename for an uploaded orchestra image.
    """
    return "orchestra_images/%s" % _get_filename(orchestra, filename)


def logo_filename(orchestra, filename):
    """
    Generates a directory/filename for an uploaded orchestra logo.
    """
    return "orchestra_logos/%s" % _get_filename(orchestra, filename)


def numeric_choice(start, stop):
    """
    Returns choices for all numeric values between start and stop
    i.e. [('1', '1 st'), ('2', '2 st')] if start = 1 and stop = 2
    """
    return [(unicode(i), '%d st' % i) for i in range(start, stop + 1)]


def _mail(template_name, to, template_params):
    """
    Helper-function used by send_confirm_email()-methods below.

    Sends a mail with content from template_name, to all recipients in
    a list. Uses template_params to render the content-templates.
    """
    send_mail(subject=render_to_string('orkester/mail/%s_subject.txt' % template_name,
                                       template_params).replace('\n', ''),
              message=render_to_string('orkester/mail/%s.txt' % template_name,
                                       template_params),
              from_email=DEFAULT_FROM_EMAIL, recipient_list=to)


class Orchestra(models.Model):
    """
    An Orchestra describes an visiting Orchestra, including an insane amount
    of fields for unclear purposes specified by orkesteransvarig.
    """

    class Meta:
        verbose_name = 'orkester'
        verbose_name_plural = 'orkestrar'

    def __unicode__(self):
        return unicode(self.orchestra_name)

    # Orkesterinfo
    orchestra_name = models.CharField("Orkesterns namn", max_length=50)
    short_name = models.CharField("Förkortning av orkesternamn", max_length=10)
    use_short_name = models.CharField("Är det ok att använda förkortningen i spelschemat?",
                                      choices=YESNO, max_length=5)
    sof_count = models.PositiveSmallIntegerField("Hur många gånger har ni deltagit i SOF?")
    look_forward_to = models.TextField("Vad ser ni mest fram emot?", blank=True)
    music_type = models.TextField("Vilken typ av musik spelar ni helst?")
    best_memory = models.TextField("Bästa orkesterminnet?")
    rituals = models.TextField("Har ni några ritualer inför en konsert?")
    three_words = models.CharField("Beskriv orkestern med tre ord.",
                                   max_length=60)
    showpiece = models.CharField("Vilket är ert paradnummer? (alltså låten ni spelar allra bäst)",
                                 max_length=60, blank=True)
    best_with_sof = models.TextField("Vad är det bästa med SOF?")
    why_orchestra = models.TextField("Varför borde alla studenter vara med i en orkester?", blank=True)
    craziest_thing = models.TextField("Vad är det galnaste som hänt på en spelning?")
    determines_repertory = models.TextField("Vem bestämmer hur repertoaren ska se ut?", blank=True)
    what_do_you_do = models.TextField("""Om 30 minuter ska ni upp på scen,
                        hälften av manskapet ligger fortfarande och sover efter
                        gårdagens bravader, vad gör ni?""", blank=True)
    uniform_description = models.TextField("Beskriv er uniform!")
    dance = models.TextField("Spontandans på era spelningar, ja eller nej?", blank=True)
    thing_to_bring = models.CharField("Om ni enbart får ta med en sak till SOF, vad skulle ni isåfall ta med?",
                                      max_length=30, blank=True)
    mottos = models.TextField("Vad har orkestern för motton?", blank=True)
    orchestra_image = models.ImageField("Ladda upp en högupplöst bild på er orkester",
                                        upload_to=image_filename)
    logo_image = models.ImageField("Ladda upp en högupplöst bild på er logga",
                                    upload_to=logo_filename)

    # Under SOF
    departure_day = models.CharField("Ankomstdag", choices=ARRIVAL_DAYS,
                                     max_length=15)

    parking_lot_needed = models.CharField("Behöver ni parkeringsplats?",
                                          choices=YESNO, max_length=5)
    parking_lot_type = models.TextField("Om så är fallet, hur många och vilken typ av fordon?",
                                         blank=True)

    estimated_instruments = models.CharField("Uppskattat antal pallar instrument",
                                             choices=numeric_choice(0, 3), max_length=5)

    # Spelningar
    play_thursday = models.CharField("Har möjlighet att spela på torsdagen?",
                                     choices=YESNO_MAYBE, max_length=5)
    play_friday = models.CharField("Antal önskade spelningar, fre (räknat utan Conserto Preludium)",
                                     choices=numeric_choice(1, 2), max_length=5)

    concerto_preludium = models.CharField("Vill ni spela under Conserto Preludium på fredagen?",
                                          choices=YESNO, max_length=5)
    concerto_grosso = models.CharField("Vill ni spela under Conserto Grosso på lördagen?",
                                          choices=YESNO, max_length=5)
    family_play = models.CharField("Vill ni spela på den jättemysiga Familjespelningan på söndagen?",
                                          choices=YESNO, max_length=5)

    # Extra utrustning
    backline = models.TextField("Har ni några speciella behov gällande backline?", blank=True)
    amplifier_guitar = models.CharField("Behöver ni gitarrförstärkare?",
                                        choices=YESNO_NOT_NEEDED, max_length=5)
    amplifier_bass = models.CharField("Behöver ni basförstärkare?",
                                        choices=YESNO_NOT_NEEDED, max_length=5)
    uses_drumset = models.CharField("Använder trumset? (ALLA måste ta med EGNA cymbaler!)",
                                          choices=YESNO, max_length=5)
    will_bring_drumset = models.CharField("Kommer ni att ta med er eget trumset?",
                                          choices=YESNO, max_length=5)

    uses_piano = models.CharField("Använder ni piano?",
                                  choices=YESNO_NOT_NEEDED, max_length=5)

    microphones = models.PositiveSmallIntegerField("Ungefärligt antal mikrofoner som behövs (om några)",
                                                   blank=True, null=True)

    # Kontaktperson
    primary_contact_name = models.CharField("Namn kontaktperson", max_length=40)
    primary_contact_phone = models.CharField("Telefon kontaktperson", max_length=40)
    primary_contact_email = models.EmailField("E-postadress kontaktperson", max_length=40)

    vice_contact_name = models.CharField("Namn vice kontakt", max_length=40)
    vice_contact_phone = models.CharField("Telefon vice kontakt", max_length=40)
    vice_contact_email = models.EmailField("E-postadress vice kontakt", max_length=40)

    # Balett
    ballet_name = models.CharField("Namn på eventuell tillhörande balett?", max_length=50, blank=True)
    ballet_contact_name = models.CharField("Namn kontakt balett", max_length=40, blank=True)
    ballet_contact_phone = models.CharField("Telefon kontakt balett", max_length=40, blank=True)
    ballet_contact_email = models.EmailField("E-postadress kontakt balett", max_length=40, blank=True)

    # Övrigt
    message = models.TextField("Meddelande till Crew Orkester", blank=True)

    token = models.CharField(max_length=60)

    def send_confirm_email(self):
        _mail('confirm_orchestra',
              [self.primary_contact_email],
              {'orchestra': self})

    def generate_token(self):
        self.token = os.urandom(10).encode('hex')


class Member(models.Model):
    """
    A Member is a member of one or many Orchestras.
    """
    class Meta:
        verbose_name = 'orkestermedlem'
        verbose_name_plural = 'orkestermedlemmar'

    def __unicode__(self):
        return unicode("%s %s" % (self.first_name, self.last_name))

    first_name = models.CharField("förnamn", max_length=30)
    last_name = models.CharField("efternamn", max_length=30)
    pid = models.CharField("personnummer", max_length=20, unique=True)
    email = models.EmailField("e-postadress")

    ticket_type = models.CharField("biljettyp", max_length=10, choices=TICKET_TYPES)

    attends_10th_year = models.BooleanField("Detta blir det 10:e året i rad jag besöker SOF/STORK")
    attends_25th_time = models.BooleanField("Detta blir mitt 25:e besök på SOF/STORK")

    plays_kartege = models.CharField("Kommer du att gå/spela/dansa i kårtegen?",
                                     choices=YESNO, max_length=5)
    allergies = models.CharField("Eventuella allergier",
                                 max_length=60, blank=True)
    needs_bed = models.CharField("Önskar sovplats",
                                 choices=YESNO, max_length=5)
    attend_sitting = models.CharField("""Önskar att få möjligheten att gå på sittningen på torsdagen (pris 125 kr)
                                        (om det blir tillräckligt stort intresse så kommer denna sittning att hållas)""",
                                        choices=YESNO, max_length=5)

    t_shirt = models.BooleanField("T-shirt (100 kr)")
    t_shirt_size = models.CharField("Storlek T-shirt",
                                    choices=TSHIRT_SIZES, max_length=5,
                                    blank=True)
    badge_orchestra = models.BooleanField("Orkestermärke (20 kr)")
    badge_visitor = models.BooleanField("Besökarmärke (20 kr)")
    medal = models.BooleanField("Medalj (25 kr)")
    bottle_opener = models.BooleanField("Kapsylöppnare (30 kr)")
    yoyo = models.BooleanField("Jojo (20 kr) (skidliftkortshållare som man kan ha kapsylöppnaren i)")
    beer_glass = models.BooleanField("Ölglas (50 kr)")

    orchestras = models.ManyToManyField(Orchestra)

    def send_confirm_email(self, orchestra):
        _mail('confirm_member',
              [self.email],
              {'member': self, 'orchestra': orchestra})

    def get_gadgets_display(self):
        GADGETS = [('t_shirt', 'T-shirt'),
                   ('badge_orchestra', 'Orkestermärke'),
                   ('badge_visitor', 'Besökarmärke'),
                   ('medal', 'Medalj'),
                   ('bottle_opener', 'Kapsylöppnare'),
                   ('yoyo', 'Jojo'),
                   ('beer_glass', 'Ölglas')]
        return ', '.join([name for attr, name in GADGETS if getattr(self, attr)])

    def get_attends_display(self):
        result = []
        if self.attends_10th_year:
            result.append('10:e året')
        if self.attends_25th_time:
            result.append('25:e året')
        return ', '.join(result)
