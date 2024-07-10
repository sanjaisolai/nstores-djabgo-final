import sqlite3
con=sqlite3.connect("db.sqlite3")
cur=con.cursor()
query=f'''
INSERT INTO Words (name)
SELECT 'check'
WHERE NOT EXISTS (
    SELECT 1 FROM Words WHERE name = 'check'
);
'''
# cur.execute("delete from Words where name='chillies,'")
cur.execute("select * from Words")
tup=cur.fetchall()
print(tup)
con.commit()
con.close()


data_dir = r'C:\Users\sanjai\Desktop\nstore qc automation web application django\nstores_QC\nstores_QC\dataset'  # Path to your dataset
model_dir = r'C:\Users\sanjai\Desktop\nstore qc automation web application django\nstores_QC\nstores_QC\models'