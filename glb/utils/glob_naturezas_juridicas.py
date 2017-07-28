import csv
import sqlite3

conn = sqlite3.connect('C:/Users/eduar/DjangoProjects/Dev/contabilidade/db.sqlite3')
c = conn.cursor()

arquivo = open('glob_naturezas_juridicas.txt', 'r', encoding='UTF-8')
creader = csv.reader(arquivo, delimiter="|")
next(creader)


for r in creader:
    # Insert a row of data
    print(r)
    c.execute("INSERT INTO glb_globalnaturezajuridica  VALUES (?, ?, ?);", r)

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
arquivo.close()
