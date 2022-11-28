#
# Created on Sun Oct 09 2022
#
# The MIT License (MIT)
# Copyright (c) 2022 Rohit Geddam, Arun Kumar, Teja Varma, Kiron Jayesh, Shandler Mason
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software
# and associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial
# portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

from email.policy import default
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from django_countries.fields import CountryField


from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager
from .utils import check_ncsu_email


class CustomUser(AbstractUser):
    """Custom User Model"""

    username = None
    email = models.EmailField("email address", unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        email = self.email

        if not check_ncsu_email(email):
            raise ValueError("Please use NCSU Email Id!")
        super(CustomUser, self).save(*args, **kwargs)

    def __str__(self):
        return self.email


class Profile(models.Model):
    """Model for User Profile"""

    GENDER_MALE = "Male"
    GENDER_FEMALE = "Female"
    GENDER_OTHER = "Other"

    STUDY_CONDITIONS_QUIET = "Calm and quiet"
    STUDY_CONDITIONS_LOUD = "Energetic and excited"

    SLEEP_HABITS_LATE = "Night owl (I prefer to sleep late)"
    SLEEP_HABITS_EARLY = "Early bird (I prefer to sleep early)"

    CLEANLINESS_NEAT = "I tend to be neat"
    CLEANLINESS_MESSY = "I tend to be messy"

    DRUG_ATTITUDES_ALCOHOL = "I drink, but don't smoke"
    DRUG_ATTITUDES_SMOKING = "I smoke, but don't drink"
    DRUG_ATTITUDES_NONE = "I don't drink or smoke"

    DEGREE_BS = "Bachelors"
    DEGREE_MS = "Masters"
    DEGREE_PHD = "Phd"

    BLANK = "--"
    NO_PREF = "No Preference"

    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    )

    STUDY_CONDITIONS_CHOICES = (
        (STUDY_CONDITIONS_QUIET, "Calm and quiet"),
        (STUDY_CONDITIONS_LOUD, "Energetic and excited"),
    )

    SLEEP_HABITS_CHOICES = (
        (SLEEP_HABITS_LATE, "Night owl (I prefer to sleep late)"),
        (SLEEP_HABITS_EARLY, "Early bird (I prefer to sleep early)"),
    )

    CLEANLINESS_CHOICES = (
        (CLEANLINESS_NEAT, "I tend to be neat"),
        (CLEANLINESS_MESSY, "I tend to be messy"),
    )

    DRUG_ATTITUDE_CHOICES = (
        (DRUG_ATTITUDES_ALCOHOL, "I drink, but don't smoke"),
        (DRUG_ATTITUDES_SMOKING, "I smoke, but don't drink"),
        (DRUG_ATTITUDES_NONE, "I don't drink or smoke"),
    )

    DEGREE_CHOICES = (
        (DEGREE_BS, "Bachelors Program (BS)"),
        (DEGREE_MS, "Masters Program (MS)"),
        (DEGREE_PHD, "Doctoral Program (PhD)"),
    )

    PREF_GENDER_CHOICES = (
        (NO_PREF, "No Preference"),
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    )

    PREF_DEGREE_CHOICES = (
        (NO_PREF, "No Preference"),
        (DEGREE_BS, "Bachelors Program (BS)"),
        (DEGREE_MS, "Masters Program (MS)"),
        (DEGREE_PHD, "Doctoral Program (PhD)"),
    )

    PREF_STUDY_CONDITIONS_CHOICES = (
        (STUDY_CONDITIONS_QUIET, "Calm and quiet"),
        (STUDY_CONDITIONS_LOUD, "Energetic and excited"),
    )

    PREF_SLEEP_HABITS_CHOICES = (
        (SLEEP_HABITS_LATE, "Night owl (I prefer to sleep late)"),
        (SLEEP_HABITS_EARLY, "Early bird (I prefer to sleep early)"),
    )

    PREF_CLEANLINESS_CHOICES = (
        (CLEANLINESS_NEAT, "I tend to be neat"),
        (CLEANLINESS_MESSY, "I tend to be messy"),
    )

    PREF_DRUG_ATTITUDE_CHOICES = (
        (DRUG_ATTITUDES_ALCOHOL, "I drink, but don't smoke"),
        (DRUG_ATTITUDES_SMOKING, "I smoke, but don't drink"),
        (DRUG_ATTITUDES_NONE, "I don't drink or smoke"),
    )

    """User Profile Model"""
    name = models.CharField(max_length=100, default="")
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    hometown = models.CharField(max_length=100, default="", blank=True)

    gender = models.CharField(
        max_length=128, choices=GENDER_CHOICES, blank=True
    )
    study_conditions = models.CharField(
        max_length=128, choices=STUDY_CONDITIONS_CHOICES, blank=True
    )
    sleep_habits = models.CharField(
        max_length=128, choices=SLEEP_HABITS_CHOICES, blank=True
    )
    drug_attitude = models.CharField(
        max_length=128, choices=DRUG_ATTITUDE_CHOICES, blank=True
    )
    degree = models.CharField(
        max_length=128, choices=DEGREE_CHOICES, blank=True
    )
    country = CountryField(blank_label="Select Country", blank=True)
    major = models.CharField(
        max_length=128, choices=COURSE_CHOICES, blank=True
    )
    visibility = models.BooleanField(default=True)
    is_profile_complete = models.BooleanField(default=False)
    profile_photo = models.ImageField(
        default="default.png", upload_to="profile_pics"
    )

    # preferences

    preference_gender = models.CharField(
        max_length=128, choices=PREF_GENDER_CHOICES, default=NO_PREF
    )
    preference_study_conditions = models.CharField(
        max_length=128, choices=PREF_STUDY_CONDITIONS_CHOICES, default=NO_PREF
    )
    preference_sleep_habits = models.CharField(
        max_length=128, choices=PREF_SLEEP_HABITS_CHOICES, default=NO_PREF
    )
    preference_cleanliness = models.CharField(
        max_length=128, choices=PREF_CLEANLINESS_CHOICES, default=NO_PREF
    )
    preference_drug_attitude = models.CharField(
        max_length=128, choices=PREF_DRUG_ATTITUDE_CHOICES, default=NO_PREF
    )
    preference_degree = models.CharField(
        max_length=128, choices=PREF_DEGREE_CHOICES, default=NO_PREF
    )
    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email}-profile"


@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    """Create User Profile"""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=get_user_model())
def save_user_profile(sender, instance, **kwargs):
    """Save User Profile"""
    instance.profile.save()
