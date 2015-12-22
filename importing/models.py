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
    student_id = models.TextField(max_length=20)
    the_class = models.ForeignKey(Class, default=None)
    times_remain_to_clean = models.PositiveSmallIntegerField(default=3)
    date_to_come = models.TextField()

def retreive_to_db(file_name):
    for sheet in structure_data('test.xls'):
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
    current_row = sheet.row(1)
    tmp_row = sheet.row(0)
    for i in range( len(current_row) ):
        class_name = current_row[i].value
        type_name = tmp_row[i].value
        if class_name != '':
            if '一年' in class_name:
                current_class = Class(grade=1, name=class_name, type= type_name)
            elif '二年' in class_name:
                current_class = Class(grade=2, name=class_name, type= type_name)
            elif '三年' in class_name:
                current_class = Class(grade=3, name=class_name, type= type_name)
            current_class.save()
            root += [current_class]
            start_column += [i]
            class_end += [False]

    i = 3
    while False in class_end:
        current_row = sheet.row(i)
        for idx in range( len(start_column) ):
            j = start_column[idx]
            if current_row[j].value != '':
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
