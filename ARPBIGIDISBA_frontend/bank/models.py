from django.db import models

class Sample(models.Model):
    name = models.CharField(max_length=200)
    species = models.CharField(max_length=200, blank=True, null=True)
    clone = models.CharField(max_length=200, blank=True, null=True)
    plasmid = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    frozen_date = models.DateField(blank=True, null=True)
    responsible = models.CharField(max_length=200)
    publication_ref = models.CharField(max_length=200, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    strain = models.CharField(max_length=200, blank=True, null=True)
    rack = models.CharField(max_length=10, blank=True, null=True)
    rack_row = models.CharField(max_length=2, blank=True, null=True)
    rack_col = models.CharField(max_length=2, blank=True, null=True)
    box = models.CharField(max_length=10, blank=True, null=True)
    box_row = models.CharField(max_length=2, blank=True, null=True)
    box_col = models.CharField(max_length=2, blank=True, null=True)
    freezer = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.rack}{self.rack_row}{self.rack_col})"