import psycopg2

try:
    conn = psycopg2.connect(
        dbname="formulariosenai",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )
    print("Conexão bem-sucedida!")
    conn.close()
except Exception as e:
    print("Erro na conexão:", e)
