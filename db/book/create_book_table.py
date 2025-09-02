import psycopg2 # type: ignore

# connect to the database
conn = psycopg2.connect(
  user="postgres", 
  password="1111",
  host="localhost",
  database="mydb"
  )

# create a cursor
cursor = conn.cursor()

# create table
cursor.execute("""CREATE TABLE book (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100),
    author VARCHAR(100),
    language VARCHAR(50),
    published_date DATE
)
""")

# commit changes and close the connection
conn.commit()
# cursor.close()
conn.close()
