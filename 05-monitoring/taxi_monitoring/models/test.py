import psycopg
conn = psycopg.connect("host=localhost port=5432 dbname=test user=postgres password=example gssencmode=disable", autocommit=True)
print("Connection successful!")
