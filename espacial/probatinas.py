import sqlite3

con = sqlite3.connect('score.db')
cur = con.cursor()
cur.execute("""
            SELECT Player,Puntos 
            FROM puntuaciones \
            ORDER BY Puntos DESC
            """
    )
datos = cur.fetchall()
cur.close()



for i in range(3):
    #result = 10-len(datos[i][0])*1+40*1
    player = str(datos[i][0])
    print (player, len(player))