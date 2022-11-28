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
from django.test import TestCase
from base.models import Profile
from django.contrib.auth import get_user_model


class TestModels(TestCase):
    def test_user_profile_model(self):
        user = get_user_model().objects.create_user(
            "admin@ncsu.edu", "password"
        )
        profile = Profile.objects.get(user=user)
        profile.name = "Heidi"
        profile.bio = "Cooler than cool, or ice cold"
        profile.birth_date = "2000-11-15"
        profile.hometown = "Ontario"
        profile.gender = "Female"
        profile.study_conditions = "Calm and quiet"
        profile.sleep_habits = "Night owl (I prefer to sleep late)"
        profile.cleanliness = "I tend to be messy"
        profile.drug_attitude = "I drink, but don't smoke"
        profile.degree = "Masters Program (MS)"
        profile.country = "Canada"
        profile.visibility = "True"
        profile.preference_gender = "Female"
        profile.preference_country = "Jordan"
        profile.preference_degree = "Masters Program (MS)"
        profile.preference_study_conditions = "Calm and quiet"
        profile.preference_sleep_habits = "Night owl (I prefer to sleep late)"
        profile.preference_cleanliness = "I tend to be neat"
        profile.preference_drug_attitude = "I drink, but don't smoke"
        profile.preference_course = "Computer Science"
        profile.is_profile_complete = "True"
        profile.save()
        self.assertEqual(user.email, "admin@ncsu.edu")
        self.assertEqual(profile.name, "Heidi")
        self.assertEqual(profile.bio, "Cooler than cool, or ice cold")
        self.assertEqual(profile.birth_date, "2000-11-15")
        self.assertEqual(profile.hometown, "Ontario")
        self.assertEqual(profile.gender, "Female")
        self.assertEqual(profile.degree, "Masters Program (MS)")
        self.assertEqual(profile.study_conditions, "Calm and quiet")
        self.assertEqual(profile.sleep_habits, "Night owl (I prefer to sleep late)")
        self.assertEqual(profile.drug_attitude, "I drink, but don't smoke")
        self.assertEqual(profile.country, "Canada")
        self.assertEqual(profile.visibility, "True")
        self.assertEqual(profile.preference_gender, "Female")
        self.assertEqual(profile.preference_country, "Jordan")
        self.assertEqual(profile.preference_degree, "Masters Program (MS)")
        self.assertEqual(profile.preference_course, "Computer Science")
        self.assertEqual(profile.preference_study_conditions, "Calm and quiet")
        self.assertEqual(profile.preference_sleep_habits, "Night owl (I prefer to sleep late)")
        self.assertEqual(profile.preference_cleanliness, "I tend to be neat")
        self.assertEqual(profile.preference_drug_attitude, "I drink, but don't smoke")
        self.assertEqual(profile.is_profile_complete, "True")
