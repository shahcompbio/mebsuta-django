from django.db import models

# Create your models here.


class Cell_Image(models.Model):
    cell_id = models.CharField(max_length=15)
    microscope_image_filename = models.CharField(max_length=100)
    microscope_image_url = models.CharField(max_length=150)
    library_id = models.CharField(max_length=15)
    chip_row = models.IntegerField()
    chip_column = models.IntegerField()
    condition = models.CharField(max_length=5)
    pick_met = models.CharField(max_length=5)
    cellenone_image_filename = models.CharField(max_length=100)
    cellenone_image_url = models.CharField(max_length=175)
    cellenone_background_filename = models.CharField(max_length=100)
    cellenone_background_url = models.CharField(max_length=175)
    X = models.DecimalField(max_digits=10, decimal_places=2)
    Y = models.DecimalField(max_digits=10, decimal_places=2)
    Diameter = models.DecimalField(max_digits=10, decimal_places=2)
    Elongation = models.DecimalField(max_digits=10, decimal_places=2)
    Circularity = models.DecimalField(max_digits=10, decimal_places=2)
    Intensity = models.DecimalField(max_digits=10, decimal_places=2)
    ejection_zone_boundary = models.IntegerField()
    row = models.IntegerField()
    col = models.IntegerField()
    jira_ticket = models.CharField(max_length=10, default = "")
    sample_id = models.CharField(max_length=25, default = "")
    isDebris = models.BooleanField(default= False)
    annotation = models.CharField(max_length=50, default = "")


#https://stackoverflow.com/questions/31920853/aggregate-and-other-annotated-fields-in-django-rest-framework-serializers
class Library(models.Model):
    library_id = models.CharField(max_length=50)
    num_cells = models.IntegerField()
    num_annotated = models.IntegerField()




class Mebsuta_Users(models.Model):
    user_id = models.CharField(max_length=50, default = "", primary_key = True)
    name = models.CharField(max_length=50)

class Annotation(models.Model):
    Cell_Image = models.ForeignKey("Cell_Image",related_name= "rel_annotation", on_delete=models.PROTECT)
    library_id = models.CharField(max_length=500)
    cell_id = models.CharField(max_length=500)
    user = models.ForeignKey("Mebsuta_Users", on_delete=models.PROTECT)
    row = models.IntegerField()
    col = models.IntegerField()
    annotation = models.CharField(max_length=50)


class Debris(models.Model):
    Cell_Image = models.ForeignKey("Cell_Image", related_name="debris", on_delete=models.PROTECT)
    library_id = models.CharField(max_length=15)
    cell_id = models.CharField(max_length=15)
    user = models.ForeignKey("Mebsuta_Users", on_delete=models.PROTECT)
    row = models.IntegerField()
    col = models.IntegerField()
    isDebris = models.BooleanField(default = False)
