#скрипт забирает все данные ЕРУЗ и закидывает их в MySQL

import bs4 as bs
from itertools import cycle
import traceback
import os
import mysql.connector
import re
import time
from colorama import Fore, Back, Style
import datetime
import sys
# import urllib
import socket
import requests
from fake_useragent import UserAgent
import random
from fp.fp import FreeProxy

ua = UserAgent()
# CREATES PROXY FOR RUSPROFILE MINING
# http://list.didsoft.com/get?email=vadimkhar@mail.ru&pass=qhgiqs&pid=socks1100&showcountry=no

# def check_in():
#
#     fqn = os.uname()[1]
#     ext_ip = urllib.urlopen('http://whatismyip.org').read()
#     print("Asset: %s " % fqn, "Checking in from IP#: %s " % ext_ip)

# def GetProxy():
#     url = 'http://list.didsoft.com/get?email=vadimkhar@mail.ru&pass=qhgiqs&pid=socks1100&showcountry=no'
#     url = 'http://list.didsoft.com/get?email=vadimkhar@mail.ru&pass=qhgiqs&pid=socks1100&showcountry=no&country=RU'
#     response2 = requests.get(url)
#     parser = response2.text
#     parser = parser.splitlines()
#     proxies = set()
#
#     for e in parser:
#         e = e.strip('#socks4')
#         e = e.split(":")
#         # print(e[0], e[1])
#         proxy = ":".join([e[0], e[1]])
#         proxies.add(proxy)
#
#     # print(proxies)
#     # proxyDict = {}
#     # proxy = FreeProxy(rand=True).get()
#     # print(proxy)
#     # proxyDict['http'] = proxy
#     # proxyDict['https'] = proxy
#     return proxies
# END PROXY FOR RUSPROFILE MINING
#
#
#
# proxies = GetProxy()
# # print(proxies)
#
#
#
#
#########FUNCTION ADDS MAIN OKVED AND MAIN OKVED DESCRIPTION FROM RUSPROFILE.RU TO NEW ERUZ ENTRIES AND OLD ERUZ ENTRIES
def GetMainOkved(eruzNumSent, eruzAlreadyRegistered, companyINN, eruzRegistryID):
    # return None
    mainOkved2 = ""
    if eruzAlreadyRegistered == True:
        try:
            sql5 = "SELECT main_okved FROM eruz_member WHERE eruz_registry_id = %s"
            my_cursor.execute(sql5, (eruzNumSent,))
            mainOkved2 = my_cursor.fetchone()[0]
            # print("Главный ОКВЭД уже существует в реестре под №", mainOkved2)
            # return None
        except:
            print("Главного ОКВЭДа у записи " + eruzNumSent + "нет, поэтому ищем")

    if mainOkved2 == "0" or not mainOkved2:
        print("Главный ОКВЭД не существует в реестре для записи ЕРУЗ " + eruzNumSent)
    else:
        print("Главный ОКВЭД уже существует в реестре под №", mainOkved2)
        return None

    if not companyINN or companyINN == "0":
        try:
            sql5 = "SELECT eruz_member_inn FROM eruz_member WHERE eruz_registry_id = %s"
            my_cursor.execute(sql5, (eruzNumSent,))
            companyINN = my_cursor.fetchone()[0]
            print("ИНН члена ЕРУЗ = ", companyINN)

        except:
            print("ИНН компании у записи " + eruzNumSent + "нет, поэтому бросаем затею с главным ОКВЭДОМ для этой записи")
            return None


    if len(companyINN) == 10:
        rusProfileLink = "https://www.rusprofile.ru/search?query=" + companyINN + "&type=ul&search_inactive=2"
        # rusProfileLink = "http://httpbin.org/ip"
    else:
        rusProfileLink = "https://www.rusprofile.ru/search?query=" + companyINN + "&search_inactive=2"
        # rusProfileLink = "http://httpbin.org/ip"
    # rusProfileLink = "https://www.rusprofile.ru/search?query=" + companyINN + "&search_inactive=2"
    # rusProfileLink = "https://www.rusprofile.ru/search?query=" + companyINN + "&type=ul&search_inactive=2"
    # rusProfileLink = "https://www.rusprofile.ru/search?query=" + companyINN
    print(rusProfileLink)

    wait = random.randint(10, 25)
    time.sleep(wait)
    proxies = ""
    headers2 = {'User-Agent': str(ua.random)}
    response2 = ""

    # try:
    #     proxies = GetProxy()
    #     proxy_pool = cycle(proxies)
    # except:
    #     proxies = ""



    # for i in range(1, 999):
    #     proxy = next(proxy_pool)
    #     proxy = {"http": "128.73.34.74:1080"}
    #     print
    #     response2 = ""
    #     try:
    #         # response2 = requests.get(rusProfileLink, headers=headers2, timeout=5, proxies={"http": proxy, "https": proxy})
    #         response2 = requests.get(rusProfileLink, headers=headers2, timeout=5,
    #                                  proxies=proxy)
    #         print("Что-то прочиталось с первой попытки c прокси")
    #         # print(response.json())
    # 
    #         break
    #     except:
    #         print(proxy)
    #         print("Skipping. Connnection error")
    #         response2 = ""
    # print(check_in())

    if not response2:
        try:
            response2 = requests.get(rusProfileLink, headers=headers2, timeout=5)
            print("Что-то прочиталось с первой попытки без прокси")

        except requests.exceptions.Timeout:
            # time.sleep(10)
            # sauce = urllib.request.urlopen(eruzLink).read()

            headers2 = {'User-Agent': str(ua.random)}
            response2 = requests.get(rusProfileLink, headers=headers2, timeout=5)
            print("Что-то прочиталось со второй попытки без прокси")

        except:

            print("сайт rusprofile не прочитался, поэтому облом с главным ОКВЭД")
            return None

    if response2.ok:
        s2 = response2.content
        print("Ответ rusprofile в порядке, вроде")
    else:

        print("сайт rusprofile не прочитался, поэтому облом с главным ОКВЭД 2")
        return None

    soup2 = bs.BeautifulSoup(s2, "lxml")
    mainOkvedFull = ""

    # mainOkvedFull2 = soup2.find("span", class_="company-info__title", text="Основной вид деятельности").next_sibling.text.strip()
    # print("Nothing " + mainOkvedFull2)
    # try:
    #     notAvailable = soup2.find("div", class_="error-code", text="HTTP ERROR 429").parent.text.strip()
    #     print(notAvailable, " Делаем паузу")
    #     wait = random.randint(25, 30)
    #     time.sleep(wait)
    # except:
    #     notAvailable = ""


    try:
        mainOkvedFull = soup2.find("span", text=re.compile("\(\d{2}\.")).parent.text.strip()
        print(mainOkvedFull)
    except:
        mainOkvedFull = ""

    # try:
    #     gosZakupkiRusprofile = soup2.find(text=re.compile("Госзакупки")).parent.parent.text.strip()
    #     print(gosZakupkiRusprofile)
    # except:
    #     gosZakupkiRusprofile = ""


    # if not mainOkvedFull:
    #     try:
    #         # mainOkvedFull = soup2.find("p", class_="tile-item__text").next_sibling.text.strip()
    #         mainOkvedFull = soup2.find("span", text=re.compile("\(\d{2}\.")).parent.text.strip()
    #         print(mainOkvedFull)
    #     except:
    #         mainOkvedFull = ""

    if not mainOkvedFull:
        print("Главный ОКВЭД все равно не нашелся")
        return None
    mainOkvedDesc2 = ""
    mainOkvedNum2 = ""
    mainOkvedDesc2 = re.findall(r"^.*", mainOkvedFull)
    mainOkvedNum2 = re.findall(r"(?<=\().*(?=\))", mainOkvedFull)
    mainOkvedDesc2 = mainOkvedDesc2[0].strip()
    mainOkvedNum2 = mainOkvedNum2[0].strip()
    print("Описание Оквэда: " + mainOkvedDesc2)
    print("Оквэд: " + mainOkvedNum2)

    if mainOkvedNum2:
        try:
            sql5 = "UPDATE eruz_member SET main_okved = %s, main_okved_desc = %s  WHERE id = %s"
            my_cursor.execute(sql5, (mainOkvedNum2, mainOkvedDesc2, eruzRegistryID))
        except:
            print("Что-то пошло не так и главный ОКВЭД с опианием добавлен не был")
            return None


