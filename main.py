import coreEtl
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import pandas as pd

warnings.filterwarnings("ignore")

def main():

    cnpjs = ['12.082.452/0001-49', '34.309.551/0001-53', '32.893.503/0001-20', '30.509.221/0001-50']
    data_inicio = '2020-11-01'
    data_fim = None

    #dados = coreEtl.dados_cvm(data_inicio, data_fim, cnpjs)
    #dados.to_csv('venv/assets/historico.csv')

    rentabilidade = coreEtl.calc_retabilidade()

    sns.set(font_scale=1)
    fig = plt.figure(figsize=(20, 7))
    for fundo in cnpjs:

        rent = rentabilidade[rentabilidade['CNPJ_FUNDO'].isin([fundo])]
        rent['DT_COMPTC'] = pd.to_datetime(rent['DT_COMPTC'])

        plt.plot(rent['DT_COMPTC'], rent['RENT_ACUM'])

    plt.legend(cnpjs, ncol=2, loc='upper left');
    plt.xlabel("Período")
    plt.ylabel("Rent - %")
    plt.title("Rentabilidade Fundos")
    plt.show()


if __name__ == '__main__':
    main()
