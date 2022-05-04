#!/usr/bin/env python3
"""
Function that returns all students sorted by average score
"""
import pymongo


def top_students(mongo_collection):
    """
    Function that returns all students sorted by average score
    """
    students = mongo_collection.find()
    for student in students:
        sum = 0
        for topic in student.get('topics', ''):
            sum += topic['score']
        avg = sum / len(student.get('topics', ''))
        name = student.get('name')
        avg_dic = {"averageScore": avg}
        mongo_collection.update_many({"name": name}, {'$set': avg_dic})
    return mongo_collection.find().sort("averageScore", pymongo.DESCENDING)