#### END RUSPROFILE FUNCTION

 #MAKES FAKE BROWSER HEADERS WHEN REQUESTING CONTRACTS FROM ZAKUPKI.GOV.RU

today = datetime.date.today()

tomorrow = datetime.date.today() + datetime.timedelta(days=1)
d1 = today.strftime("%d.%m.%Y")
d12 = tomorrow.strftime("%d.%m.%Y")

# today = date.today()
# d1 = today.strftime("%d.%m.%Y")
print("Сегодня:", d1)
print("Завтра:", d12)
d1 = str(d12)


mydb = mysql.connector.connect(host="v0434826.beget.tech", user="v0434826_eruz", passwd="expertiki100%", database = "v0434826_eruz")
mydb.autocommit = True

print(mydb)

if(mydb):
    print(Fore.RED + "Connection is successful")
    print(Style.RESET_ALL)
else:
    print("Connection is unsuccessful")

my_cursor = mydb.cursor(buffered=True)

# my_cursor.execute("SHOW TABLES")
# for table in my_cursor:
#     print(table[0])

#my_cursor.execute("SELECT * FROM nalog_codes WHERE region_code = 02")

#for table in my_cursor:
#    print(table)

#my_cursor.execute("SELECT * FROM okved_codes WHERE SubKod1 = 1")

#for table in my_cursor:
#    print(table)

# my_cursor.execute("SELECT nalog_city FROM nalog_codes WHERE nalog_region LIKE '%Башкортостан%'")
#
# for table in my_cursor:
#     print(table[0])

startEruzNum = open('startEruzNum.txt', 'r').read()
endEruzNum = open('endEruzNum.txt', 'r').read()
endEruzNum = int(endEruzNum)

#print(startEruzNumFromText)
#startEruzNum = 19000001
#endEruzNum = 20450000
endEruzNumLastYear = 19333006

