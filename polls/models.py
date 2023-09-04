from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text


class student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    city= models.CharField(max_length=50,blank=True,null=True)



class Team(models.Model):
    name = models.CharField(blank=True, null=True, max_length=50)
    email = models.CharField(blank=True, null=True, max_length=200)

    def __str__(self):
        return self.name

class TeamMember(models.Model):   
     team = models.ForeignKey(Team, on_delete=models.CASCADE)  
     member = models.ForeignKey(User, on_delete=models.CASCADE)   
     is_lead = models.BooleanField(default=False)       
    
     def __str__(self):      
          return self.team

class Documents(models.Model):    
     document_name = models.CharField(max_length=100)  # name of the file
     document_type = models.CharField(max_length=10)  # type of the file, only accept pdf, doc, txt
     document_size = models.PositiveIntegerField()
     uploaded_date = models.DateTimeField(auto_now_add=True)  # automatically adds the current date on insert

     def __str__(self):
          return self.document_name