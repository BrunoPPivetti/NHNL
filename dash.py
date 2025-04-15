import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Indicador NH-NL", layout="wide")

# Título
st.title("📈 Indicador NH-NL (Novas Máximas - Novas Mínimas)")

# Sidebar: seleção do índice
indice_opcao = st.sidebar.selectbox("Escolha o índice:", ["IBOV", "NASDAQ", "DAX"])

# Define os tickers para cada índice
indices = {
    "IBOV": 
    ['ALOS3.SA','ABEV3.SA','ASAI3.SA','AURE3.SA','AMOB3.SA',
    'AZUL4.SA','AZZA3.SA','B3SA3.SA','BBSE3.SA','BBDC3.SA',
    'BBDC4.SA','BRAP4.SA','BBAS3.SA','BRKM5.SA','BRAV3.SA',
    'BRFS3.SA','BPAC11.SA','CXSE3.SA','CRFB3.SA','CCRO3.SA',
    'CMIG4.SA','COGN3.SA','CPLE6.SA','CSAN3.SA','CPFE3.SA',
    'CMIN3.SA','CVCB3.SA','CYRE3.SA','ELET3.SA','ELET6.SA',
    'EMBR3.SA','ENGI11.SA','ENEV3.SA','EGIE3.SA','EQTL3.SA',
    'FLRY3.SA','GGBR4.SA','GOAU4.SA','NTCO3.SA','HAPV3.SA',
    'HYPE3.SA','IGTI11.SA','IRBR3.SA','ISAE4.SA','ITSA4.SA',
    'ITUB4.SA','JBSS3.SA','KLBN11.SA','RENT3.SA','LREN3.SA',
    'LWSA3.SA','MGLU3.SA','POMO4.SA','MRFG3.SA','BEEF3.SA',
    'MRVE3.SA','MULT3.SA','PCAR3.SA','PETR3.SA','PETR4.SA',
    'RECV3.SA','PRIO3.SA','PETZ3.SA','PSSA3.SA','RADL3.SA',
    'RAIZ4.SA','RDOR3.SA','RAIL3.SA','SBSP3.SA','SANB11.SA',
    'STBP3.SA','SMTO3.SA','CSNA3.SA','SLCE3.SA','SUZB3.SA',
    'TAEE11.SA','VIVT3.SA','TIMS3.SA','TOTS3.SA','UGPA3.SA',
    'USIM5.SA','VALE3.SA','VAMO3.SA','VBBR3.SA','VIVA3.SA',
    'WEGE3.SA','YDUQ3.SA'],
    "NASDAQ": 
    ['AAPL','ASML','QCOM','KLAC','ADI',
    'INTC','NVDA','CSCO','TXN','MU',
    'AXON','NXPI','AVGO','AMD','ARM',
    'MRVL','MCHP','GFS','ON','TSLA',
    'MSFT','PLTR','PANW','FTNT','ROP',
    'TEAM','GOOGL','INTU','CRWD','CDNS',
    'PAYX','VRSK','EA','META','ADBE',
    'MSTR','SNPS','TTWO','DDOG','ZS',
    'NFLX','ADP','APP','WDAY','CTSH',
    'ANSS','CDW','CSGP','TTD','MDB',
    'AMZN','PDD','ORLY','CPRT','COST',
    'MELI','ROST','TMUS','LIN','AZN',
    'ISRG','GILD','VRTX','AMGN','REGN',
    'IDXX','GEHC','DXCM','BIIB','PEP',
    'MNST','MDLZ','KDP','CCEP','KHC',
    'LULU','BKNG','SBUX','ABNB','MAR',
    'CMCSA','CTAS','CHTR','WBD','HON',
    'FAST','AMAT','LRCX','PCAR','DASH',
    'CSX','ODFL','CEG','AEP','EXC',
    'XEL','PYPL','BKR','FANG','ADSK'],
    "DAX": 
    ['ALV.DE','MUV2.DE','DB1.DE','HNR1.DE',
    'DBK.DE','CBK.DE','VNA.DE','SAP.DE',
    'SIE.DE','ENR.DE','BAS.DE','AIR.DE',
    'RHM.DE','IFX.DE','MTX.DE','DTE.DE',
    'MBG.DE','VOW3.DE','BMW.DE','P911.DE',
    'DTG.DE','CON.DE','PAH3','MRK.DE',
    'SHL.DE','BAYN.DE','SRT3.DE','QIA.DE',
    'ADS.DE','HEN3.DE','BEI.DE','EOAN.DE',
    'RWE.DE','DHL.DE','HEI.DE','FRE.DE',
    'FME.DE','SY1.DE','ZAL.DE','BNR.DE']
}

tickers = indices[indice_opcao]

# Intervalo de tempo
hoje = datetime.datetime.today()
data_inicio = '2000-01-01'

st.sidebar.write("Buscando dados históricos desde: 01/01/2000")

# Download dos dados
dados = yf.download(tickers, start=data_inicio)['Close']
dados = dados.dropna(how='all')

# Cálculo do NH-NL
nh = dados == dados.rolling(window=252).max()
l = dados == dados.rolling(window=252).min()
nh_nl = nh.sum(axis=1) - l.sum(axis=1)
nh_nl_ma = nh_nl.rolling(window=20).mean()

# Baixa o índice de referência
ticker_indice = {
     "IBOV": "^BVSP",
     "NASDAQ": "^NDX",
     "DAX": "^GDAXI"
}[indice_opcao]

indice = yf.download(ticker_indice, start=data_inicio)['Close']
print(indice)
indice = indice.reindex(nh_nl.index)

# #Garantir Series 1D para DataFrame final
# indice = pd.Series(indice, name=indice_opcao)
# nh_nl = pd.Series(nh_nl, name='NH-NL')
# nh_nl_ma = pd.Series(nh_nl_ma, name='Média Móvel')

# Gráfico com Plotly
fig = go.Figure()
fig.add_trace(go.Scatter(x=nh_nl.index, y=nh_nl, mode='lines+markers', name='NH-NL', line=dict(color='cyan')))
fig.add_trace(go.Scatter(x=nh_nl_ma.index, y=nh_nl_ma, mode='lines', name='Média Móvel 20 dias', line=dict(color='orange')))

fig.update_layout(
    title="Indicador NH-NL",
    xaxis=dict(title='Data'),
    yaxis=dict(title='NH - NL', side='left'),
    legend=dict(x=0.01, y=0.99),
    height=600,
    shapes=[
        dict(
            type='line',
            xref='paper',
            x0=0,
            x1=1,
            yref='y',
            y0=0,
            y1=0,
            line=dict(color='white',width=1.5)
        )
    ]
)

# Mostrar gráfico
st.plotly_chart(fig, use_container_width=True)