if not startEruzNum:
    startEruzNum = open('startEruzNumBackup.txt', 'r').read()

startEruzNum = int(startEruzNum)

if startEruzNum > 19333006 and startEruzNum < 20000000:
    startEruzNum = 20000000

while startEruzNum < endEruzNum:
    startEruzNumString = str(startEruzNum)
    fullCompanyName = ""
    shortCompanyName = ""
    bossFullName = ""
    bossFullNameSplit = ""
    personINN = ""
    bossFirstName = ""
    bossSecondName = ""
    bossLastName = ""
    companyEmail = ""
    companyCell = ""
    companyAddress = ""
    companyPhone = ""
    companyCountry = ""
    companyRegDate = ""
    companySite = ""
    companyINN = ""
    eruz_registry_date = ""
    eruz_registry_date2 = ""

    eruzLink = "https://zakupki.gov.ru/epz/eruz/card/general-information.html?reestrNumber=" + startEruzNumString
    eruzNum = startEruzNumString

    try:
        # sauce = urllib.request.urlopen(eruzLink).read()
        headers = {'User-Agent': str(ua.random)}
        response = requests.get(eruzLink, headers=headers, timeout=5)

    except requests.exceptions.Timeout:
        # time.sleep(10)
        # sauce = urllib.request.urlopen(eruzLink).read()
        headers = {'User-Agent': str(ua.random)}
        response = requests.get(eruzLink, headers=headers, timeout=5)

    except:
        startEruzNum = startEruzNum + 1
        startEruzNumString = str(startEruzNum)
        # os.remove("startEruzNum.txt")
        f = open("startEruzNum.txt", "w")
        f.write(startEruzNumString)
        f.close()
        print("Запись ЕРУЗ не прочиталось. Переходим на следующую")
        continue

    if response.ok:
        s = response.content
    else:
        startEruzNum = startEruzNum + 1
        continue





    #print(content)

    #soup = bs.BeautifulSoup(content, "html.parser")
    zapisNeNaidena = ""
    soup = bs.BeautifulSoup(s, "lxml")
    zapisNeNaidena = soup.find("h2").text

#Если "Запись не найдена", переходил на следующую

    if zapisNeNaidena == "Запись не найдена":
        print("Запись не найдена", eruzLink)
        startEruzNum = startEruzNum + 1
        continue

    eruzAlreadyRegistered = False
    try:
        sql5 = "SELECT id FROM eruz_member WHERE eruz_registry_id = %s"
        my_cursor.execute(sql5, (eruzNum,))
        eruzRegistryID = my_cursor.fetchone()[0]
        print("Запись уже существует в реестре под Id=", eruzRegistryID)
        eruzAlreadyRegistered = True
        GetMainOkved(eruzNum, eruzAlreadyRegistered, companyINN, eruzRegistryID)
    except:
        print(eruzLink)

    # regDateAlreadyRegistered = False
    if eruzAlreadyRegistered == True:
        try:
            sql5 = "SELECT eruz_registry_date FROM eruz_member WHERE eruz_registry_id = %s"
            my_cursor.execute(sql5, (eruzNum,))
            eruz_registry_date2 = my_cursor.fetchone()[0]
            if eruz_registry_date2:
                print("Дата регистрации в ЕРУЗ: " + eruz_registry_date2)
        except:
            None

        if not eruz_registry_date2:

            eruz_registry_date = soup.find("span", text="Дата регистрации в ЕИС").next_sibling.next_sibling.text.strip()
            print(eruz_registry_date)

            try:
                sql5 = "UPDATE eruz_member SET eruz_registry_date = %s WHERE eruz_registry_id = %s"
                my_cursor.execute(sql5, (eruz_registry_date, eruzNum))
                print("Дата регистрации компании в ЕРУЗ была добавлена")
            except:
                print("Что-то пошло не так и дата регистрации компании в ЕРУЗ не была добавлена")


        startEruzNum = startEruzNum + 1

        startEruzNumString = str(startEruzNum)

        f = open("startEruzNum.txt", "w")
        f.write(startEruzNumString)
        f = open("startEruzNumBackup.txt", "w")
        f.write(startEruzNumString)
        f.close()
        continue


    dataReg = soup.find("span", text="Дата регистрации в ЕИС").next_sibling.next_sibling.text
    print("Дата регистрации в ЕИС", dataReg)

    if dataReg == d1:
        print("Дата регистрации и сегодняшняя(завтрашняя) дата совпадают")
        time.sleep(10000)
        sys.exit()

    eruz_registry_date = soup.find("span", text="Дата регистрации в ЕИС").next_sibling.next_sibling.text.strip()
    print(eruz_registry_date)


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
        tipUchastnika = 8

