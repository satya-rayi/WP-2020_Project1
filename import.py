import os
import csv
from database_setup import Books, db
from sqlalchemy.exc import IntegrityError

# isbn = "1111"
# title = "test"
# author = "test"
# year = 2000
# bk = Books(isbn=isbn, title=title, author=author, year=year)
# try:
# 	db.add(bk)
# 	db.commit()
# except IntegrityError:
# 	print("ISBN already exists")
# 	db.rollback()

with open('books.csv', 'r') as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	#isbn,title,author,year
	for row in reader:		
		try:
			isbn = (row[0])
			title = (row[1])
			author = (row[2])
			year = int(row[3])
			book = Books(isbn=isbn, title=title, author=author, year=year)
			db.add(book)
			db.commit()
		except IntegrityError:
			print("ISBN already exists")
			db.rollback()
	
