# -*- coding: utf-8 -*-

from django.db import models
from index.models import Class,Student
import xlrd
import re

# Create your models here.
#
def retreive_to_db(file_name):
    for sheet in structure_data(file_name):
        structure_class(sheet)


def structure_data(file_name):
    book = xlrd.open_workbook(file_name)
    return [book.sheet_by_index(i) for i in range(3)]

def structure_class(sheet):
    root = []
    start_column = []
    class_end = []
    students = []

    # Read Class number and name
    regular_matcher = re.compile(u'([一二三])年(\d+)班')
    current_row = sheet.row(1)
    tmp_row = sheet.row(0)
    for i in range( len(current_row) ):
        class_name = current_row[i].value
        match_result = regular_matcher.match(class_name)
        type_name = tmp_row[i].value
        if class_name != '':
            if '一' == match_result.group(1):
                current_class = Class(grade=1, name=class_name, type= type_name, number=match_result.group(2))
            elif '二' == match_result.group(1):
                current_class = Class(grade=2, name=class_name, type= type_name, number=match_result.group(2))
            elif '三' == match_result.group(1):
                current_class = Class(grade=3, name=class_name, type= type_name, number=match_result.group(2))
            current_class.save()
            root += [current_class]
            start_column += [i]
            class_end += [False]

    i = 3
    while False in class_end:
        current_row = sheet.row(i)
        for idx in range( len(start_column) ):
            j = start_column[idx]
            if current_row[j+1].value != '':
                student = Student(id_in_class = int(current_row[j].value),
                                  name = current_row[j+1].value,
                                  student_id = current_row[j+2].value,
                                  gender = current_row[j+3].value,
                                  the_class = root[idx]
                                  )
                student.save()
                students += [student]
            else:
                class_end[idx] = True
        i+=1
    return (root,students)

if __name__ == '__main__':
    structure_data('../test.xls')
