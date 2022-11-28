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

from base.models import Profile


WEIGHTS = {
    "gender": 0.3,
    "study_conditions": 0.2,
    "sleep_habits": 0.1,
    "cleanliness": 0.15,
    "drug_attitude": 0.2,
    "degree": 0.05,
}


def similarity_score(gender, study_conditions, sleep_habits, cleanliness, drug_attitude, degree):
    """Calculate the similarity score"""
    score = (
        WEIGHTS["gender"] * gender
        + WEIGHTS["study_conditions"] * study_conditions
        + WEIGHTS["sleep_habits"] * sleep_habits
        + WEIGHTS["cleanliness"] * cleanliness
        + WEIGHTS["drug_attitude"] * drug_attitude
        + WEIGHTS["degree"] * degree
    )

    return score


def matchings(current_user):
    """Generate matches using Manhattan Distance Algorithm"""
    user_profile = Profile.objects.get(user=current_user)
    all_profiles = Profile.objects.exclude(user=current_user)

    match_list = []
    matches = []

    for profile in all_profiles:

        gender = (
            1
            if user_profile.preference_gender == profile.gender
            or user_profile.preference_gender == profile.NO_PREF
            else 0
        )
        study_conditions = (
            1
            if user_profile.study_conditions == profile.study_conditions
            or user_profile.preference_study_conditions == profile.NO_PREF
            else 0
        )
        sleep_habits = (
            1
            if user_profile.sleep_habits == profile.sleep_habits
            or user_profile.sleep_habits == profile.NO_PREF
            else 0
        )
        cleanliness = (
            1
            if user_profile.cleanliness == profile.cleanliness
            or user_profile.preference_cleanliness == profile.NO_PREF
            else 0
        )
        drug_attitude = (
            1
            if user_profile.drug_attitude == profile.drug_attitude
            or user_profile.preference_drug_attitude == profile.NO_PREF
            else 0
        )
        degree = (
            1
            if user_profile.preference_degree == profile.degree
            or user_profile.preference_degree == profile.NO_PREF
            else 0
        )

        score = similarity_score(gender, study_conditions, sleep_habits, cleanliness, drug_attitude, degree)

        if score > 0.5:
            match_list.append((profile, score))

    match_list.sort(key=lambda x: x[1], reverse=True)

    for m in match_list:
        matches.append(m[0])

    return matches
