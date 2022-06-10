"""Dados sobre os dividendos das empresas da B3

Este script obtem os dados sobre os dividendos das empresas listadas
na B3 ano a ano, permitindo calcular estátisticas para escolha dos
melhores papéis para formação de uma carteira previdenciária, segundo
o Método Barsi.

Este arquivo pode ser importado como um módulo e contém a seguinte função:

    * listaDividendos() - Estatísticas sobre os dividendos das empresas da B3.
"""
import pandas as pd
import numpy as np
import statistics as st
import json
from datetime import date

def listaDividendos(N = 10, csvFileName = None, b3CsvFileName = "b3.csv", jsonFileName = "yahooData.json"):
    """Obtém as estatísticas dos dividendos das empresas listadas na B3

    Parameters
    -------------
    N: int
        Período usado na análise - os últimos N anos. (padrão: 10)
    jsonFileName: str
        Nome do arquivo json com os dados do Yahoo Finance. (padrão: yahooData.json)
    csvFileName: str
        Se diferente de None, salva os dados em um arquivo CSV com o referido nome. (padrão: None)

    Returns
    -------------
    b3
        Lista com as estatisticas dos dividendos das empresas da B3.
    """

    def getYear(div):
        div["year"] = int(div["date"].split("-")[0])
        return div

    yahooData = None
    with open(jsonFileName, "r") as f:
        yahooData = json.load(f)
    codes = [ x["code"].split(".")[0] for x in yahooData ]

    b3 = pd.read_csv(b3CsvFileName, sep=";")
    b3 = b3[b3["TICKET"].isin(codes)]
    b3.reset_index(inplace = True)
    b3.drop(columns=['index'], inplace = True)
    b3["DIV MEDIO"] = pd.NaT
    b3["DIV MEDIANA"] = pd.NaT
    b3["PRECO ATUAL"] = pd.NaT
    b3["TAXA ATUAL_M"] = pd.NaT
    b3["TAXA ATUAL_MD"] = pd.NaT

    DIV_MEDIO = b3.columns.get_loc('DIV MEDIO')
    DIV_MEDIANA = b3.columns.get_loc('DIV MEDIANA')
    PRECO_ATUAL = b3.columns.get_loc('PRECO ATUAL')
    TAXA_ATUAL_M = b3.columns.get_loc('TAXA ATUAL_M')
    TAXA_ATUAL_MD = b3.columns.get_loc('TAXA ATUAL_MD')
    years = list(range(date.today().year - N, date.today().year))
    for i in range(len(b3)):
        div = list(map(getYear, yahooData[i]["dividends"]))
        dividends = []
        for year in years:
            for d in div:
                if d["year"] == year:
                    dividends.append(d["dividend"])
        if dividends:
            b3.iloc[i, DIV_MEDIO] = round(st.mean(dividends), 2)
            b3.iloc[i, DIV_MEDIANA] = round(st.median(dividends), 2)
        else:
            b3.iloc[i, DIV_MEDIO] = 0.0
            b3.iloc[i, DIV_MEDIANA] = 0.0
        b3.iloc[i, PRECO_ATUAL] = yahooData[i]["price"]
        b3.iloc[i, TAXA_ATUAL_M] = round(b3.iloc[i, DIV_MEDIO] * 100.0 / b3.iloc[i, PRECO_ATUAL], 2)
        b3.iloc[i, TAXA_ATUAL_MD] = round(b3.iloc[i, DIV_MEDIANA] * 100.0 / b3.iloc[i, PRECO_ATUAL], 2)

    if (csvFileName != None):
        b3.to_csv(csvFileName, sep=";", index=False)

    return b3

if __name__ == '__main__':
    listaDividendos(N = 10, jsonFileName="../data/yahooData.json",
        b3CsvFileName="../data/b3.csv", csvFileName="../data/listaDividendos.csv")
