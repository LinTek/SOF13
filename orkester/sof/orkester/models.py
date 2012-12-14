# encoding: utf-8
from django.db import models

YESNO = [(True, 'ja'), (False, 'nej')]
YESNO_MAYBE = [('yes', 'ja'), ('maybe', 'kanske'), ('no', 'nej')]
YESNO_NOT_NEEDED = [('yes', 'ja'), ('maybe', 'klarar oss utan om det kniper'), ('no', 'nej')]

ARRIVAL_DAYS = [('thursday', 'torsdag'), ('friday', 'fredag')]
PLAY_LENGTHS = [(i, '%d min' % i) for i in [20, 30, 40]]


def numeric_choice(start, stop):
    """
    Returns choices for all numeric values between start and stop
    """
    return [(i, '%d st' % i) for i in range(start, stop + 1)]


class Orchestra(models.Model):
    # Orkesterinfo
    name = models.CharField("Orkesterns namn", max_length=50)
    short_name = models.CharField("Förkortning av orkesternamn", max_length=10)
    use_short_name = models.CharField("Är det ok att använda det i spelschemat?",
                                      choices=YESNO, max_length=5)
    sof_count = models.PositiveSmallIntegerField("Hur många gånger har ni deltagit i SOF?")
    look_forward_to = models.TextField("Vad ser ni mest fram emot?")
    music_type = models.TextField("Vilken typ av musik spelar ni helst?")
    best_memory = models.TextField("Bästa orkesterminnet?")
    rituals = models.TextField("Har ni några ritualer inför en konsert?")
    three_words = models.CharField("Beskriv orkestern med tre ord.",
                                   max_length=60)
    showpiece = models.CharField("Vilket är ert paradnummer? (alltså låten ni spelar allra bäst)",
                                 max_length=60)
    best_with_sof = models.TextField("Vad är det bästa med SOF?")
    why_orchestra = models.TextField("Varför borde alla studenter vara med i en orkester?")
    craziest_thing = models.TextField("Vad är det galnaste som hänt på en spelning?")
    determines_repertory = models.TextField("Vem bestämmer hur repertoaren ska se ut?")
    what_do_you_do = models.TextField("""Om 30 minuter ska ni upp på scen,
                        hälften av manskapet ligger fortfarande och sover efter
                        gårdagens bravader, vad gör ni?""")
    uniform_description = models.TextField("Beskriv er uniform!")
    dance = models.CharField("Förekommer spontandans på era spelningar?",
                             choices=YESNO, max_length=5)
    thing_to_bring = models.CharField("Om ni enbart får ta med en sak till SOF, vad skulle ni isåfall ta med?",
                                      max_length=30)
    mottos = models.TextField("Vad har orkestern för motton?")
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
                                    choices=PLAY_LENGTHS, max_length=5)

    concerto_preludium = models.CharField("Vill ni spela under Conserto Preludium på fredagen?",
                                          choices=YESNO, max_length=5)
    concerto_grosso = models.CharField("Vill ni spela under Conserto Grosso på lördagen?",
                                          choices=YESNO, max_length=5)
    family_play = models.CharField("Vill ni spela på den jättemysiga Familjespelningan på söndagen?",
                                          choices=YESNO, max_length=5)

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
                                                   blank=True)

    # Kontaktperson

    primary_contact_name = models.CharField("Namn kontaktperson", max_length=40)
    primary_contact_phone = models.CharField("Telefon kontaktperson", max_length=40)
    primary_contact_email = models.EmailField("E-postadress kontaktperson", max_length=40)

    vice_contact_name = models.CharField("Namn vice kontaktperson", max_length=40)
    vice_contact_phone = models.CharField("Telefon vice kontaktperson", max_length=40)
    vice_contact_email = models.EmailField("E-postadress vice kontaktperson", max_length=40)

    # Övrigt
    message = models.TextField("Meddelande till Crew Orkester")
