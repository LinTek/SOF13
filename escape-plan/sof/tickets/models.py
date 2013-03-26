from django.db import models


class TicketType(models.Model):
    name = models.CharField()
    price = models.DecimalField()


class Ticket(models.Model):
    ticket_type = models.ForeignKey()


class Invoice(models.Model):
    tickets = models.ManyToManyField()
