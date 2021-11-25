"""
Parse information from the HTML downloads and store it in a CSV.
"""
import csv
import glob
import json
import os
import sys

from bs4 import BeautifulSoup

from config import from_config


def get_data_rows(html_filename, data_indexes_len_14, data_indexes_len_15):
    with open(html_filename, 'r') as file_in:
        filename = html_filename.split('/')[-1].split('.')[0]
        content = file_in.read()
        soup = BeautifulSoup(content, 'lxml')
        data_elem = soup.find('table')
        trs = [tr.text.strip('\n').strip(' ') for tr in data_elem.find_all('tr')]
        if len(trs) == 14:
            data = [x for ind, x in enumerate(trs) if ind in data_indexes_len_14]
            data.append(filename)
            return data
        elif len(trs) == 15:
            data = [x for ind, x in enumerate(trs) if ind in data_indexes_len_15]
            data.append(filename)
            return data


def parse(data):
    row = []
    gta_num = data[0].split(':')[1].split('S')[0].strip()
    series = data[0].split(':')[-1].strip()
    estab_origen = data[1].split('\n\n\n')[0].split('\n')
    est_or = estab_origen[0].split(':')[-1].strip()
    cod_est_or = estab_origen[1].split(':')[-1].strip()
    inscr_est_or = estab_origen[2].split(':')[-1].strip()
    nome_or = estab_origen[3].split(':')[-1].strip()
    cpf_or = estab_origen[4].split(':')[-1].strip()
    mun_or = estab_origen[5].split(':')[-1].strip()
    estab_dest = data[1].split('\n\n\n')[1].split('\n')
    est_dest = estab_dest[0].split(':')[-1].strip()
    cod_est_dest = estab_dest[1].split(':')[-1].strip()
    inscr_est_dest = estab_dest[2].split(':')[-1].strip()
    nome_dest = estab_dest[3].split(':')[-1].strip()
    cpf_dest = estab_dest[4].split(':')[-1].strip()
    mun_dest = estab_dest[5].split(':')[-1].strip()
    transporte = data[2].split('\n\n')[0].split(':')[1].strip()
    finalidade = data[2].split('\n\n')[1].split(':')[1].strip()
    especie = data[3].split('\n')[0].split(':')[-1].strip()
    faixa = json.dumps(data[3].split('\n')[1:-1])
    vaccine = json.dumps([item.strip() for item in data[4].split('\n')[1:-1]])
    dare = {data[5].split('\n')[1].strip() if 'Dare' in data[5] else ''}
    data_emmissao = data[6].split('\n\n')[0].split(':')[1].strip()
    validade = data[6].split('\n\n')[1].split(':')[1].strip()
    filename = data[7]
    row.extend([gta_num, series, est_or, est_dest, cod_est_or, cod_est_dest, inscr_est_or, inscr_est_dest, nome_or,
                nome_dest, cpf_or, cpf_dest, mun_or, mun_dest, transporte, finalidade, especie, faixa, vaccine, dare,
                data_emmissao, validade, filename])
    return row


def main(html_glob, output_filename, attributes, data_indexes_len_14, data_indexes_len_15):
    run_id = os.getenv('RUN_ID')
    date = os.getenv('DATE')
    with open(output_filename.format(run_id=run_id, date=date), 'w') as file_out:
        writer = csv.writer(file_out)
        writer.writerow(attributes)
        for html_filename in glob.glob(html_glob.format(run_id=run_id, date=date)):
            if html_filename.endswith('.html'):
                data = get_data_rows(html_filename, data_indexes_len_14, data_indexes_len_15)
                try:
                    writer.writerow(parse(data))
                except Exception as e:
                    print(e)
                    continue


if __name__ == '__main__':
    script, config_filename = sys.argv
    from_config(main)(config_filename)
