# encoding: utf-8
from django.db import models

YESNO = [('yes', 'Ja'), ('no', 'Nej')]
YESNO_MAYBE = [('yes', 'Ja'), ('maybe', 'Kanske'), ('no', 'Nej')]
YESNO_NOT_NEEDED = [('yes', 'Ja'), ('maybe', 'Klarar oss utan om det kniper'), ('no', 'Nej')]

ARRIVAL_DAYS = [('thursday', 'Torsdag'), ('friday', 'Fredag')]
PLAY_LENGTHS = [(unicode(i), '%d min' % i) for i in [20, 30, 40]]

TICKET_TYPES = [('thursday', 'Torsdag - Söndag'),
                ('friday', 'Fredag - Söndag')]


def numeric_choice(start, stop):
    """
    Returns choices for all numeric values between start and stop
    """
    return [(unicode(i), '%d st' % i) for i in range(start, stop + 1)]


class Orchestra(models.Model):
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
                                        upload_to='orchestra_images')
    logo_image = models.ImageField("Ladda upp en högupplöst bild på er logga",
                                    upload_to='orchestra_logos')

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

    play_length = models.CharField("Önskad längd på spelningarna, kväll",
                                    choices=PLAY_LENGTHS, max_length=5, blank=True)

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


class Member(models.Model):
    class Meta:
        verbose_name = 'orkestermedlem'
        verbose_name_plural = 'orkestermedlemmar'

    def __unicode__(self):
        return unicode("%s %s" % (self.first_name, self.last_name))

    first_name = models.CharField("förnamn", max_length=30)
    last_name = models.CharField("efternamn", max_length=30)
    ticket_type = models.CharField("biljettyp", max_length=10, choices=TICKET_TYPES)

    plays_kartege = models.CharField("Kommer du att gå/spela/dansa i kårtegen?",
                                     choices=YESNO, max_length=5)
    allergies = models.CharField("Eventuella allergier",
                                 max_length=60, blank=True)
    needs_bed = models.CharField("Önskar sovplats",
                                 choices=YESNO, max_length=5)
    attend_sitting = models.CharField("""Önskar att få möjligheten att gå på sittningen på torsdagen
                                        (om det blir tillräckligt stort intresse så kommer denna sittning att hållas)""",
                                        choices=YESNO, max_length=5)

    t_shirt = models.BooleanField("T-shirt")
    badge_orchestra = models.BooleanField("Orkestermärke")
    badge_visitor = models.BooleanField("Besökarmärke")
    medal = models.BooleanField("Medalj")
    bottle_opener = models.BooleanField("Kapsylöppnare")
    yoyo = models.BooleanField("Jojo (skidliftkortshållare som man kan ha kapsylöppnaren i)")

    orchestra = models.ForeignKey(Orchestra)
