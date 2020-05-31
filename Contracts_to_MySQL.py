#скрипт забирает все данные ЕРУЗ и закидывает их в MySQL

import bs4 as bs
import codecs
import ftplib
import mysql.connector
import os
import re
import shutil
import sys
import time

import requests
import zipfile
from fake_useragent import UserAgent

from datetime import date

ua = UserAgent() #MAKES FAKE BROWSER HEADERS WHEN REQUESTING CONTRACTS FROM ZAKUPKI.GOV.RU


today = date.today()
d1 = today.strftime("%d.%m.%Y")
print("Сегодня:", d1)
d1 = str(d1)

# headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
# SINGLE FAKE BROWSER HEADER JUST IN CASE

mydb = mysql.connector.connect(host="v0434826.beget.tech", user="v0434826_eruz", passwd="1560ford", database = "v0434826_eruz")
mydb.autocommit = True

print(mydb)

if mydb:
    print("Connection is successful")


else:
    print("Connection is unsuccessful")

my_cursor = mydb.cursor(buffered=True)




ftp = ftplib.FTP("ftp.zakupki.gov.ru")
ftp.login("free", "free")
print(ftp.getwelcome())

region_list = open('region_list.txt', 'r')
region_names = region_list.readlines()
regexp = re.compile(r"^contract")
region_list.close()
# contractNumRE = re.compile(r"\d{11}")

for region_name in region_names:
    region_name = region_name.strip()
    print("Начинается загрузка контрактов для региона:", region_name)
    ftpFolder = "/fcs_regions/" + region_name + "/contracts/"
    ftp.cwd(ftpFolder)
    xml_contracts = ftp.nlst()
    for xml_contract in xml_contracts:
        if regexp.search(xml_contract):
            # здесь надо проверить, не обрабатывался ли файл архива раньше
            baseDirContracts = "contracts"
            fileNameXMLzips = region_name + "_xmlzips.txt"
            addXMLzip = xml_contract + "\n"
            xmlZipsFile = open(os.path.join(baseDirContracts, fileNameXMLzips), "a+", encoding="utf-8")
            # if xml_contract in xmlZipsFile:
            # xmlZipsFileString = xmlZipsFile.read()
            # if xmlZipsFileString.find(xml_contract) >= 0:
            #     xmlZipsFile.close()
            #     # print("Этот архив с xml уже обрабатывался:", xml_contract)
            #     print(Fore.RED + "Этот архив с xml уже обрабатывался:" + xml_contract)
            #     print(Style.RESET_ALL)
            #     continue
            alreadyWorked = False
            with open(os.path.join(baseDirContracts, fileNameXMLzips), "r") as myfile:
                data = myfile.readlines()
                for line in data:
                    if xml_contract in line:
                        xmlZipsFile.close()
                        print("Этот архив с xml уже обрабатывался:" + xml_contract)

                        alreadyWorked = True
                        break

            if alreadyWorked:
                # print("Already worked")
                continue
            print(xml_contract)
            #END здесь надо проверить, не обрабатывался ли файл архива раньше

            #DOWNLOADS FTP ARCHIVE
            with open(xml_contract, 'wb') as f:
                try:
                    ftp.retrbinary('RETR ' + xml_contract, f.write)
                except:
                    print("ftp.retr на сработал")
                    continue

            fileSize = os.stat(xml_contract)
            fileSize = fileSize.st_size
            print(fileSize)
            dirName = xml_contract.strip(".xml.zip")
            contract = "contracts"
            try:
                shutil.rmtree(dirName)
            except:
                print("Папку создали")

            try:
                os.remove(unzipped_contract_list.txt)
            except:
                print("Создали пустой файл для выгрузки названий файлов из архива")

            try:
                os.mkdir(dirName)
            except:
                print("Директория существует для xml")



            contractDirName = "contracts/" + dirName

            try:
                os.mkdir(contractDirName)
            except:
                print("Директория существует для контрактов")


            if fileSize > 0:
                print("Начинаем распаковку файла", xml_contract)

                with zipfile.ZipFile(xml_contract, 'r') as zip_ref:
                    zip_ref.extractall(dirName)
                    #time.sleep(20)

                print("Далаем список из распакованных файлов")

                with open("unzipped_contract_list.txt", "w") as a:
                    for path, subdirs, files in os.walk(dirName):
                        for filename in files:
                            f = os.path.join(path, filename)
                            #a.write(str(f) + os.linesep)
                            a.write(str(f) + "\n")
                print("Готов список из распаковынных файлов")
