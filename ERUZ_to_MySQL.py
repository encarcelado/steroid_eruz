print("hello")

import bs4 as bs
import urllib.request

sauce = urllib.request.urlopen("https://zakupki.gov.ru/epz/eruz/card/general-information.html?revisionId=143760").read()
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

address = soup.find("td", text="ИНН")
print(address.next_sibling.next_sibling.text)

address = soup.find("td", text="Номер реестровой записи в ЕРУЗ")
print(address.next_sibling.next_sibling.text)

address = soup.find("td", text="Адрес электронной почты")
print(address.next_sibling.next_sibling.text)

address = soup.find(class_="odd")
print(address)
address2 = address.find_all("td")
print(address2[0].text)


#for match1 in match
 #   if "Номер" in match1.next:
 #       print(match1)
#print(match)