#Если субъект Физлицо РФ или ИП, то отдельная собиралка
    if tipUchastnikaID == 6 or tipUchastnikaID == 5 or tipUchastnikaID == 7 or tipUchastnikaID == 8:
        startEruzNum = startEruzNum + 1
        startEruzNumString = str(startEruzNum)
        # os.remove("startEruzNum.txt")
        f = open("startEruzNum.txt", "w")
        f.write(startEruzNumString)
        f.close()
        continue

    if tipUchastnikaID == 3 or tipUchastnikaID == 2:
        print(soup.title.text)  # or string
        print(startEruzNumString)

        statusReg = soup.find("span", text="Статус регистрации").next_sibling.next_sibling.text
        print(statusReg)

        print(tipUchastnika)



        personINN = soup.find("span", text="ИНН").next_sibling.next_sibling.text.strip()
        print(personINN)

        bossFullName = soup.find("span", text="ФИО").next_sibling.next_sibling.text.title().strip()
        print(bossFullName)

        bossFullNameSplit = bossFullName.split()
        bossLastName = bossFullNameSplit[0]
        bossFirstName = bossFullNameSplit[1]

        try:
            bossSecondName = bossFullNameSplit[2]
        except:
            bossSecondName = ""

        print(bossFirstName, bossSecondName, bossLastName, personINN)

        try:
            OGRNIP = soup.find("span", text="ОГРНИП").next_sibling.next_sibling.text.strip()
            print(OGRNIP)
        except:
            OGRNIP = ""



        nalogCode = personINN[:4]
        nalogCodeZapasnoy = personINN[:2] + "00"
        nalogCodeZapasnoy1 = personINN[:2] + "01"
        nalogCodeZapasnoy2 = personINN[:2] + "02"
        print(nalogCode, nalogCodeZapasnoy)

        try:
            nalogRegDate = soup.find("span", text="Дата постановки на учет в налоговом органе").next_sibling.next_sibling.text.strip()
            print(nalogRegDate)
            ipRegDate = soup.find("span", text="Дата регистрации индивидуального предпринимателя").next_sibling.next_sibling.text.strip()
            print(ipRegDate)

        except:
            nalogRegDate = ""
            ipRegDate = ""





        companyEmail = soup.find("span", text="Адрес электронной почты").next_sibling.next_sibling.text.replace(" ", "")
        companyEmail = companyEmail.replace(" ", "")
        print(companyEmail)

        sql2 = "SELECT id FROM nalog_codes WHERE nalog_kod = %s"

        try:
            my_cursor.execute(sql2, (nalogCode,))
            nalogCodesID = my_cursor.fetchone()[0]
            # nalogInfo = my_cursor.fetchall()
            # for x in nalogInfo:
            #    print(x)
            print("Получен Id нaлоговой:", nalogCodesID)
        except AttributeError:
            my_cursor.execute(sql2, (nalogCodeZapasnoy,))
            nalogCodesID = my_cursor.fetchone()[0]
            print("Получен Id нaлоговой:", nalogCodesID)
        except AttributeError:
            my_cursor.execute(sql2, (nalogCodeZapasnoy1,))
            nalogCodesID = my_cursor.fetchone()[0]
            print("Получен Id нaлоговой:", nalogCodesID)
        except AttributeError:
            my_cursor.execute(sql2, (nalogCodeZapasnoy2,))
            nalogCodesID = my_cursor.fetchone()[0]
            print("Получен Id нaлоговой:", nalogCodesID)
        except:
            nalogCodesID = "1"


        thisBossExist = False
        try:
            sql4 = "SELECT id FROM boss_person WHERE full_name = %s AND boss_inn = %s"
            my_cursor.execute(sql4, (bossFullName, personINN))
            bossPersonID = my_cursor.fetchone()[0]
            print("Такой босс уже есть", bossPersonID)
            thisBossExist = True
        except AttributeError:
            sql4 = "SELECT id FROM boss_person WHERE full_name = %s AND email_1 = %s"
            my_cursor.execute(sql4, (bossFullName, companyEmail))
            bossPersonID = my_cursor.fetchone()[0]
            print("Такой босс уже есть", bossPersonID)
            thisBossExist = True
        except:
            bossPersonID = ""
            print("Такого босса еще не было", bossPersonID)
            thisBossExist = False

        if thisBossExist == False:
            try:
                sql3 = "INSERT INTO boss_person(boss_inn, full_name, f_name, s_name, l_name, email_1) values(%s, %s, %s, %s, %s, %s)"
                my_cursor.execute(sql3, (personINN, bossFullName, bossFirstName, bossSecondName, bossLastName, companyEmail))
                sql4 = "SELECT id FROM boss_person WHERE full_name = %s AND email_1 = %s"
                my_cursor.execute(sql4, (bossFullName, companyEmail))
                bossPersonID = my_cursor.fetchone()[0]
                print("Добавили персону под ID", bossPersonID)
            # except AttributeError:
            #     sql3 = "INSERT INTO boss_person(boss_inn, full_name, email_1) values(%s, %s, %s)"
            #     my_cursor.execute(sql3, (personINN, bossFullName, companyEmail))
            #     sql4 = "SELECT id FROM boss_person WHERE full_name = %s AND email_1 = %s"
            #     my_cursor.execute(sql4, (bossFullName, companyEmail))
            #     bossPersonID = my_cursor.fetchone()[0]
            #     print("Добавили персону под ID", bossPersonID)
            except:
                bossPersonID = ""
                print(Fore.RED + "Ошибка с ID босса")
                print(Style.RESET_ALL)

        if not bossPersonID:
            bossPersonID = 1

        zapisExistWithoutEruzNum = False
        eruzAlreadyRegistered = False

        try:
            sql8 = "SELECT id FROM eruz_member WHERE email_1 = %s AND eruz_member_inn = %s"
            my_cursor.execute(sql8, (eruzNum, personINN))
            eruzRegistryID = my_cursor.fetchone()[0]
            print("Запись существует в реестре без номера ЕРУЗ под Id=", eruzRegistryID)
            zapisExistWithoutEruzNum = True
        except:
            print("ЕРУЗ еще не был зарегистрирован")


        if zapisExistWithoutEruzNum == True:

            try:
                sql5 = "UPDATE eruz_member SET eruz_registry_id=%s, eruz_registry_date=% registry_date=%s, ip_reg_date=%s, ogrnip=%s, nalog_reg_date=%s, registry_status=%s, tip_uchastnika_id=%s, nalog_codes_id=%s, boss_person_id=%s WHERE email_1=%s AND eruz_member_inn=%s"
                my_cursor.execute(sql5, (
                eruzNum, dataReg, eruz_registry_date, ipRegDate, OGRNIP, nalogRegDate, statusReg, tipUchastnikaID, nalogCodesID,
                bossPersonID, companyEmail, personINN))
                sql5 = "SELECT id FROM eruz_member WHERE eruz_registry_id = %s"
                my_cursor.execute(sql5, (eruzNum,))
                eruzRegistryID = my_cursor.fetchone()[0]

                print("Запись обновлена свежими данными")
                zapisExist = True
                eruzAlreadyRegistered = True
            except:
                print("Что-то пошло не так с обновление ранее существующей записи ИП или физлица")




        if eruzAlreadyRegistered == False:

            try:
                sql = "INSERT INTO eruz_member(eruz_registry_id, eruz_member_inn, ip_reg_date, eruz_registry_date, ogrnip, nalog_reg_date, company_email, registry_status, tip_uchastnika_id, nalog_codes_id, boss_person_id) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                my_cursor.execute(sql, (
                    eruzNum, personINN, ipRegDate, eruz_registry_date, OGRNIP, nalogRegDate, companyEmail, statusReg, int(tipUchastnikaID),
                    nalogCodesID, bossPersonID))

                sql8 = "SELECT id FROM eruz_member WHERE eruz_registry_id = %s"
                my_cursor.execute(sql8, (eruzNum,))
                eruzRegistryID = my_cursor.fetchone()[0]

                if tipUchastnikaID == 3:
                    print("Запись индивидуального предпринимателя успешно занесена в реестр под Id=", eruzRegistryID)
                else:
                    print("Запись физического лица РФ успешно занесена в реестр под Id=", eruzRegistryID)
            except:
                print("Что-то пошло не так с добавление записи ЕРУЗ нового ИП или физлица")







        #mydb.commit()



        startEruzNum = startEruzNum + 1
        startEruzNumString = str(startEruzNum)
        # os.remove("startEruzNum.txt")
        f = open("startEruzNum.txt", "w")
        f.write(startEruzNumString)
        f.close()
        continue



    if tipUchastnikaID == 4:
        print(soup.title.text)  # or string
        print(startEruzNumString)

        statusReg = soup.find("span", text="Статус регистрации").next_sibling.next_sibling.text
        print(statusReg)

        print(tipUchastnika)
        #
        # dataReg = soup.find("span", text="Дата регистрации в ЕИС").next_sibling.next_sibling.text
        # print(dataReg)

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

        companyCountry = soup.find("span", text="Страна или территория регистрации (инкорпорации)").next_sibling.next_sibling.text
        print(companyCountry)

        companyAddress = soup.find("span", text="Адрес в пределах места нахождения").next_sibling.next_sibling.text
        print(companyAddress)

        foreignINN = soup.find("span", string=re.compile("^\d{6,12}$")).text
        print(foreignINN)

        # foreignINN = soup.find_all("span", class_="section__info", string_=re.compile("^\d{6,12}$"))
        # print(foreignINN[1])


        try:
            bossFullName = soup.find("td", class_="tableBlock__col").text.title()

            bossFullNameSplit = bossFullName.split()
            bossLastName = bossFullNameSplit[0]
            bossFirstName = bossFullNameSplit[1]




            print(bossFirstName, bossSecondName, bossLastName)
        except:
            bossFullNameSplit = ""
            bossLastName = ""
            bossFirstName = ""
            bossSecondName = ""

            bossFullName = ""
            print("Данные о руководителе не опубликованы")

        try:
            bossSecondName = bossFullNameSplit[2]
        except:
            bossSecondName = ""

        try:
            bossTitle = soup.find("td", class_="tableBlock__col").next_sibling.next_sibling.text.title()
        except:
            bossTitle = ""

        try:
            personINN = soup.find("td", class_="tableBlock__col").next_sibling.next_sibling.next_sibling.next_sibling.text
        except:
            personINN = ""

        print(bossFirstName, bossSecondName, bossLastName, bossTitle, personINN)

        companyEmail = soup.find("span", text="Адрес электронной почты").next_sibling.next_sibling.text.replace(" ",
                                                                                                                "")
        companyEmail = companyEmail.replace(" ", "")
        print(companyEmail)

        try:
            companyPhone = soup.find("span", text="Контактный телефон").next_sibling.next_sibling.text.replace(" ", "")
            # companyPhone = soup.find("span", text="Контактный телефон").next_sibling.next_sibling.text.replace(" ", "")
            companyPhone = companyPhone.replace(" ", "")
            companyPhone = companyPhone.replace(")", "")
            companyPhone = companyPhone.replace("(", "")
            companyPhone = companyPhone.replace("-", "")
            companyPhone = companyPhone.replace("+", "")
            companyPhone = re.sub(r'^8', '7', companyPhone)
        except:
            companyPhone = ""

        # try:
        #     smallBusinessSubject = soup.find("span", text="Да").text.strip()
        #     print(smallBusinessSubject)
        #
        #     if smallBusinessSubject == "Да":
        #         smallBusinessSubject = 2
        #     else:
        #         smallBusinessSubject = 1
        # except AttributeError:
        #     smallBusinessSubject = 1

        thisBossExist = False

        try:
            sql4 = "SELECT id FROM boss_person WHERE full_name = %s AND email_1 = %s"
            my_cursor.execute(sql4, (bossFullName, companyEmail))
            bossPersonID = my_cursor.fetchone()[0]
            print("Такой босс существует:", bossPersonID)
            thisBossExist = True
        except:
            print("Такого босса еще не было")

        if thisBossExist == False:
            try:
                sql3 = "INSERT INTO boss_person(boss_inn, full_name, f_name, s_name, l_name, phone_1, email_1) values(%s, %s, %s, %s, %s, %s, %s)"
                my_cursor.execute(sql3, (
                personINN, bossFullName, bossFirstName, bossSecondName, bossLastName, companyPhone, companyEmail))
                sql4 = "SELECT id FROM boss_person WHERE full_name = %s AND email_1 = %s"
                my_cursor.execute(sql4, (bossFullName, companyEmail))
                bossPersonID = my_cursor.fetchone()[0]
                print(bossPersonID)
            except:
                bossPersonID = ""
                print("Ошибка с ID босса")

        if not bossPersonID:
            bossPersonID = 1

        eruzAlreadyRegistered = False

        try:
            sql5 = "SELECT id FROM eruz_member WHERE eruz_registry_id = %s"
            my_cursor.execute(sql5, (eruzNum,))
            eruzRegistryID = my_cursor.fetchone()[0]
            print("Запись иностранного юридического лица уже существует Id=", eruzRegistryID)
            eruzAlreadyRegistered = True
        except:
            print("Запись юридического лица еще не существует")

        if eruzAlreadyRegistered == False:
            try:
                sql = "INSERT INTO eruz_member(full_company_name, short_company_name, registry_country, company_address, eruz_registry_id, foreign_inn, registry_date, company_email, registry_status, tip_uchastnika_id, boss_person_id) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                my_cursor.execute(sql, (
                fullCompanyName, shortCompanyName, companyCountry, companyAddress, eruzNum, foreignINN, dataReg,
                companyEmail, statusReg, int(tipUchastnikaID), bossPersonID))

                sql5 = "SELECT id FROM eruz_member WHERE eruz_registry_id = %s"
                my_cursor.execute(sql5, (eruzNum,))
                eruzRegistryID = my_cursor.fetchone()[0]
                print("Запись юридического лица иностранного государства успешно занесена в реестр под Id=", eruzRegistryID)
            except:
                pass



        #mydb.commit()

        startEruzNum = startEruzNum + 1
        startEruzNumString = str(startEruzNum)
        # os.remove("startEruzNum.txt")
        f = open("startEruzNum.txt", "w")
        f.write(startEruzNumString)
        f.close()
        continue


    print(soup.title.text) #or string

    print(startEruzNumString)

    statusReg = soup.find("span", text="Статус регистрации").next_sibling.next_sibling.text
    print(statusReg)

    print(tipUchastnika)

    # dataReg = soup.find("span", text="Дата регистрации в ЕИС").next_sibling.next_sibling.text
    # print(dataReg)

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
        nalogCodeZapasnoy1 = companyKPP[:2] + "01"
        nalogCodeZapasnoy2 = companyKPP[:2] + "02"
        print(nalogCode, nalogCodeZapasnoy)
    else:
        nalogCode = companyINN[:4]
        nalogCodeZapasnoy
        nalogCodeZapasnoy = companyINN[:2] + "00"
        nalogCodeZapasnoy1 = companyINN[:2] + "01"
        nalogCodeZapasnoy2 = companyINN[:2] + "02"
        print(nalogCode, nalogCodeZapasnoy)

    companyRegDate = soup.find("span", text="Дата постановки на учет в налоговом органе").next_sibling.next_sibling.text.strip()
    print(companyRegDate)



    companyOGRN = soup.find("span", text="ОГРН").next_sibling.next_sibling.text.strip()
    print(companyOGRN)

    nalogRegDate = soup.find("span", text="Дата постановки на учет в налоговом органе").next_sibling.next_sibling.text.strip()
    print(nalogRegDate)





    # try:
    #     smallBusinessSubject = soup.find("span", text="Да").text.strip()
    #     print(smallBusinessSubject)
    #
    #     if smallBusinessSubject == "Да":
    #         smallBusinessSubject = 2
    #     else:
    #         smallBusinessSubject = 1
    # except AttributeError:
    #     smallBusinessSubject = 1

    bossFullName = ""

    try:
        bossFullName = soup.find("td", class_="tableBlock__col").text.title()

        bossFullNameSplit = bossFullName.split()
        bossLastName = bossFullNameSplit[0]
        bossFirstName = bossFullNameSplit[1]



        print(bossFirstName, bossLastName)
    except AttributeError:
        bossFullNameSplit = ""
        bossLastName = ""
        bossFirstName = ""
        bossSecondName = ""

        bossFullName = ""

        print(Fore.RED + "Данные о руководителе не опубликованы")
        print(Style.RESET_ALL)

    try:
        bossSecondName = bossFullNameSplit[2]
        print(bossSecondName)
    except:
        bossSecondName = ""


    try:
        bossTitle = soup.find("td", class_="tableBlock__col").next_sibling.next_sibling.text.title()
        print(bossTitle)
    except:
        bossTitle = ""
        print("Нет названия должности")

    try:
        personINN = soup.find("td", class_="tableBlock__col").next_sibling.next_sibling.next_sibling.next_sibling.text
        print("ИНН руководителя", personINN)
    except:
        personINN = ""
        print("Нет ИНН руководителя")



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
    nalogCodesID = ""

    try:
        my_cursor.execute(sql2, (nalogCode,))
        nalogCodesID = my_cursor.fetchone()[0]
        #nalogInfo = my_cursor.fetchall()
        #for x in nalogInfo:
        #    print(x)
        print("Получен Id нaлоговой:", nalogCodesID)
    except AttributeError:
        my_cursor.execute(sql2, (nalogCodeZapasnoy,))
        nalogCodesID = my_cursor.fetchone()[0]
        print("Получен Id нaлоговой:", nalogCodesID)
    except AttributeError:
        my_cursor.execute(sql2, (nalogCodeZapasnoy1,))
        nalogCodesID = my_cursor.fetchone()[0]
        print("Получен Id нaлоговой:", nalogCodesID)
    except AttributeError:
        my_cursor.execute(sql2, (nalogCodeZapasnoy2,))
        nalogCodesID = my_cursor.fetchone()[0]
        print("Получен Id нaлоговой:", nalogCodesID)
    except:
        nalogCodesID = "1"

    thisBossExist = True
    if bossFullName:
        try:
            sql4 = "SELECT id FROM boss_person WHERE boss_inn = %s AND full_name = %s"
            my_cursor.execute(sql4, (personINN, bossFullName))
            bossPersonID = my_cursor.fetchone()[0]
            print("Такой босс уже есть", bossPersonID)
        except AttributeError:
            sql4 = "SELECT id FROM boss_person WHERE full_name = %s AND email_1 = %s "
            my_cursor.execute(sql4, (bossFullName, companyEmail))
            bossPersonID = my_cursor.fetchone()[0]
            print("Такой босс уже есть", bossPersonID)
        except:
            thisBossExist = False
            print("Этого босса в базе еще не было")


        if thisBossExist == False:
            try:
                sql3 = "INSERT INTO boss_person(boss_inn, full_name, f_name, s_name, l_name, phone_1, cellphone_1, email_1) values(%s, %s, %s, %s, %s, %s, %s, %s)"
                my_cursor.execute(sql3, (personINN, bossFullName, bossFirstName, bossSecondName, bossLastName, companyPhone, companyCell, companyEmail))
                sql4 = "SELECT id FROM boss_person WHERE full_name = %s AND email_1 = %s"
                my_cursor.execute(sql4, (bossFullName, companyEmail))
                bossPersonID = my_cursor.fetchone()[0]
                print("Внесен босс и получен ID босса =", bossPersonID)
            except AttributeError:
                sql3 = "INSERT INTO boss_person(full_name, phone_1, cellphone_1, email_1) values(%s, %s, %s, %s)"
                my_cursor.execute(sql3, (bossFullName, companyPhone, companyCell, companyEmail))
                sql4 = "SELECT id FROM boss_person WHERE full_name = %s AND email_1 = %s"
                my_cursor.execute(sql4, (bossFullName, companyEmail))
                bossPersonID = my_cursor.fetchone()[0]
                print("Внесен босс в укороченной версии и получен ID босса =", bossPersonID)
            except:
                bossPersonID = ""
                print(Fore.RED + "Ошибка с ID босса")
                print(Style.RESET_ALL)


    else:
        bossPersonID = ""

    if not bossPersonID:
        bossPersonID = 1

    doOkveds = True

    zapisExist = False


    zapisExistWithoutEruzNum = False
    if zapisExist == False:
        try:
            sql5 = "SELECT id FROM eruz_member WHERE email_1 = %s AND eruz_member_inn = %s"
            my_cursor.execute(sql5, (companyEmail, companyINN))
            eruzRegistryID = my_cursor.fetchone()[0]
            print("Запись существует в реестре без номера ЕРУЗ под Id=", eruzRegistryID)
            zapisExistWithoutEruzNum = True
        except:
            print("Запись еще не заносилась даже в неполном виде")


    if zapisExistWithoutEruzNum == True:
        try:
            sql5 = "UPDATE eruz_member SET full_company_name=%s, short_company_name=%s, eruz_registry_id=%s, eruz_member_inn=%s, registry_date=%s, eruz_registry_date=%s, ogrn=%s, nalog_reg_date=%s, company_phone=%s, company_cell=%s, company_address=%s, company_kpp=%s, company_site=%s, registry_status=%s, tip_uchastnika_id=%s, nalog_codes_id=%s, boss_person_id=%s, WHERE email_1 = %s"
            my_cursor.execute(sql5, (fullCompanyName, shortCompanyName, eruzNum, companyINN, companyRegDate, eruz_registry_date, companyOGRN, nalogRegDate, companyPhone, companyCell, companyAddress, companyKPP, companySite, statusReg, tipUchastnikaID, nalogCodesID, bossPersonID, companyEmail))
            sql5 = "SELECT id FROM eruz_member WHERE eruz_registry_id = %s"
            my_cursor.execute(sql5, (eruzNum,))
            eruzRegistryID = my_cursor.fetchone()[0]
            doOkveds = True
            print("Запись существует в реестре без номера ЕРУЗ под Id=", eruzRegistryID, "Запись обновлена свежими данными")
            zapisExist = True
        except:
            print("Пробовали обновить ранее существуюущую запись, но что-то пошло не так")



    if zapisExist == False:
        try:
            sql = "INSERT INTO eruz_member(full_company_name, short_company_name, eruz_registry_id, eruz_member_inn, registry_date, eruz_registry_date, ogrn, nalog_reg_date, company_email, company_phone, company_cell, company_address, company_kpp, company_site, registry_status, tip_uchastnika_id, nalog_codes_id, boss_person_id) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            my_cursor.execute(sql, (
            fullCompanyName, shortCompanyName, eruzNum, companyINN, companyRegDate, eruz_registry_date, companyOGRN, nalogRegDate,
            companyEmail, companyPhone, companyCell, companyAddress, companyKPP, companySite, statusReg,
            int(tipUchastnikaID), nalogCodesID, bossPersonID))
            sql5 = "SELECT id FROM eruz_member WHERE eruz_registry_id = %s"
            my_cursor.execute(sql5, (eruzNum,))
            eruzRegistryID = my_cursor.fetchone()[0]
            print("Запись занесена в реестр под Id=", eruzRegistryID)
            zapisExist = True
        except:
            eruzRegistryID = "0"
            doOkveds = False

            print(Fore.RED + "Запись не занесена в реестр")
            print(Style.RESET_ALL)







    startEruzNum = startEruzNum + 1
    startEruzNumString = str(startEruzNum)
    #os.remove("startEruzNum.txt")
    f = open("startEruzNum.txt", "w")
    f.write(startEruzNumString)
    f = open("startEruzNumBackup.txt", "w")
    f.write(startEruzNumString)
    f.close()

    GetMainOkved(eruzNum, zapisExist, companyINN, eruzRegistryID)

    if doOkveds == True:
        for singleOkved in companyOkveds.find_all("div"):
            singleOkved = singleOkved.text
            # singleOkvedSplit = singleOkved.split(".")
            # singleOkvedSubKod1 = int(singleOkvedSplit[0])
            # singleOkvedSubKod2 = int(singleOkvedSplit[1])
            # singleOkvedSubKod3 = int(singleOkvedSplit[2])
            # print(singleOkvedSubKod1, singleOkvedSubKod2,singleOkvedSubKod3)

            if singleOkved.endswith("0") and len(singleOkved) > 2:
                singleOkved = singleOkved[:-1]

            try:
                sql6 = "SELECT id FROM okved_2020 WHERE okved_code = %s"
                my_cursor.execute(sql6, (singleOkved,))
                okved2020ID = my_cursor.fetchone()[0]

                sql7 = "INSERT INTO eruz_member_okved_codes(gov_eruz_registry_id, okved_codes_id) values(%s, %s)"
                my_cursor.execute(sql7, (int(eruzRegistryID), okved2020ID))
            except AttributeError:
                sql6 = "SELECT id FROM okved_2020 WHERE okved_code = %s"
                singleOkvedZapasnoy = singleOkved[:2]
                my_cursor.execute(sql6, (singleOkvedZapasnoy,))
                okved2020ID = my_cursor.fetchone()[0]

                sql7 = "INSERT INTO eruz_member_okved_codes(gov_eruz_registry_id, okved_codes_id) values(%s, %s)"
                my_cursor.execute(sql7, (int(eruzRegistryID), okved2020ID))
            except:
                singleOkved = "ОКВЭД не существует"

            print(singleOkved)




    #mydb.commit()

    # startEruzNum = startEruzNum + 1
    # startEruzNumString = str(startEruzNum)
    # #os.remove("startEruzNum.txt")
    # f = open("startEruzNum.txt", "w")
    # f.write(startEruzNumString)
    # f = open("startEruzNumBackup.txt", "w")
    # f.write(startEruzNumString)
    # f.close()

