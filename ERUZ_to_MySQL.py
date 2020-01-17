#print("hello2")

import bs4 as bs
import urllib.request

sauce = urllib.request.urlopen("https://zakupki.gov.ru/epz/eruz/card/general-information.html?reestrNumber=20008985").read()
content = sauce.decode("utf-8")

#print(content)

#soup = bs.BeautifulSoup(content, "html.parser")
soup = bs.BeautifulSoup(content, "lxml")
print(soup.title.text) #or string

#match = soup.find("td", class_="noticeTdFirst fontBoldTextTd").text
#match = soup.td.text[15]
#match = soup.find_all("td").text

#address = soup.find_all("td", class_="noticeTdFirst fontBoldTextTd")
#print(address[1].text)

#address = soup.find("td", class_="noticeTdFirst fontBoldTextTd")
#print(address.next_sibling.next_sibling.text)

eruzNum = soup.find("span", text="Номер реестровой записи в ЕРУЗ").next_sibling.next_sibling.text
print(eruzNum)


statusReg = soup.find("span", text="Статус регистрации").next_sibling.next_sibling.text
print(statusReg)

tipUchastnika = soup.find("span", text="Тип участника закупки").next_sibling.next_sibling.text
print(tipUchastnika)

dataReg = soup.find("span", text="Дата регистрации в ЕИС").next_sibling.next_sibling.text
print(dataReg)

fullCompanyName = soup.find("span", text="Полное наименование").next_sibling.next_sibling.text.title()
print(fullCompanyName)

shortCompanyName = soup.find("span", text="Сокращенное наименование").next_sibling.next_sibling.text
print(shortCompanyName)

companyAddress = soup.find("span", text="Адрес в пределах места нахождения").next_sibling.next_sibling.text.title()
print(companyAddress)

companyOkveds = soup.find("span", text="Код(ы) ОКВЭД").next_sibling.next_sibling


#singleOkved = companyOkveds2.find_all("div")

#print(singleOkved[0].text)

for singleOkved in companyOkveds.find_all("div"):
    print(singleOkved.text)




companyINN = soup.find("span", text="ИНН").next_sibling.next_sibling.text.strip()
print(companyINN)

companyKPP = soup.find("span", text="КПП").next_sibling.next_sibling.text.strip()
print(companyKPP)

companyRegDate = soup.find("span", text="Дата постановки на учет в налоговом органе").next_sibling.next_sibling.text.strip()
print(companyRegDate)

companyOGRN = soup.find("span", text="ОГРН").next_sibling.next_sibling.text.strip()
print(companyOGRN)

bossFullName = soup.find("td", class_="tableBlock__col").text.title()
bossTitle = soup.find("td", class_="tableBlock__col").next_sibling.next_sibling.text.title()
bossINN = soup.find("td", class_="tableBlock__col").next_sibling.next_sibling.next_sibling.next_sibling.text
print(bossFullName, bossTitle, bossINN)

companyEmail = soup.find("span", text="Адрес электронной почты").next_sibling.next_sibling.text.replace(" ", "")
print(companyEmail)

companyPhone = soup.find("span", text="Контактный телефон").next_sibling.next_sibling.text.replace(" ", "")
print(companyPhone)







#address = soup.find(class_="odd")
#print(address)
#address2 = address.find_all("td")
#print(address2[0].text)


#for match1 in match
 #   if "Номер" in match1.next:
 #       print(match1)
#print(match)