# TAKES CONTRACT NUMS VIA FILE NAME REGEX
                unzipped_contract_list = open('unzipped_contract_list.txt')
                unzipped_contracts = unzipped_contract_list.readlines()
                for unzipped_contract_path in unzipped_contracts:
                    unzipped_contract_path = unzipped_contract_path.strip()
                    if unzipped_contract_path.endswith("xml"):
                        print("Here's a single contract link:", unzipped_contract_path, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
                        # print(fore.LIGHT_BLUE + back.RED + style.BOLD + "Here's a single contract link:" + unzipped_contract_path + style.RESET)
                        contractNum = re.findall(r"\d{19}", unzipped_contract_path)
                        contractNum = contractNum[0]

                        # HERE NEEDS TO CHECK IF THE FILE WAS ALREADY PROCESSED - CONTINUE IF SO
                        baseDirContracts = "contracts"
                        fileNameContractNums = region_name + "_contracts.txt"
                        addContractNum = contractNum + "\n"
                        contractNumsFile = open(os.path.join(contract, dirName, fileNameContractNums), "a+", encoding="utf-8")
                        # if contractNum in contractNumsFile:
                        contractNumsFileString = contractNumsFile.read()
                        # if contractNumsFileString.find(contractNum) >= 0:
                        #     contractNumsFile.close()
                        #     # print("Этот контракт уже обрабатывался:", contractNum)
                        #     print(Fore.RED + "Этот контракт уже обрабатывался:", contractNum)
                        #     print(Style.RESET_ALL)
                        #     continue

                        alreadyWorked = False
                        with open(os.path.join(contract, dirName, fileNameContractNums), "r") as myfile:
                            data = myfile.readlines()
                            for line in data:
                                if contractNum in line:
                                    contractNumsFile.close()
                                    print("Этот контракт уже обрабатывался:" + contractNum)

                                    alreadyWorked = True
                                    break

                        if alreadyWorked == True:
                            # print("Контракт уже обработан")
                            continue

                        print("Номер карточки контракта: " + contractNum + " Начинаем обработку")


# OPENS CONTRACT ON ZAKUPKI.GOV.RU AND SCRAPES ALL DATA
                        response = ""
                        contractCard = "https://zakupki.gov.ru/epz/contract/contractCard/common-info.html?reestrNumber=" + contractNum
                        try:
                            headers = {'User-Agent': str(ua.random)}
                            # print(headers)
                            #headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
                            response = requests.get(contractCard, headers=headers, timeout=5) #здесь отсылается фейковый хедер, чтобы сервер думал, что с ним имеет дело реальный браузер
                            # print(response.content)
                            # sauce = urllib.request.urlopen(contractCard, timeout=100).read()
                            # sauce = urllib.request.urlopen(contractCard, timeout=4).read()
                            # print(sauce)
                            # time.sleep(2)
                            print("С первого раза забрали карточку контракта " + contractCard)
                        except requests.exceptions.Timeout:
                            # headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
                            headers = {'User-Agent': str(ua.random)}
                            time.sleep(2)
                            response = requests.get(contractCard, headers=headers, timeout=5)
                            # sauce = urllib.request.urlopen(contractCard, timeout=20).read()
                            # sauce = urllib.request.urlopen(contractCard).read()
                            print("Со второго раза забрали карточку контракта " + contractCard)
                        except:
                            print("Не прочитался " + contractCard + "*****************************************************")
                            continue

                        if response.ok: #OK WORKS FOR REQUESTS TO SHOW THE RESULT IS 200S OR 300S, NOT 400S
                            try:
                                s = response.content
                                soup = bs.BeautifulSoup(s, "lxml")
                            except:
                                continue


                        try:
                            status_kontrakta = soup.find("span", text="Статус контракта").next_sibling.next_sibling.text.strip()
                            print("Статус контракта:", status_kontrakta)
                        except:
                            status_kontrakta = ""

                        try:
                            zakupka_num = soup.find("span", text="Номер извещения об осуществлении закупки").next_sibling.next_sibling.text.strip()
                            print("Номер извещения об осуществлении закупки:", zakupka_num)
                        except:
                            zakupka_num = ""

                        try:
                            ikz = soup.find("span", text="Идентификационный код закупки (ИКЗ)").next_sibling.next_sibling.text.strip()
                            print("Идентификационный код закупки (ИКЗ):", ikz)
                        except:
                            ikz = ""

                        try:
                            price_kontrakta = soup.find("span", text="Цена контракта").next_sibling.next_sibling.text.strip()
                            price_kontrakta = price_kontrakta[:-4]
                            price_kontrakta = price_kontrakta.rstrip()
                            print("Цена контракта:", price_kontrakta)
                        except:
                            price_kontrakta = ""

                        try:
                            data_zakl_kontrakta = soup.find("span",
                                                            text="Дата заключения контракта").next_sibling.next_sibling.text.strip()
                            print("Дата заключения контракта:", data_zakl_kontrakta)
                        except:
                            data_zakl_kontrakta = ""

                        try:
                            data_ispol_kontrakta = soup.find("span",
                                                            text="Дата начала исполнения контракта").next_sibling.next_sibling.text.strip()
                            print("Дата начала исполнения контракта:", data_ispol_kontrakta)
                        except:
                            data_ispol_kontrakta = ""

                        try:
                            data_end_kontrakta = soup.find("span",
                                                            text="Дата окончания исполнения контракта").next_sibling.next_sibling.text.strip()
                            print("Дата окончания исполнения контракта:", data_end_kontrakta)
                        except:
                            data_end_kontrakta = ""

                        zakupka_link = ""
                        try:
                            zakupka_link = soup.find("a", string="Закупка")['href']
                            if zakupka_link.find("null") >= 0:
                                zakupka_link = ""
                            if zakupka_link.find("https://zakupki.gov.ru") < 0 and zakupka_link > 0:
                                zakupka_link = "https://zakupki.gov.ru" + zakupka_link
                            print(zakupka_link)
                        except:
                            zakupka_link = ""

                        zakazchik_link = ""
                        try:
                            zakazchik_link = soup.find("a", string="Заказчик")['href']
                            if zakazchik_link.find("https://zakupki.gov.ru") < 0:
                                zakazchik_link = "https://zakupki.gov.ru" + zakazchik_link

                            print(zakazchik_link)
                        except:
                            zakazchik_link = ""

                        #SCRAPES ALL DATA ABOUT ZAKAZCHIK
                        try:
                            full_name_zakazchika = soup.find("span", text="Полное наименование заказчика").next_sibling.next_sibling.text.strip()
                            print("Полное наименование заказчика:", full_name_zakazchika)
                        except:
                            full_name_zakazchika = ""

                        try:
                            short_name_zakazchika = soup.find("span", text="Сокращенное наименование заказчика").next_sibling.next_sibling.text.strip()
                            print("Сокращенное наименование заказчика:", short_name_zakazchika)
                        except:
                            short_name_zakazchika = ""

                        try:
                            date_uchet_zakazchika = soup.find("span", text="Дата постановки на учет в налоговом органе").next_sibling.next_sibling.text.strip()
                            print("Дата постановки на учет в налоговом органе:", date_uchet_zakazchika)
                        except:
                            date_uchet_zakazchika = ""

                        try:
                            id_zakazchika = soup.find("span", text="Идентификационный код заказчика").next_sibling.next_sibling.text.strip()
                            print("Идентификационный код заказчика:", id_zakazchika)
                        except:
                            id_zakazchika = ""

                        try:
                            inn_zakazchika = soup.find("span", text="ИНН").next_sibling.next_sibling.text.strip()
                            print("ИНН заказчика:", inn_zakazchika)
                        except:
                            inn_zakazchika = ""

                        try:
                            kpp_zakazchika = soup.find("span", text="КПП").next_sibling.next_sibling.text.strip()
                            print("КПП заказчика:", kpp_zakazchika)
                        except:
                            kpp_zakazchika = ""

                        try:
                            kod_opf_zakazchika = soup.find("span", text="Код организационно-правовой формы").next_sibling.next_sibling.text.strip()
                            print("Код организационно-правовой формы:", kod_opf_zakazchika)
                        except:
                            kod_opf_zakazchika = ""

                        try:
                            kod_okpo_zakazchika = soup.find("span", text="Код ОКПО").next_sibling.next_sibling.text.strip()
                            print("Код ОКПО:", kod_okpo_zakazchika)
                        except:
                            kod_okpo_zakazchika = ""

                        try:
                            kod_ter_zakazchika = soup.find("span", text="Код территории муниципального образования").next_sibling.next_sibling.text.strip()
                            print("Код территории муниципального образования:", kod_ter_zakazchika)
                        except:
                            kod_ter_zakazchika = ""

                        #SCRAPES ALL DATA ABOUT CONTRACTOR

                        try:
                            contractor_table = soup.find("table", class_="blockInfo__table tableBlock grayBorderBottom")
                            #print("Данные подрядчика:", contractor_table)
                        except:
                            contractor_table = ""

                        if contractor_table:
                            try:
                                contractor_name = contractor_table.find("td", class_="tableBlock__col tableBlock__col_first").text.rstrip().strip()

                                contractor_name = re.findall(r'.*\n', contractor_name)
                                contractor_name = contractor_name[0].rstrip()
                                print("Название фирмы подрядчика:", contractor_name)
                            except:
                                contractor_name = ""

                            try:
                                contractor_okpo = contractor_table.find("span", class_="section__title", string="Код по ОКПО:").next_sibling.next_sibling.text.strip()
                                if contractor_okpo:
                                    print("ОКПО подрядчика:", contractor_okpo)
                            except:
                                contractor_okpo = ""

                            try:
                                contractor_inn = contractor_table.find("span", class_="section__title", string="ИНН:").next_sibling.next_sibling.text.strip()
                                print("ИНН подрядчика:", contractor_inn)
                            except:
                                contractor_inn = ""

                            nalogCodesID = "1"
                            if contractor_inn:
                                nalogCode = contractor_inn[:4]
                                nalogCodeZapasnoy = contractor_inn[:2] + "00"
                                nalogCodeZapasnoy1 = contractor_inn[:2] + "01"
                                nalogCodeZapasnoy2 = contractor_inn[:2] + "02"
                                print(nalogCode, nalogCodeZapasnoy)

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

                            try:
                                contractor_kpp = contractor_table.find("span",
                                                                        class_="section__title", string="КПП, дата постановки на учет:").next_sibling.next_sibling.text.strip()
                                contractor_kpp = re.findall(r'\d{7,9}', contractor_kpp)
                                contractor_kpp = contractor_kpp[0].strip()
                                print("КПП подрядчика:", contractor_kpp)
                            except:
                                contractor_kpp = ""

                            try:
                                contractor_address = contractor_table.find("td",
                                                                        class_="tableBlock__col", string=re.compile("\d{6},")).text.strip()
                                print("Адрес подрядчика:", contractor_address)
                            except:
                                contractor_address = ""

                            # try:
                            #     contractor_phone_email = contractor_table.find("td", class_="tableBlock__col", string=re.compile(".*7-.*")).text
                            #
                            #     print("Телефон и email подрядчика:", contractor_phone_email)
                            # except:
                            #     contractor_phone_email = ""
                            #     print("Телефон и email подрядчика не определились!")
                            contractor_phone_email = ""
                            contractor_phone = ""
                            contractor_email = ""
                            contractor_cell = ""
                            try:
                                for contractor_phone_email_try in contractor_table.findAll("td", class_="tableBlock__col"):
                                    contractor_phone_email_try = contractor_phone_email_try.text.strip().rstrip()
                                    print("Телефон/e-mail: ", contractor_phone_email_try)

                                    # contractor_phone_email = re.findall(r'7-', contractor_phone_email_try)
                                    # contractor_phone_email = contractor_phone_email[0]
                                    if contractor_phone_email_try.find("@") >= 0 or contractor_phone_email_try.find("7-") == 0 or contractor_phone_email_try.find("8-") == 0 or contractor_phone_email_try.find("7 ") == 0 or contractor_phone_email_try.find("8 ") == 0 or contractor_phone_email_try.find("7(") == 0 or contractor_phone_email_try.find("8(") == 0 or contractor_phone_email_try.find("+") == 0 or contractor_phone_email_try.find("9") == 0:
                                        contractor_phone_email = contractor_phone_email_try
                                        #print("Телефон и email подрядчика:", contractor_phone_email)
                                        contractor_phone_email = contractor_phone_email.splitlines()
                                        #contractor_phone = contractor_phone_email[0].strip()
                                        #contractor_email = contractor_phone_email[1].strip()
                                        #for email in contractor_phone_email:
                                        #    if email.find("@") >= 0:
                                          #      contractor_email = email.strip()
                                          #  else:
                                            #    contractor_phone = email.strip()
										if "@" in contractor_phone_email[0]:
											contractor_email = contractor_phone_email[0].strip()
										else:
											contractor_phone = contractor_phone_email[0].strip()
										# print("Тел" + contractor_phone)

										try:
											# print(contractor_phone_email[1])
											# print("stop2")
											if "@" in contractor_phone_email[1]:
												contractor_email = contractor_phone_email[1].strip()
											else:
												contractor_phone = contractor_phone_email[1].strip()
										except:
											pass
										if contractor_phone:
											contractor_phone = contractor_phone.replace(" ", "")
											contractor_phone = contractor_phone.replace(")", "")
											contractor_phone = contractor_phone.replace("(", "")
											contractor_phone = contractor_phone.replace("-", "")
											contractor_phone = contractor_phone.replace("+", "")
											contractor_phone = re.sub(r'^8', '7',  contractor_phone)
											contractor_phone = re.sub(r'^9', '79', contractor_phone)
											#print("Телефон подрядчика:", contractor_phone)
											contractor_cell = re.match("^79\d*", contractor_phone)

                                        if contractor_cell:
                                            contractor_cell = contractor_phone
                                            contractor_phone = ""
                                            print("Сотовый телефон подрядчика", contractor_cell)
                                        else:
                                            print("Офисный телефон подрядчика", contractor_phone)
                                            contractor_cell = ""
                                        print("Email подрядчика:", contractor_email)
                                        break
                            except:
                                contractor_phone_email = ""
                                contractor_phone = ""
                                contractor_email = ""
                                contractor_cell = ""
                                print("Телефон и email подрядчика не определились!")

                        #PUTS ALL DATA INTO ZAKUPKA_CARD TABLE

                        # sql5 = "SELECT id FROM zakupka_card WHERE zakupka_num = %s"
                        # my_cursor.execute(sql5, (zakupka_num,))
                        # zakupka_card_id = my_cursor.fetchone()[0]
                        # print("Закупка уже существует в реестре под Id=", zakupka_card_id)
                        # zakupkaAlreadyRegistered = True






                        zakupkaAlreadyRegistered = False
                        if zakupka_num:
                            try:
                                sql5 = "SELECT id FROM zakupka_card WHERE zakupka_num = %s"
                                my_cursor.execute(sql5, (zakupka_num,))
                                # zakupka_card_id = my_cursor.fetchone()[0]

                                zakupka_card_ids = my_cursor.fetchone()
                                for zakupka_card_id in zakupka_card_ids:
                                    print(zakupka_card_id)
                                print("Закупка уже существует в реестре под Id=", zakupka_card_id)
                                zakupkaAlreadyRegistered = True
                            except:
                                zakupka_card_id = ""
                                print("Это новая закупка. Начинаем заносить в базу.")

                            if zakupkaAlreadyRegistered == False:
                                try:
                                    sql3 = "INSERT INTO zakupka_card(zakupka_num, ikz, zakupka_link) VALUES(%s, %s, %s)"
                                    my_cursor.execute(sql3, (zakupka_num, ikz, zakupka_link))
                                    sql5 = "SELECT id FROM zakupka_card WHERE zakupka_num = %s"
                                    my_cursor.execute(sql5, (int(zakupka_num),))

                                    zakupka_card_ids = my_cursor.fetchone()
                                    for zakupka_card_id in zakupka_card_ids:
                                        print(zakupka_card_id)
                                    print("Закупка создана в реестре под Id=", zakupka_card_id)
                                except:
                                    zakupka_card_id = ""
                                    print("Закупка не создалась по какой-то причине")
                        else:
                            print("Номера закупки не было, поэтому не стали заносить в базу")
                            zakupka_card_id = ""



                        # PUTS ALL DATA INTO CONTRACT_CARD TABLE

                        # sql3 = "INSERT INTO contract_card(contract_num, data_end_kontrakta, data_ispol_kontrakta, data_zakl_kontrakta, price_kontrakta, status_kontrakta) values(%s, %s, %s, %s, %s, %s)"
                        # my_cursor.execute(sql3, (contractNum, data_end_kontrakta, data_ispol_kontrakta, data_zakl_kontrakta, price_kontrakta, status_kontrakta))
                        # print("Данные по контракту занесены в MySQL", contractNum)
                        # sql5 = "SELECT id FROM contract_card WHERE contract_num = %s"
                        # my_cursor.execute(sql5, (contractNum,))
                        # contract_card_id = my_cursor.fetchone()[0]
                        # print("Карточка контракта создана в реестре под Id=", contract_card_id)


                        contractCardAlreadyRegistered = False
                        try:
                            sql5 = "SELECT id FROM contract_card WHERE contract_num = %s"
                            my_cursor.execute(sql5, (contractNum,))
                            # contract_card_id = my_cursor.fetchone()[0]
                            contract_card_ids = my_cursor.fetchone()
                            for contract_card_id in contract_card_ids:
                                print(contract_card_id)
                            print("Карточка контракта уже существует в реестре под Id=", contract_card_id)
                            contractCardAlreadyRegistered = True
                        except:
                            print("Это новая карточка контракта. Начинаем заносить в базу.")

                        if contractCardAlreadyRegistered == False:
                            try:
                                sql3 = "INSERT INTO contract_card(contract_num, data_end_kontrakta, data_ispol_kontrakta, data_zakl_kontrakta, price_kontrakta, status_kontrakta) VALUES(%s, %s, %s, %s, %s, %s)"
                                my_cursor.execute(sql3, (
                                contractNum, data_end_kontrakta, data_ispol_kontrakta, data_zakl_kontrakta,
                                price_kontrakta, status_kontrakta))
                                print("Данные по контракту занесены в MySQL", contractNum)
                                sql5 = "SELECT id FROM contract_card WHERE contract_num = %s"
                                my_cursor.execute(sql5, (contractNum,))
                                # contract_card_id = my_cursor.fetchone()[0]
                                contract_card_ids = my_cursor.fetchone()
                                for contract_card_id in contract_card_ids:
                                    print(contract_card_id)
                                print("Карточка контракта создана в реестре под Id=", contract_card_id)
                            except:
                                print("Карточка контракта не создалась по какой-то причине")



                        # PUTS ALL DATA INTO ZAKAZCHIK CARD TABLE

                        # sql3 = "INSERT INTO zakazchik_card(zakazchik_link, full_name_zakazchika, short_name_zakazchika, date_uchet_zakazchika, id_zakazchika, inn_zakazchika, kpp_zakazchika, kod_opf_zakazchika, kod_okpo_zakazchika, kod_ter_zakazchika) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                        # my_cursor.execute(sql3, (
                        # zakazchik_link, full_name_zakazchika, short_name_zakazchika, date_uchet_zakazchika,
                        # id_zakazchika, inn_zakazchika, kpp_zakazchika, kod_opf_zakazchika, kod_okpo_zakazchika,
                        # kod_ter_zakazchika))
                        # sql5 = "SELECT id FROM zakazchik_card WHERE inn_zakazchika = %s"
                        # my_cursor.execute(sql5, (inn_zakazchika,))
                        # zakazchik_card_id = my_cursor.fetchone()[0]
                        # print("Карточка заказчика создана в реестре под Id=", zakazchik_card_id)

                        if inn_zakazchika:
                            zakazchikCardAlreadyRegistered = False
                            try:
                                sql5 = "SELECT id FROM zakazchik_card WHERE inn_zakazchika = %s"
                                my_cursor.execute(sql5, (inn_zakazchika,))
                                # zakazchik_card_id = my_cursor.fetchone()[0]
                                zakazchik_card_id = my_cursor.fetchone()
                                for zakazchik_card_id in zakazchik_card_ids:
                                    print(zakazchik_card_id)
                                print("Карточка заказчика уже существует в реестре под Id=", zakazchik_card_id)
                                zakazchikCardAlreadyRegistered = True
                            except:
                                print("Это новая карточка заказчика. Начинаем заносить в базу.")

                            if zakazchikCardAlreadyRegistered == False:
                                try:
                                    sql3 = "INSERT INTO zakazchik_card(zakazchik_link, full_name_zakazchika, short_name_zakazchika, date_uchet_zakazchika, id_zakazchika, inn_zakazchika, kpp_zakazchika, kod_opf_zakazchika, kod_okpo_zakazchika, kod_ter_zakazchika) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                                    my_cursor.execute(sql3, (zakazchik_link, full_name_zakazchika, short_name_zakazchika, date_uchet_zakazchika, id_zakazchika, inn_zakazchika, kpp_zakazchika, kod_opf_zakazchika, kod_okpo_zakazchika, kod_ter_zakazchika))
                                    sql5 = "SELECT id FROM zakazchik_card WHERE inn_zakazchika = %s"
                                    my_cursor.execute(sql5, (inn_zakazchika,))
                                    # zakazchik_card_id = my_cursor.fetchone()[0]
                                    zakazchik_card_ids = my_cursor.fetchone()
                                    for zakazchik_card_id in zakazchik_card_ids:
                                        print(zakazchik_card_id)
                                    print("Карточка заказчика создана в реестре под Id=", zakazchik_card_id)
                                except:
                                    print("Карточка заказчика не создалась по какой-то причине")
                        else:
                            zakazchik_card_id = ""
                            print("Карточка заказчика не создана, так-как нет ИНН заказчика")


                        # PUTS ALL DATA INTO ERUZ_MEMBER TABLE
                        eruz_member_id = ""
                        eruzAlreadyRegistered = False
                        if contractor_inn:
                            try:
                                sql5 = "SELECT id FROM eruz_member WHERE eruz_member_inn = %s"
                                my_cursor.execute(sql5, (contractor_inn,))
                                # eruz_member_id = my_cursor.fetchone()[0]
                                eruz_member_ids = my_cursor.fetchone()
                                for eruz_member_id in eruz_member_ids:
                                    print(eruz_member_id)
                                print("Подрядчик уже существует в качесте члена ЕРУЗ под Id=", eruz_member_id)
                                eruzAlreadyRegistered = True
                            except:
                                print("Этот подрядчик в ЕРУЗ еще не занесен.")
                        cellAlreadyExist = False
                        cellFromEruz = ""
                        if eruzAlreadyRegistered:
                            try:
                                sql5 = "SELECT company_cell FROM eruz_member WHERE eruz_member_inn = %s"
                                my_cursor.execute(sql5, (contractor_inn,))
                                cellFromEruz = my_cursor.fetchone()[0]
                                if cellFromEruz.startswith("97"):
                                    print("Сотовый телефон уже есть =", cellFromEruz)
                                    cellAlreadyExist = True
                                else:
                                    print("Сотового номера нет")
                                    cellAlreadyExist = False
                            except:
                                print("Этот подрядчик в ЕРУЗ еще не занесен.")

                        if cellFromEruz != contractor_cell and cellFromEruz.startswith("79") and eruzAlreadyRegistered and contractor_cell.startswith("79"):
                            try:
                                sql5 = "UPDATE eruz_member SET company_cell2 = %s  WHERE eruz_member_inn = %s"
                                my_cursor.execute(sql5, (contractor_cell, contractor_inn))
                            except:
                                print("Что-то пошло не так и второй сотовый добавлен не был")

                        if eruzAlreadyRegistered == False:
                            try:
                                sql = "INSERT INTO eruz_member(eruz_member_inn, full_company_name, company_kpp, company_address, company_phone, company_cell, company_email, nalog_codes_id) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
                                my_cursor.execute(sql, (
                                    contractor_inn, contractor_name, contractor_kpp, contractor_address, contractor_phone, contractor_cell, contractor_email, nalogCodesID,))

                                sql8 = "SELECT id FROM eruz_member WHERE eruz_member_inn = %s"
                                my_cursor.execute(sql8, (contractor_inn,))
                                # eruzRegistryID = my_cursor.fetchone()[0]
                                eruzRegistryIDs = my_cursor.fetchone()
                                for eruzRegistryID in eruzRegistryIDs:
                                    print(eruzRegistryID)
                            except:
                                print("Ничего не занеслось в таблицу члена ЕРУЗ, почему-то")
                                eruzRegistryID = ""

                        # TAKES PUBLISH DATE FROM XML
                        with codecs.open(unzipped_contract_path, "rb", encoding='utf8') as xmlContract:
                            # text = okpd2file.read()
                            # print(text)
                            soupchik = bs.BeautifulSoup(xmlContract, "xml")
                            try:
                                publish_date = soupchik.find("publishDate").text
                            except AttributeError:
                                publish_date = soupchik.find("oos:publishDate").text
                            except:
                                publish_date = soupchik.find_all("")

                            print(publish_date)

# TAKES OKPDs, OKPDS2s

                            OKPDs = ""
                            try:
                                OKPDs = soupchik.find_all("oos:OKPD")
                                #print(OKPDs)
                                # for findokpd in OKPDs:
                                #     okpd = findokpd.find("oos:code").text
                                #     print(okpd)
                            except AttributeError:
                                OKPDs = soupchik.find_all("OKPD")
                                # for findokpd in OKPDs:
                                #     okpd = findokpd.find("code").text
                                #     print(okpd)
                            except AttributeError:
                                OKPDs = soupchik.find_all("OKPD2")
                                # for findokpd in OKPDs:
                                #     okpd = findokpd.find("code").text
                                #     print(okpd)
                            except:
                                OKPDs = ""
                                okpd = ""
                                print("Не нашел ОКПД")

                            lastOkpd = ""

                            if not OKPDs:
                                print("ОКПД не нашлись. Печалька (((((((((((((((((((((((")

                            if OKPDs:
                                for findokpd in OKPDs:
                                    okpd = ""
                                    try:
                                        okpd = findokpd.find("oos:code").text

                                    except:
                                        okpd = findokpd.find("code").text

                                    if okpd == lastOkpd:
                                        continue

                                    lastOkpd = okpd
                                    print(okpd)



                                    if okpd:


                                        try:
                                            sql6 = "SELECT id FROM okpd2_2020 WHERE okpd2_code = %s"
                                            my_cursor.execute(sql6, (okpd,))
                                            # okpd_ids = ""
                                            # okpd_ids = my_cursor.fetchone()
                                            # for okpd_id in okpd_ids:
                                            #     print(okpd_id)
                                            okpd_id = my_cursor.fetchone()[0]
                                            print("OKPD_id = ", okpd_id)
                                        except (RuntimeError, TypeError, NameError):
                                            sql62 = "SELECT id FROM okpd2_2020 WHERE okpd2_code = %s"
                                            okpd = okpd[0:2]
                                            my_cursor.execute(sql62, (okpd,))
                                            # okpd_ids = ""
                                            # okpd_ids = my_cursor.fetchone()
                                            # for okpd_id in okpd_ids:
                                            #     print(okpd_id)
                                            okpd_id = my_cursor.fetchone()[0]
                                            print("TypeError2 OKPD_id = ", okpd_id)
                                        except (RuntimeError, TypeError, NameError):
                                            sql61 = "SELECT id FROM okpd2_2020 WHERE okpd2_code = %s"
                                            okpd = okpd[0:5]
                                            my_cursor.execute(sql61, (okpd,))
                                            # okpd_ids = ""
                                            # okpd_ids = my_cursor.fetchone()
                                            # for okpd_id in okpd_ids:
                                            #     print(okpd_id)
                                            okpd_id = my_cursor.fetchone()[0]
                                            print("TypeError1 OKPD_id = ", okpd_id)
                                        except:
                                            okpd_id = ""
                                            print("Не смогли определить Okpd_id")


                                        if okpd_id and eruz_member_id:
                                            print(okpd_id, eruz_member_id)
                                            try:
                                                sql7 = "INSERT INTO eruz_member_okpd(eruz_member_id, okpd_id) VALUES(%s, %s)"
                                                my_cursor.execute(sql7, (eruz_member_id, okpd_id))
                                                print("Одна сведенная запись по ОКПД и члену ЕРУЗ появилась")
                                            except mysql.connector.IntegrityError:
                                                print("Такая запись уже есть  для okpd_id, eruz_member_okpd")
                                            # except:
                                            #     print("Что-то пошло не так и данные по ОКПД и члену ЕРУЗ не свелись")
                                            # print(okpd_id, eruz_member_id)
                                            # sql7 = "INSERT INTO eruz_member_okpd(eruz_member_id, okpd_id) VALUES(%s, %s)"
                                            # my_cursor.execute(sql7, (eruz_member_id, okpd_id))
                                            # print("Одна сведенная запись по ОКПД и члену ЕРУЗ появилась")

                                        if okpd_id and contract_card_id:
                                            print(okpd_id, contract_card_id)
                                            try:
                                                sql7 = "INSERT INTO contract_card_okpd(contract_card_id, okpd_id) VALUES(%s, %s)"
                                                my_cursor.execute(sql7, (contract_card_id, okpd_id))
                                                print("Одна сведенная запись по ОКПД и карточке контракта появилась")
                                            except mysql.connector.IntegrityError:
                                                print("Такая запись уже есть  для okpd_id, contract_card_id")
                                            except:
                                                print("Что-то пошло не так и данные по ОКПД и карточке контракта не свелись")

                                        if okpd_id and zakupka_card_id:
                                            print(okpd_id, zakupka_card_id)
                                            try:
                                                sql7 = "INSERT INTO zakupka_card_okpd(zakupka_card_id, okpd_id) VALUES(%s, %s)"
                                                my_cursor.execute(sql7, (zakupka_card_id, okpd_id))
                                                print("Одна сведенная запись по ОКПД и карточке контракта появилась")
                                            except mysql.connector.IntegrityError:
                                                print("Такая запись уже есть  для okpd_id, 	zakupka_card")
                                            except:
                                                print("Что-то пошло не так и данные по ОКПД и карточке закупки не свелись")

#### DONE WITH OKPDS

                            ### CREATES MANY TO MANY NON OKPD RELATED TABLES
                            if eruz_member_id and contract_card_id:
                                print(eruz_member_id, contract_card_id)
                                try:
                                    sql7 = "INSERT INTO eruz_member_contract_card(eruz_member_id, contract_card_id) VALUES(%s, %s)"
                                    my_cursor.execute(sql7, (eruz_member_id, contract_card_id))
                                    print("Одна сведенная запись по члену ЕРУЗ и карточке контракта появилась")
                                except mysql.connector.IntegrityError:
                                    print("Такая запись уже есть для eruz_member_id, contract_card_id")
                                except:
                                    print("Что-то пошло не так и данные по члену ЕРУЗ и карточке контракта не свелись")
                            else:
                                print("Карточки ЕРУЗ или карточки контракта не оказалось")

                            if eruz_member_id and zakupka_card_id:
                                print(eruz_member_id, zakupka_card_id)
                                win_status = "yes"
                                try:
                                    sql7 = "INSERT INTO eruz_member_zakupka_card(eruz_member_id, zakupka_card_id, win_status) VALUES(%s, %s, %s)"
                                    my_cursor.execute(sql7, (eruz_member_id, zakupka_card_id, win_status))
                                    print("Одна сведенная запись по члену ЕРУЗ и карточке закупки появилась")
                                except mysql.connector.IntegrityError:
                                    print("Такая запись уже есть для eruz_member_id, zakupka_card_id")
                                except:
                                    print("Что-то пошло не так и данные по члену ЕРУЗ и карточке закупки не свелись")
                            else:
                                print("Карточки ЕРУЗ или карточки закупки не оказалось")
                            ### DONE CREATES MANY TO MANY NON OKPD RELATED TABLES




                            #HERE NEEDS TO WRITE DOWN THIS CONTRACT AS ALREADY PROCESSED ONE
                            # file = open(os.path.join(baseDirContracts, fileNameContractNums), "a+")
                            # file = open(fileNameContractNums, "w+")
                            contractNumsFile.write(addContractNum)
                            contractNumsFile.close()











                # time.sleep(20)



            os.remove(xml_contract)
            #os.rmdir(dirName)
            shutil.rmtree(dirName)

            print("После обработки файл и папка распаковки " + xml_contract + " удалены")
            #Здесь надо сделать запись, что файл архива обработан

            # baseDirContracts = "contracts"
            # fileNameXMLzips = region_name + "_xmlzips.txt"
            # addXMLzip = xml_contract + "\n"
            # xmlZipsFile = open(os.path.join(baseDirContracts, fileNameXMLzips), "a+")
            # if xml_contract in xmlZipsFile:
            #     xmlZipsFile.close()
            #     continue

            xmlZipsFile.write(addXMLzip)
            xmlZipsFile.close()



# ftp.cwd("/fcs_regions/Bashkortostan_Resp/contracts/")
#ftp.cwd("/fcs_regions/")

# print(ftp.getwelcome())
# print("Current Directory", ftp.pwd())
#ftp.dir()
#ftp.retrlines('LIST')
#ftp.mlsd()
# regexp = re.compile(r"^contract")
#
# files = ftp.nlst()
# for file in files:
#     if regexp.search(file):
#         print(file)

# files = ftp.nlst()
# for file in files:
#     if(file.endswith("019.xml.zip")):
#         print(file)
# #fileName = "3.jpg"
# fileNameUpload = "11.jpg"
#
# #saveDir = "D:\pytest"
# #os.chdir(saveDir)
# #file = open(fileName, "wb")
#
# #ftp.retrbinary("RETR " + fileName, file.write)
# fileLoc = "11.jpg"
# fileUp = open(str(fileLoc), "rb")
# ftp.storbinary("STOR " + str(fileNameUpload), fileUp)
# #ftp.storlines("STOR " + fileNameUpload, fileUp)
#
# #file.close()
# fileUp.close()
ftp.quit()