import sqlite3

# Sample array of elements
elements = [
    'adai', 'akkaravadisal', 'appam', 'arachuvitta', 'arisi', 'bath', 'bele', 'benne', 'bhath', 'biriyani', 'bisi', 'bisibelabath', 'bisibele', 'boorelu', 'chakara', 'chettinad', 'chettinadu', 'chicken', 'chops', 'chukka', 'chutney', 'coconut', 'curd', 'davangere', 'dosa', 'dosai', 'fish', 'food', 'fry', 'gobi', 'gur', 'idiyappam', 'idli', 'inji', 'kadamba', 'kai', 'kal', 'kali', 'kalkandu', 'kambu', 'kara', 'kari', 'karuvadu', 'karuveppilai', 'kathirikai', 'kavuni', 'keerai', 'kizhangu', 'kola', 'kollu', 'kootu', 'koozh', 'kosu', 'kothamalli', 'kothu', 'kozhambu', 'kozhi', 'kozhikari', 'kozhukattai', 'kulambu', 'kuli', 'kurma', 'kuzhambu', 'kuzhi', 'lemon', 'maavu', 'madras', 'madurai', 'mangai', 'masala', 'masiyal', 'meen', 'milagu', 'millet', 'millets', 'mithai', 'mixture', 'mochai', 'mor', 'morkootu', 'mudde', 'mullu', 'murukku', 'murungai', 'mutton', 'nadu', 'nattu', 'nei', 'nellai', 'nellikkai', 'paal', 'pachadi', 'paniyaram', 'parotta', 'paruppu', 'paya', 'payasam', 'payatham', 'payir', 'pazham', 'pazhaya', 'pepper', 'pirattal', 'podi', 'podimas', 'pongal', 'poornam', 'poosanikai', 'poriyal', 'potato', 'puli', 'puliyodarai', 'puliyogare', 'puri', 'puthina', 'puttu', 'ragi', 'rasam', 'rava', 'recipes', 'rice', 'sadam', 'sakkarai', 'sambar', 'sambhar', 'satham', 'sev', 'siru', 'sodhi', 'sundal', 'sura', 'tamarind', 'tamil', 'thair', 'thakkali', 'thalicha', 'thanni', 'thatta', 'thattai', 'thattu', 'thavala', 'thayir', 'then', 'thenga', 'thengai', 'thenkuzhal', 'thiruvathirai', 'thogayal', 'thokku', 'thoran', 'thuvaiyal', 'tomato', 'upma', 'uraundai', 'urundai', 'uttapam', 'vada', 'vadai', 'varagu', 'varuval', 'vatha', 'vathal', 'vazhakkai', 'vazhapoo', 'veg', 'vellai', 'ven', 'vendaikai', 'vendhaya', 'vengaya','runtime',"la'forte"
]

# SQLite database file path
db_path = 'exception_words.db'

# Connect to SQLite database
conn = sqlite3.connect("db.sqlite3")
cursor = conn.cursor()

# Create a table if it doesn't exist
create_table_sql = """
    CREATE TABLE IF NOT EXISTS Words (
        name TEXT
    )
"""
cursor.execute(create_table_sql)

# Insert array elements into the table
insert_sql = "INSERT INTO Words (name) VALUES (?)"

for element in elements:
    cursor.execute(insert_sql, (element,))

# Commit changes and close connection
conn.commit()
conn.close()

print("Elements inserted successfully into SQLite database.")
