from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Task(models.Model):
    HOME='Home'
    SCHOOL = 'School'
    WORK= 'Work'
    SI= 'Self-improvement'
    OTHER= 'Other'
    categoryChoices = [
        (HOME,"Home"),
        (SCHOOL, "School"),
        (WORK, "Work"),
        (SI, "Self-Improvement"),
        (OTHER, "Other"),
        ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=400)
    category = models.CharField(
        max_length=20,
        choices = categoryChoices,
        default=OTHER
    )
    completed = models.BooleanField(default=False)

class Budget(models.Model):
    FOOD="Food"
    CLOTHING="Clothing"
    HOUSING="Housing"
    EDUCATION="Education"
    OTHER="Other"
    categoryChoices= [
        (FOOD, "Food"),
        (CLOTHING, "Clothing"),
        (HOUSING, "Housing"),
        (EDUCATION, "Education"),
        (OTHER,"Other"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=400)
    category = models.CharField(
        max_length=20,
        choices=categoryChoices,
        default=OTHER
    )
    projected = models.PositiveIntegerField()
    actual = models.PositiveIntegerField()
    
