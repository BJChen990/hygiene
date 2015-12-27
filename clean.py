__author__ = 'chenbangjing'
import os

if __name__ == '__main__':
    for file in os.listdir('./'):
        if file.endswith('.xls') or file.endswith('.sqlite3'):
            print('remove'+file)
            os.remove(file)