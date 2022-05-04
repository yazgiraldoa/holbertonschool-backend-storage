#!/usr/bin/env python3
"""
Function that returns the list of
school having a specific topic
"""


def schools_by_topic(mongo_collection, topic):
    """
    Function that returns the list of
    school having a specific topic
    """
    school_by_topic = []
    schools = mongo_collection.find()
    for school in schools:
        if topic in school.get('topics', ''):
            school_by_topic.append(school) 
    return school_by_topic
