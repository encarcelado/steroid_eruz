#скрипт забирает все данные ЕРУЗ и закидывает их в MySQL

import bs4 as bs
import urllib.request
#import os
import mysql.connector
import re

mydb = mysql.connector.connect(host="v0434826.beget.tech", user="v0434826_eruz", passwd="1560ford", database = "v0434826_eruz")

print(mydb)

if(mydb):
    print("Connection is successful")
else:
    print("Connection is unsuccessful")

my_cursor = mydb.cursor()

my_cursor.execute("SHOW TABLES")
for table in my_cursor:
    print(table[0])

#my_cursor.execute("SELECT * FROM nalog_codes WHERE region_code = 02")

#for table in my_cursor:
#    print(table)

#my_cursor.execute("SELECT * FROM okved_codes WHERE SubKod1 = 1")

#for table in my_cursor:
#    print(table)

my_cursor.execute("SELECT nalog_city FROM nalog_codes WHERE nalog_region LIKE '%Башкортостан%'")

for table in my_cursor:
    print(table[0])

startEruzNum = open('startEruzNum.txt', 'r').read()

#print(startEruzNumFromText)
#startEruzNum = 19000001
endEruzNum = 20450000
endEruzNumLastYear = 19333006

if not startEruzNum:
    startEruzNum = open('startEruzNumBackup.txt', 'r').read()

startEruzNum = int(startEruzNum)

if startEruzNum > 19333006 and startEruzNum < 20000000:
    startEruzNum = 20000000

while startEruzNum < endEruzNum:
    startEruzNumString = str(startEruzNum)
    eruzLink = "https://zakupki.gov.ru/epz/eruz/card/general-information.html?reestrNumber=" + startEruzNumString
    sauce = urllib.request.urlopen(eruzLink).read()
    content = sauce.decode("utf-8")

    #print(content)

    #soup = bs.BeautifulSoup(content, "html.parser")
    soup = bs.BeautifulSoup(content, "lxml")
    zapisNeNaidena = soup.find("h2").text

#Если "Запись не найдена", переходил на следующую

    if zapisNeNaidena == "Запись не найдена":
        startEruzNum = startEruzNum + 1
        continue

    tipUchastnika = soup.find("span", text="Тип участника закупки").next_sibling.next_sibling.text

    if tipUchastnika == "Юридическое лицо РФ":
        tipUchastnikaID = 1

    if tipUchastnika == "Физическое лицо РФ":
        tipUchastnikaID = 2

    if tipUchastnika == "Физическое лицо РФ (индивидуальный предприниматель)":
        tipUchastnikaID = 3

    if tipUchastnika == "Юридическое лицо иностранного государства":
        tipUchastnikaID = 4

    if tipUchastnika == "Физическое лицо иностранного государства":
        tipUchastnikaID = 5

    if tipUchastnika == "Физическое лицо иностранного государства (индивидуальный предприниматель)":
        tipUchastnikaID = 6

    if tipUchastnika == "Обособленное подразделение юридического лица РФ":
        tipUchastnikaID = 7

    if tipUchastnika == "Аккредитованный филиал или представительство иностранного юридического лица":
        tipUchastnikaID = 8
    else:
        tipUchastnika = 1

