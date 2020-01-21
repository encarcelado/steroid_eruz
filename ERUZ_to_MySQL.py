#скрипт забирает все данные ЕРУЗ и закидывает их в MySQL

import bs4 as bs
import urllib.request

startEruzNum = open('startEruzNum.txt', 'r').read()
startEruzNum = int(startEruzNum)
#print(startEruzNumFromText)
#startEruzNum = 19000001
endEruzNum = 19450000

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
        bossSecondName = bossFullNameSplit[2]

        print(bossFirstName, bossSecondName, bossLastName, personINN)

        OGRNIP = soup.find("span", text="ОГРНИП").next_sibling.next_sibling.text.strip()
        print(OGRNIP)

        nalogDate = soup.find("span", text="Дата постановки на учет в налоговом органе").next_sibling.next_sibling.text.strip()
        print(nalogDate)

        ipRegDate = soup.find("span", text="Дата регистрации индивидуального предпринимателя").next_sibling.next_sibling.text.strip()
        print(ipRegDate)

        companyEmail = soup.find("span", text="Адрес электронной почты").next_sibling.next_sibling.text.replace(" ", "")
        print(companyEmail)

        startEruzNum = startEruzNum + 1
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






    for singleOkved in companyOkveds.find_all("div"):
        print(singleOkved.text)

    #singleOkved2 = companyOkveds.find_all("div")
    #print("One Okved")
    #print(singleOkved2[1].text)




    companyINN = soup.find("span", text="ИНН").next_sibling.next_sibling.text.strip()
    print(companyINN)

    companyKPP = soup.find("span", text="КПП").next_sibling.next_sibling.text.strip()
    print(companyKPP)

    companyRegDate = soup.find("span", text="Дата постановки на учет в налоговом органе").next_sibling.next_sibling.text.strip()
    print(companyRegDate)

    companyOGRN = soup.find("span", text="ОГРН").next_sibling.next_sibling.text.strip()
    print(companyOGRN)

    bossFullName = soup.find("td", class_="tableBlock__col").text.title()

    bossFullNameSplit = bossFullName.split()
    bossLastName = bossFullNameSplit[0]
    bossFirstName = bossFullNameSplit[1]
    bossSecondName = bossFullNameSplit[2]




    bossTitle = soup.find("td", class_="tableBlock__col").next_sibling.next_sibling.text.title()
    personINN = soup.find("td", class_="tableBlock__col").next_sibling.next_sibling.next_sibling.next_sibling.text
    print(bossFirstName, bossSecondName, bossLastName, bossTitle, personINN)

    companyEmail = soup.find("span", text="Адрес электронной почты").next_sibling.next_sibling.text.replace(" ", "")
    print(companyEmail)

    companyPhone = soup.find("span", text="Контактный телефон").next_sibling.next_sibling.text.replace(" ", "")
    print(companyPhone)


    try:
        companySite = soup.find("span", text="Адрес сайта в сети интернет").next_sibling.next_sibling.text.replace(" ", "")
        print(companySite)
    except AttributeError:
        companySite = ""
        print("Название сайта не опубликовано")


    startEruzNum = startEruzNum + 1




