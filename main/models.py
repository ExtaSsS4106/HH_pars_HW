from django.db import models

class Specialisation(models.Model):
    title = models.CharField(max_length=200)
    
    def __str__(self):
        return self.title
    
    
class Groups(models.Model):
    title = models.CharField(max_length=200)
    spec_id = models.ForeignKey(Specialisation, on_delete=models.CASCADE)   
    
    def __str__(self):
        return self.title


# Create your models here.
class Vacancies(models.Model):
    title = models.CharField(max_length=200)
    link = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    salary = models.CharField(max_length=100)
    work_schedule = models.CharField(max_length=100)
    publicationTime = models.IntegerField()
    company = models.CharField(max_length=200)
    vacancyId = models.IntegerField(unique=True)
    dataGet = models.DateTimeField(auto_now_add=True)
    dataUpdate = models.DateTimeField(auto_now=True)
    group_id = models.ForeignKey(Groups, on_delete=models.CASCADE, null=True, blank=True)
    spec_id = models.ForeignKey(Specialisation, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, default='active')
    def __str__(self):
        return self.title