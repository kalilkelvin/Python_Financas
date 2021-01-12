from datetime import datetime

import pandas as pd
import funcAux


def dados_cvm(inicio, fim=None, l_cnpj=None):
    if fim is None:
        fim = pd.to_datetime(datetime.today().strftime('%Y-%m-%d'))

    datas = pd.date_range(inicio, fim, freq='MS')
    historico = pd.DataFrame()

    print('----Iniciando coleta de dados----')
    for data in datas:

        try:
            url = 'http://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/inf_diario_fi_{}{:02d}.csv'.format(data.year,
                                                                                                            data.month)
            download_part = funcAux.downloadWithProgressBar(url)
            mensal = pd.read_csv(download_part, sep=';')

        except:
            print("Arquivo {} não encontrado!".format(url))

        historico = pd.concat([historico, mensal], ignore_index=True)
    print('----Processo Concluído----')

    historico = historico[historico['CNPJ_FUNDO'].isin(l_cnpj)]

    return historico


def calc_retabilidade():

    dados = pd.read_csv('venv/assets/historico.csv')
    fundos = dados['CNPJ_FUNDO'].unique()

    fundos_rent = pd.DataFrame()

    i = 0
    while i < len(fundos):

        cotas = dados[dados['CNPJ_FUNDO'] == fundos[i]][['CNPJ_FUNDO', 'DT_COMPTC', 'VL_QUOTA']].reset_index()
        cotas['RENT'] = cotas[['VL_QUOTA']].apply(lambda x: x / x.shift()-1).fillna(0)
        cotas['RENT_ACUM'] = cotas[['RENT']].apply(lambda x: x.cumsum()*100)

        fundos_rent = pd.concat([fundos_rent, cotas], ignore_index=True)

        i += 1

    return fundos_rent
