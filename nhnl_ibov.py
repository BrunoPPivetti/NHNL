import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

ibov_tickers = [
    'ALOS3.SA','ABEV3.SA','ASAI3.SA','AURE3.SA','AMOB3.SA',
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
    'WEGE3.SA','YDUQ3.SA',
]

print('Baixando dados...')
dados = yf.download(ibov_tickers)['Close']
ibov = yf.download('^BVSP', start=dados.index.min(), end=dados.index.max())['Close']

nh = dados == dados.rolling(window=252).max()
nl = dados == dados.rolling(window=252).min()

nh_nl = nh.sum(axis=1) - nl.sum(axis=1)
nh_nl = nh_nl.dropna()
nh_nl_ma = nh_nl.rolling(window=20).mean()
ibov = ibov.reindex(nh_nl.index)

fig, ax1 = plt.subplots(figsize=(14,5))

ax1.plot(nh_nl, marker='o', color='blue', label='NH-NL')
ax1.plot(nh_nl_ma, label='Média Móvel de 20 dias', linewidth=1, color='red')
ax1.set_ylabel('NH-NL', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')
ax1.axhline(y=0, color='black')

ax2 = ax1.twinx()
ax2.plot(ibov, color='slategray', label='Ibovespa', alpha=0.3)
ax2.set_ylabel('Ibovespa', color='slategray')
ax2.tick_params(axis='y', labelcolor='slategray')

plt.title('NH-NL X IBOV')
fig.tight_layout()
plt.grid(True)
plt.show()




# plt.figure(figsize=(14,5))
# nh_nl.plot(marker='o')
# nh_nl_ma.plot(label='Média Móvel de 20 dias', linewidth=2, color='red')
# plt.axhline(y=0, color='black')
# plt.title('Índice NH-NL - IBOVESPA')
# plt.ylabel("NH - NL")
# plt.grid(True)
# plt.tight_layout()
# plt.show()

