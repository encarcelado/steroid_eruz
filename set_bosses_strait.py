import mysql.connector
import sys

mydb = mysql.connector.connect(host="v0434826.beget.tech", user="v0434826_eruz", passwd="expertiki100%", database = "v0434826_eruz")
mydb.autocommit = True

print(mydb)

if(mydb):
    print("Connection is successful")

else:
    print("Connection is unsuccessful")

my_cursor = mydb.cursor(buffered=True)

try:
    sql5 = "SELECT MAX(id) FROM eruz_member"
    my_cursor.execute(sql5)
    last_eruz_id = my_cursor.fetchone()[0]
    print("Last ERUZ id= ", last_eruz_id)

except:
    print("No last eruz id")
    sys.exit()






startEruzId = open('Z_startEruzId.txt', 'r').read()

startEruzId = int(startEruzId)
last_eruz_id = int(last_eruz_id)

while startEruzId < last_eruz_id:

    try:
        sql5 = "SELECT boss_person_id FROM eruz_member WHERE id = %s"
        my_cursor.execute(sql5, (startEruzId,))
        boss_person_id = my_cursor.fetchone()[0]
        print("boss_person_id=", boss_person_id)
    except:
        print("boss_person_id из id " + str(startEruzId) + " не выделился")
        startEruzId = startEruzId + 1
        startEruzIdString = str(startEruzId)
        # os.remove("startEruzNum.txt")
        f = open("Z_startEruzId.txt", "w")
        f.write(startEruzIdString)
        f.close()
        continue

    setOne = 1



    if not boss_person_id or boss_person_id == 0 or boss_person_id == "0":
        try:
            sql5 = "UPDATE eruz_member SET boss_person_id = %s WHERE id = %s"
            my_cursor.execute(sql5, (setOne, startEruzId))
            print("Нулевому боссу присвоили единицу!!!!!!!!!")
        except:
            print("Что-то пошло не так нулевому боссу ничего не присвоили")




    startEruzId = startEruzId + 1
    startEruzIdString = str(startEruzId)
    # os.remove("startEruzNum.txt")
    f = open("Z_startEruzId.txt", "w")
    f.write(startEruzIdString)
    f.close()