#Если субъект Физлицо РФ или ИП, то отдельная собиралка

    if tipUchastnika == "Физическое лицо РФ" or tipUchastnika == "Физическое лицо РФ (индивидуальный предприниматель)":
        print(soup.title.text)  # or string
        print(startEruzNumString)

        eruzNum = soup.find("span", text="Номер реестровой записи в ЕРУЗ").next_sibling.next_sibling.text
        print(eruzLink)

        statusReg = soup.find("span", text="Статус регистрации").next_sibling.next_sibling.text
        print(statusReg)



        print(tipUchastnika)

        dataReg = soup.find("span", text="Дата регистрации в ЕИС").next_sibling.next_sibling.text
        print(dataReg)

        personINN = soup.find("span", text="ИНН").next_sibling.next_sibling.text.strip()
        print(personINN)

        bossFullName= soup.find("span", text="ФИО").next_sibling.next_sibling.text.strip()
        print(bossFullName)

        bossFullNameSplit = bossFullName.split()
        bossLastName = bossFullNameSplit[0]
        bossFirstName = bossFullNameSplit[1]

        try:
            bossSecondName = bossFullNameSplit[2]
        except AttributeError:
            bossSecondName = ""

        print(bossFirstName, bossSecondName, bossLastName, personINN)

        OGRNIP = soup.find("span", text="ОГРНИП").next_sibling.next_sibling.text.strip()
        print(OGRNIP)

        nalogRegDate = soup.find("span", text="Дата постановки на учет в налоговом органе").next_sibling.next_sibling.text.strip()
        print(nalogRegDate)

        ipRegDate = soup.find("span", text="Дата регистрации индивидуального предпринимателя").next_sibling.next_sibling.text.strip()
        print(ipRegDate)

        companyEmail = soup.find("span", text="Адрес электронной почты").next_sibling.next_sibling.text.replace(" ", "")
        print(companyEmail)

        startEruzNum = startEruzNum + 1
        startEruzNumString = str(startEruzNum)
        # os.remove("startEruzNum.txt")
        f = open("startEruzNum.txt", "w")
        f.write(startEruzNumString)
        f.close()
        continue


    print(soup.title.text) #or string

    print(startEruzNumString)

    eruzNum = soup.find("span", text="Номер реестровой записи в ЕРУЗ").next_sibling.next_sibling.text
    print(eruzLink)

    statusReg = soup.find("span", text="Статус регистрации").next_sibling.next_sibling.text
    print(statusReg)

    print(tipUchastnika)

    dataReg = soup.find("span", text="Дата регистрации в ЕИС").next_sibling.next_sibling.text
    print(dataReg)

    try:
        fullCompanyName = soup.find("span", text="Полное наименование").next_sibling.next_sibling.text.title()
        print(fullCompanyName)
    except AttributeError:
        fullCompanyName = ""
        print("Полное имя не опубликовано")

    try:
        shortCompanyName = soup.find("span", text="Сокращенное наименование").next_sibling.next_sibling.text
        print(shortCompanyName)
    except AttributeError:
        shortCompanyName = ""
        print("Короткое имя не опубликовано")

    companyAddress = soup.find("span", text="Адрес в пределах места нахождения").next_sibling.next_sibling.text.title()
    print(companyAddress)

    companyOkveds = soup.find("span", text="Код(ы) ОКВЭД").next_sibling.next_sibling






    #for singleOkved in companyOkveds.find_all("div"):
    #    print(singleOkved.text)

    #singleOkved2 = companyOkveds.find_all("div")
    #print("One Okved")
    #print(singleOkved2[1].text)




    companyINN = soup.find("span", text="ИНН").next_sibling.next_sibling.text.strip()
    print(companyINN)

    try:
        companyKPP = soup.find("span", text="КПП").next_sibling.next_sibling.text.strip()
        print(companyKPP)
    except AttributeError:
        companyKPP = ""

    if companyKPP:
        nalogCode = companyKPP[:4]
        nalogCodeZapasnoy = companyKPP[:2] + "00"
        print(nalogCode, nalogCodeZapasnoy)
    else:
        nalogCode = companyINN[:4]
        nalogCodeZapasnoy
        nalogCodeZapasnoy = companyINN[:2] + "00"
        print(nalogCode, nalogCodeZapasnoy)

    companyRegDate = soup.find("span", text="Дата постановки на учет в налоговом органе").next_sibling.next_sibling.text.strip()
    print(companyRegDate)

    companyOGRN = soup.find("span", text="ОГРН").next_sibling.next_sibling.text.strip()
    print(companyOGRN)

    nalogRegDate = soup.find("span", text="Дата постановки на учет в налоговом органе").next_sibling.next_sibling.text.strip()
    print(nalogRegDate)





    try:
        smallBusinessSubject = soup.find("span", text="Да").text.strip()
        print(smallBusinessSubject)

        if smallBusinessSubject == "Да":
            smallBusinessSubject = 2
        else:
            smallBusinessSubject = 1
    except AttributeError:
        smallBusinessSubject = 1



    try:
        bossFullName = soup.find("td", class_="tableBlock__col").text.title()

        bossFullNameSplit = bossFullName.split()
        bossLastName = bossFullNameSplit[0]
        bossFirstName = bossFullNameSplit[1]
        bossSecondName = bossFullNameSplit[2]
        bossTitle = soup.find("td", class_="tableBlock__col").next_sibling.next_sibling.text.title()
        personINN = soup.find("td", class_="tableBlock__col").next_sibling.next_sibling.next_sibling.next_sibling.text
        print(bossFirstName, bossSecondName, bossLastName, bossTitle, personINN)
    except AttributeError:
        bossFullNameSplit = ""
        bossLastName = ""
        bossFirstName = ""
        bossSecondName = ""
        personINN = ""
        bossFullName = ""
        print("Данные о руководителе не опубликованы")



    companyEmail = soup.find("span", text="Адрес электронной почты").next_sibling.next_sibling.text.replace(" ", "")
    print(companyEmail)

    companyPhone = soup.find("span", text="Контактный телефон").next_sibling.next_sibling.text.replace(" ", "")
    #companyPhone = soup.find("span", text="Контактный телефон").next_sibling.next_sibling.text.replace(" ", "")
    companyPhone = companyPhone.replace(" ", "")
    companyPhone = companyPhone.replace(")", "")
    companyPhone = companyPhone.replace("(", "")
    companyPhone = companyPhone.replace("-", "")
    companyPhone = companyPhone.replace("+", "")
    companyPhone = re.sub(r'^8', '7', companyPhone)

    companyCell = ""
    #companyCell = re.match("((\+7|7|7\s|8|\+7\s|8\s|^|\s)-?)\(?(9\d{2})\)?-?\s?\d{1}-?\d{1}-?\s?\d{1}-?\s?\d{1}-?\s?\d{1}-?\s?\d{1}-?\d{1}(?=\s|,|$|\.)", companyPhone)
    companyCell = re.match("^79\d*", companyPhone)

    if companyCell:
        companyCell = companyPhone
        companyPhone = ""
        print("Сотовый телефон", companyCell)
    else:
        print("Офисный телефон", companyPhone)
        companyCell = ""





    try:
        companySite = soup.find("span", text="Адрес сайта в сети интернет").next_sibling.next_sibling.text.replace(" ", "")
        print(companySite)
    except AttributeError:
        companySite = ""
        print("Название сайта не опубликовано")

    sql2 = "SELECT id FROM nalog_codes WHERE nalog_kod = %s"

    try:
        my_cursor.execute(sql2, (nalogCode,))
        nalogCodesID = my_cursor.fetchone()[0]
        #nalogInfo = my_cursor.fetchall()
        #for x in nalogInfo:
        #    print(x)
        print(nalogCodesID)
    except:
        my_cursor.execute(sql2, (nalogCodeZapasnoy,))
        nalogCodesID = my_cursor.fetchone()[0]
        print(nalogCodesID)

    try:
        sql3 = "INSERT INTO boss_person(boss_inn, full_name, f_name, s_name, l_name, phone_1, cellphone_1, email_1) values(%s, %s, %s, %s, %s, %s, %s, %s)"
        my_cursor.execute(sql3, (personINN, bossFullName, bossFirstName, bossSecondName, bossLastName, companyPhone, companyCell, companyEmail))
        sql4 = "SELECT id FROM boss_person WHERE boss_inn = %s"
        my_cursor.execute(sql4, (personINN,))
        bossPersonID = my_cursor.fetchone()[0]
        print(bossPersonID)
    except AttributeError:
        sql4 = "SELECT id FROM boss_person WHERE boss_inn = %s"
        my_cursor.execute(sql4, (personINN,))
        bossPersonID = my_cursor.fetchone()[0]
        print("Такой босс уже есть", bossPersonID)
    except:
        bossPersonID = ""
        print("Ошибка с ID босса")


    sql = "INSERT INTO eruz_member(full_company_name, short_company_name, eruz_registry_id, eruz_member_inn, registry_date, ogrn, nalog_reg_date, company_email, company_phone, company_cell, company_address, company_kpp, company_site, registry_status, tip_uchastnika_id, small_business_subject, nalog_codes_id, boss_person_id) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    my_cursor.execute(sql, (fullCompanyName, shortCompanyName, eruzNum, companyINN, companyRegDate, companyOGRN, nalogRegDate, companyEmail, companyPhone, companyCell, companyAddress, companyKPP, companySite, statusReg, int(tipUchastnikaID), int(smallBusinessSubject), int(nalogCodesID), bossPersonID))

    sql5 = "SELECT id FROM eruz_member WHERE eruz_registry_id = %s"
    my_cursor.execute(sql5, (eruzNum,))
    eruzRegistryID = my_cursor.fetchone()[0]
    print("Запись занесена в реестр под Id=", eruzRegistryID)



    for singleOkved in companyOkveds.find_all("div"):
        singleOkved = singleOkved.text
        # singleOkvedSplit = singleOkved.split(".")
        # singleOkvedSubKod1 = int(singleOkvedSplit[0])
        # singleOkvedSubKod2 = int(singleOkvedSplit[1])
        # singleOkvedSubKod3 = int(singleOkvedSplit[2])
        # print(singleOkvedSubKod1, singleOkvedSubKod2,singleOkvedSubKod3)


        try:
            sql6 = "SELECT id FROM okved_2020 WHERE okved_code = %s"
            my_cursor.execute(sql6, (singleOkved,))
            okved2020ID = my_cursor.fetchone()[0]

            sql7 = "INSERT INTO eruz_member_okved_codes(gov_eruz_registry_id, okved_codes_id) values(%s, %s)"
            my_cursor.execute(sql7, (int(eruzRegistryID), okved2020ID))
        except:
            sql6 = "SELECT id FROM okved_2020 WHERE okved_code = %s"
            singleOkvedZapasnoy = singleOkved[:2]
            my_cursor.execute(sql6, (singleOkvedZapasnoy,))
            okved2020ID = my_cursor.fetchone()[0]

            sql7 = "INSERT INTO eruz_member_okved_codes(gov_eruz_registry_id, okved_codes_id) values(%s, %s)"
            my_cursor.execute(sql7, (int(eruzRegistryID), okved2020ID))



        print(singleOkved)

    mydb.commit()

    startEruzNum = startEruzNum + 1
    startEruzNumString = str(startEruzNum)
    #os.remove("startEruzNum.txt")
    f = open("startEruzNum.txt", "w")
    f.write(startEruzNumString)
    f = open("startEruzNumBackup.txt", "w")
    f.write(startEruzNumString)
    f.close()




