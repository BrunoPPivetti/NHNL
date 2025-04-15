import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

dax_tickers = [
    'ALV.DE','MUV2.DE','DB1.DE','HNR1.DE',
    'DBK.DE','CBK.DE','VNA.DE','SAP.DE',
    'SIE.DE','ENR.DE','BAS.DE','AIR.DE',
    'RHM.DE','IFX.DE','MTX.DE','DTE.DE',
    'MBG.DE','VOW3.DE','BMW.DE','P911.DE',
    'DTG.DE','CON.DE','PAH3','MRK.DE',
    'SHL.DE','BAYN.DE','SRT3.DE','QIA.DE',
    'ADS.DE','HEN3.DE','BEI.DE','EOAN.DE',
    'RWE.DE','DHL.DE','HEI.DE','FRE.DE',
    'FME.DE','SY1.DE','ZAL.DE','BNR.DE'
]

print('Baixando dados...')
dados = yf.download(dax_tickers)['Close']
dax = yf.download('^GDAXI', start=dados.index.min(), end=dados.index.max())['Close']

nh = dados == dados.rolling(window=252).max()
nl = dados == dados.rolling(window=252).min()

nh_nl = nh.sum(axis=1) - nl.sum(axis=1)
nh_nl = nh_nl.dropna()
nh_nl_ma = nh_nl.rolling(window=20).mean()
dax = dax.reindex(nh_nl.index)

fig, ax1 = plt.subplots(figsize=(14,5))

ax1.plot(nh_nl, marker='o', color='cyan', label='NH-NL')
ax1.plot(nh_nl_ma, label='Média Móvel de 20 dias', linewidth=1, color='red')
ax1.set_ylabel('NH-NL', color='cyan')
ax1.tick_params(axis='y', labelcolor='cyan')
ax1.axhline(y=0, color='black')

ax2 = ax1.twinx()
ax2.plot(dax, color='slategray', label='DAX', alpha=0.3)
ax2.set_ylabel('DAX', color='slategray')
ax2.tick_params(axis='y', labelcolor='slategray')

plt.title('NH-NL X DAX')
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

