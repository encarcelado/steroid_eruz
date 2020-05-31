#скрипт забирает все данные ЕРУЗ и закидывает их в MySQL

import bs4 as bs
import urllib.request
#import os
import mysql.connector
import re



mydb = mysql.connector.connect(host="v0434826.beget.tech", user="v0434826_eruz", passwd="1560ford", database = "v0434826_eruz")
mydb.autocommit = True

print(mydb)

if(mydb):
    print("Connection is successful")
else:
    print("Connection is unsuccessful")

my_cursor = mydb.cursor()


my_cursor.execute("SHOW TABLES")
for table in my_cursor:
    print(table[0])

# my_cursor.execute("SELECT * FROM nalog_codes WHERE nalog_city = 'Уфа г'")
#
# for table in my_cursor:
#     print(table)
eruzMemberNumWithoutBossID = []
personINN = "760900099494"
sql6 = "SELECT id FROM boss_person WHERE boss_inn = %s"
my_cursor.execute(sql6, (personINN,))
bossPersonID = my_cursor.fetchone()[0]
print("Получен Id личности:", bossPersonID)

my_cursor.execute("SELECT eruz_registry_id FROM eruz_member WHERE tip_uchastnika_id = 3 OR tip_uchastnika_id = 2  AND  boss_person_id = 0")
eruzCounter = 0

for eruzNum in my_cursor:
    testNum = eruzNum[0]
    eruzMemberNumWithoutBossID[eruzCounter] = testNum
    eruzCounter = eruzCounter + 1
    print(eruzNum[eruzMemberNumWithoutBossID[eruzCounter]])
    # eruzMemberNumWithoutBossID = str(eruzNum[0])
    # eruzLink = "https://zakupki.gov.ru/epz/eruz/card/general-information.html?reestrNumber=" + eruzMemberNumWithoutBossID
    # print(eruzLink)
    # try:
    #     sauce = urllib.request.urlopen(eruzLink).read()
    # except AttributeError:
    #     time.sleep(10)
    #     sauce = urllib.request.urlopen(eruzLink).read()
    # except:
    #     continue
    #
    # content = sauce.decode("utf-8")
    # soup = bs.BeautifulSoup(content, "lxml")
    # zapisNeNaidena = soup.find("h2").text
    #
    #     # Если "Запись не найдена", переходил на следующую
    #
    # if zapisNeNaidena == "Запись не найдена":
    #     print("Запись не найдена", eruzLink)
    #     continue
    #
    #
    # personINN = soup.find("span", text="ИНН").next_sibling.next_sibling.text.strip()
    # print(personINN)
    #
    # bossFullName = soup.find("span", text="ФИО").next_sibling.next_sibling.text.title().strip()
    # #print(bossFullName)
    #
    # bossFullNameSplit = bossFullName.split()
    # bossLastName = bossFullNameSplit[0]
    # bossFirstName = bossFullNameSplit[1]
    #
    # try:
    #     bossSecondName = bossFullNameSplit[2]
    # except:
    #     bossSecondName = ""
    #
    # print(bossFirstName, bossSecondName, bossLastName, personINN)
    #
    #
    #
    # companyEmail = soup.find("span", text="Адрес электронной почты").next_sibling.next_sibling.text.replace(" ", "")
    # companyEmail = companyEmail.replace(" ", "")
    # print(companyEmail)
    #
    # sql2 = "SELECT id FROM boss_person WHERE boss_inn = %s"
    #
    # try:
    #     my_cursor.execute(sql2, (personINN,))
    #     bossPersonID = my_cursor.fetchone()[0]
    #     # nalogInfo = my_cursor.fetchall()
    #     # for x in nalogInfo:
    #     #    print(x)
    #     print("Получен Id личности:", bossPersonID)
    # except AttributeError:
    #     sql3 = "INSERT INTO boss_person(boss_inn, full_name, f_name, s_name, l_name, email_1) values(%s, %s, %s, %s, %s, %s)"
    #     my_cursor.execute(sql3, (personINN, bossFullName, bossFirstName, bossSecondName, bossLastName, companyEmail))
    #     sql4 = "SELECT id FROM boss_person WHERE boss_inn = %s"
    #     my_cursor2.execute(sql4, (personINN,))
    #     bossPersonID = my_cursor.fetchone()[0]
    #     print(bossPersonID)
    #     print("Вставили данные по личности")
    #
    #     sql5 = "UPDATE eruz_member SET boss_person_id=%s WHERE eruz_registry_id = %s"
    #     my_cursor.execute(sql5, (bossPersonID, eruzMemberNumWithoutBossID,))
    #     print("Обновили запись члена ЕРУЗ ссылкой на личность")
    # except:
    #     print("Что-то все-таки пошло не так")
    #

    #
    # try:
    #     sql3 = "INSERT INTO boss_person(boss_inn, full_name, f_name, s_name, l_name, email_1) values(%s, %s, %s, %s, %s, %s)"
    #     my_cursor.execute(sql3, (personINN, bossFullName, bossFirstName, bossSecondName, bossLastName, companyEmail))
    #     sql4 = "SELECT id FROM boss_person WHERE boss_inn = %s"
    #     my_cursor.execute(sql4, (personINN,))
    #     bossPersonID = my_cursor.fetchone()[0]
    #     print(bossPersonID)
    # # except AttributeError:
    # except AttributeError:
    #     sql4 = "SELECT id FROM boss_person WHERE boss_inn = %s"
    #     my_cursor.execute(sql4, (personINN,))
    #     bossPersonID = my_cursor.fetchone()[0]
    #     print("Такой босс уже есть", bossPersonID)
    # except AttributeError:
    #     sql4 = "SELECT id FROM boss_person WHERE full_name = %s"
    #     my_cursor.execute(sql4, (bossFullName,))
    #     bossPersonID = my_cursor.fetchone()[0]
    #     print("Такой босс уже есть", bossPersonID)
    # except:
    #     bossPersonID = ""
    #     print("Ошибка с ID босса")
    #
    # sql = "INSERT INTO eruz_member(eruz_registry_id, eruz_member_inn, registry_date, ogrnip, nalog_reg_date, company_email, registry_status, tip_uchastnika_id, small_business_subject, nalog_codes_id, boss_person_id) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    # my_cursor.execute(sql, (
    # eruzNum, personINN, ipRegDate, OGRNIP, nalogRegDate, companyEmail, statusReg, int(tipUchastnikaID),
    # smallBusinessSubject, nalogCodesID, bossPersonID))
    #
    # sql5 = "SELECT id FROM eruz_member WHERE eruz_registry_id = %s"
    # my_cursor.execute(sql5, (eruzNum,))
    # eruzRegistryID = my_cursor.fetchone()[0]
    #
    # # mydb.commit()
    # if tipUchastnikaID == 3:
    #     print("Запись индивидуального предпринимателя успешно занесена в реестр под Id=", eruzRegistryID)
    # else:
    #     print("Запись физического лица РФ успешно занесена в реестр под Id=", eruzRegistryID)