from django.db import models
import xlrd

# Create your models here.
#
class Class(models.Model):
    grade = models.TextField()
    name = models.TextField(default=None)
    type = models.TextField(max_length=20)

class Student(models.Model):
    id_in_class = models.PositiveSmallIntegerField(default=0)
    name = models.TextField(max_length=20)
    gender = models.TextField(max_length=10)
    student_id = models.PositiveSmallIntegerField()
    the_class = models.ForeignKey(Class, default=None)


def structure_data(file_name):
    book = xlrd.open_workbook(file_name)
    for i in range(3):
        structure_class( book.sheet_by_index(i) )

def structure_class(sheet):
    root = []
    start_column = []
    class_end = []

    # Read Class number and name
    current_row = sheet.row(1)
    for i in range( len(current_row) ):
        class_name = current_row[i].value
        if class_name != '':
            if '一年' in class_name:
                current_class = Class(grade=1, name=class_name)
            elif '二年' in class_name:
                current_class = Class(grade=1, name=class_name)
            elif '三年' in class_name:
                current_class = Class(grade=1, name=class_name)
            root += [current_class]
            start_column += [i]
            class_end += [False]

    # Read type
    current_row = sheet.row(0)
    for i in range( len(root) ):
        type_name = current_row[i].value
        if type_name != '':
            root[i].type = type_name


    i = 3
    while False in class_end:
        current_row = sheet.row(i)
        for idx in range( len(start_column) ):
            j = start_column[idx]
            if current_row[j].value != '':
                student = Student(id_in_class = current_row[j],
                                  name = current_row[j+1],
                                  student_id = current_row[j+2],
                                  gender = current_row[j+3],
                                  the_class = root[idx]
                                  )
            else:
                class_end[idx] = True
        i+=1

if __name__ == '__main__':
    structure_data('../test.xls')
