from django.db import models
import datetime
from PIL import Image, ExifTags
from io import BytesIO
from django.core.files.base import ContentFile

# Create your models here.
class BeUser(models.Model):
    uname = models.CharField(max_length = 100, blank = False, null = False)
    upickup = models.CharField(max_length = 50)
    ugrade = models.CharField(max_length = 2, blank = True, null = True)
    udate = models.DateField(auto_now_add = True, blank = True)
    uimage = models.ImageField(upload_to = 'images/', blank = True, null = True)
    umail = models.CharField(max_length = 100, blank = False, null = False, unique = True)

class Bookforsale(models.Model):
    buser = models.ForeignKey(BeUser, on_delete = models.CASCADE)
    bimage = models.ImageField(upload_to = 'images/', blank = True, null = True)
    bname = models.CharField(max_length = 50, blank = False, null = False)
    bqual = models.CharField(max_length = 10, blank = False, null = False)
    bgrade = models.CharField(max_length = 5, blank = False, null = False)
    bsubject = models.CharField(max_length = 10, blank = False, null = False)
    bprice = models.DecimalField(max_digits = 5, decimal_places = 2, blank = False, null = False)
    bdescript = models.CharField(max_length = 255, blank = True, null = True)
    bdate = models.DateField(auto_now_add = True, blank = True)

    def save(self, *args, **kwargs):
        pil_image_obj = Image.open(self.bimage)

        if hasattr(pil_image_obj, '_getexif'):
            exif = pil_image_obj._getexif()
            if exif:
                for tag, label in ExifTags.TAGS.items():
                    if label == 'Orientation':
                        orientation = tag
                        break
                if orientation in exif:
                    if exif[orientation] == 3:
                        pil_image_obj = pil_image_obj.rotate(180, expand=True)
                    elif exif[orientation] == 6:
                        pil_image_obj = pil_image_obj.rotate(270, expand=True)
                    elif exif[orientation] == 8:
                        pil_image_obj = pil_image_obj.rotate(90, expand=True)

        (w,h) = pil_image_obj.size
        print (str(w)+","+str(h))
        n_h = int(h*400/w)
        print ("800,"+str(n_h))
        new_image = pil_image_obj.resize((400, n_h))

        new_image_io = BytesIO()
        new_image.save(new_image_io, format='JPEG')

        temp_name = self.bimage.name
        self.bimage.delete(save=False)

        self.bimage.save(
            temp_name,
            content=ContentFile(new_image_io.getvalue()),
            save=False
        )

        super(Bookforsale, self).save(*args, **kwargs)