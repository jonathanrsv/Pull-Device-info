import csv
from requests_html import HTMLSession
from unicodedata import normalize 
import pprint

def clear_text(txt):
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')

def get_phone_list(csv_file):
    with open(csv_file, 'rt') as csvfile:
            normalized = []
            spamreader = csv.reader(csvfile, delimiter=';')
            for row in spamreader:
                phone_url = get_url_phone_data("https://www.maiscelular.com.br/pesquisa/?q=" + row[0])
                if phone_url: 
                    print("Device processado: " + row[0] + ', url: ' + phone_url)
                    normalized.append({
                        'modelo':row[0], 
                        'url_de_busca': phone_url,
                        'dados': get_phone_table_data(phone_url)
                        })

    return normalized

def get_url_phone_data(url):
    session = HTMLSession()
    r = session.get(url)
    element =  r.html.find('.bl1 a',first=True)
    if element:
        return "https://www.maiscelular.com.br" + element.attrs['href']
    else: 
        return False

def get_phone_table_data(url):
    session = HTMLSession()
    r = session.get(url)
    element =  r.html.find('.tab_phone tr')
    phone_data = {}
    try:
        for tr in element:
            valor = 'null'
            if len(tr.find("td")) > 1: 
                 valor = tr.find("td")[1].text 
            phone_data[clear_text(tr.find("td")[0].text)] = valor
    except ValueError:
        print("Falha na url de busca: " + ValueError)
        pass
    return phone_data

def write_csv(data, csv_name):
    with open(csv_name, mode='w',  encoding='latin', newline='') as file: 
        writer = csv.writer(file, delimiter=';')
        writer.writerow([
                "modelo",
                'Marca', 
                'Memoria RAM',
                'NFC',
                'Capacidade bateria'
        ])

        for phone in data:
            phone_info = phone["dados"]

            writer.writerow([
                phone["modelo"],
                phone_info['Marca'], 
                #phone_info['Modelo'],
                phone_info['Memoria RAM'].split(" ")[0],
                phone_info['NFC'],
                phone_info['Capacidade bateria']
            ])

def pull_device_info(csv_file, csv_file_output):
    phone_list = get_phone_list(csv_file)

    write_csv(phone_list, csv_file_output)




