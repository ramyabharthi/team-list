from django.db import models

class Notes(models.Model):    
    notes_text = models.TextField()   
    created_date = models.DateTimeField(auto_now_add=True)  # automatically adds the current date on insert          