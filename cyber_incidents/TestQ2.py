import csv
import xlrd
import utils
import db

db.transform_csv('data/cyber-operations-incidents.csv','data/cyber-operations-incidents2.csv')

conf = utils.load_config()
print(conf)
