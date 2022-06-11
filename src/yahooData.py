"""Dados do Yahoo Finance sobre os dividendos das empresas listadas na B3

Este script obtem os dados sobre os dividendos das empresas listadas
na B3 no Yahoo Finance, podendo salvá-los em um arquivo JSON. Os códigos 
dos ativos são lidos de um arquivo CSV.

Este arquivo pode ser importado como um módulo e contém a seguinte função:

    * getYahooData() - Obtém do Yahoo Finance os dados de dividendos das empresas da B3
"""

import numpy as np
import pandas as pd
import yfinance as yf
import json

def getYahooData(jsonFileName = None, csvFileName = "b3.csv"):
    """Obtém do Yahoo Finance os dados de dividendos das empresas da B3

    Parameters
    -------------
    jsonFileName: str
        Se diferente de None, salva os dados obtidos em um arquivo JSON
    csvFileName: str
        Nome do arquivo CSV com os códigos dos ativos (padrão: "b3.csv")

    Returns
    -------------
    yahooData
        Lista com os dados de dividendos das empresas
    """

    b3 = pd.read_csv(csvFileName, sep=";")
    b3["DIV MEDIO"] = pd.NaT
    b3["PRECO ATUAL"] = pd.NaT
    b3["TAXA ATUAL"] = pd.NaT

    yahooData = [{"code": ticket + ".SA", "ticker": yf.Ticker(ticket+".SA"), "price": 0, "dividends": [] } for ticket in b3["TICKET"] ]
    def readYahooData(data, i, total):
        print("%-9s - %3d/%3d - %.1f%%" % (data["code"], i, total, (i*100.0/total)))
        data["price"] = data["ticker"].info.get("regularMarketPrice", 0)
        if (data["price"] == 0):
            data["dividends"] = []
            return data
        data["dividends"] = data["ticker"].actions
        if (len(data["dividends"]) == 0):
            data["dividends"] = []
        else:
            data["dividends"].drop("Stock Splits", inplace=True, axis=1)
            data["dividends"].reset_index(inplace=True)
            data["dividends"] = [{"date": data["dividends"]["Date"][i].strftime("%Y-%m-%d"), 
                "dividend": data["dividends"]["Dividends"][i]} 
                for i in data["dividends"].index]
            data.pop("ticker")
        return data

    i = 0
    total = len(yahooData)
    for data in yahooData:
        i = i + 1
        readYahooData(data, i, total)

    yahooData = list(filter(lambda x: x.get("ticker", None) == None, yahooData))
    yahooData = list(filter(lambda x: x.get("price", None) != None, yahooData))
    yahooData = list(filter(lambda x: x.get("price", None) != 0, yahooData))

    if (jsonFileName != None):
        with open(jsonFileName, "w") as yahooFile:
            json.dump(yahooData, yahooFile, indent=2)
    return yahooData

if __name__ == '__main__':
    getYahooData(jsonFileName = "../data/yahooData.json", csvFileName="../data/b3.csv")
