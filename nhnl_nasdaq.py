import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

nasdaq_tickers = [
    'AAPL','ASML','QCOM','KLAC','ADI',
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
    'XEL','PYPL','BKR','FANG','ADSK'

]

print('Baixando dados...')
dados = yf.download(nasdaq_tickers)['Close']
nasdaq = yf.download('^NDX', start=dados.index.min(), end=dados.index.max())['Close']

nh = dados == dados.rolling(window=252).max()
nl = dados == dados.rolling(window=252).min()

nh_nl = nh.sum(axis=1) - nl.sum(axis=1)
nh_nl = nh_nl.dropna()
nh_nl_ma = nh_nl.rolling(window=20).mean()
nasdaq = nasdaq.reindex(nh_nl.index)

fig, ax1 = plt.subplots(figsize=(14,5))

ax1.plot(nh_nl, marker='o', color='navy', label='NH-NL')
ax1.plot(nh_nl_ma, label='Média Móvel de 20 dias', linewidth=1, color='red')
ax1.set_ylabel('NH-NL', color='navy')
ax1.tick_params(axis='y', labelcolor='navy')
ax1.axhline(y=0, color='black')

ax2 = ax1.twinx()
ax2.plot(nasdaq, color='slategray', label='NASDAQ', alpha=0.3)
ax2.set_ylabel('NASDAQ', color='slategray')
ax2.tick_params(axis='y', labelcolor='slategray')

plt.title('NH-NL X NASDAQ')
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

