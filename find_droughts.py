import pandas as pd
import numpy as np

# drought is defined as a continuous period of at least 3 months where SSI_6 < 0 and hits -1
# SSI is computed as the 24-week (6mo) rolling mean of standarized lognormal streamflows
def find_droughts(df):
  # http://stackoverflow.com/questions/24281936/delimiting-contiguous-regions-with-values-above-a-certain-threshold-in-pandas-da
  df['tag'] = df.ssi < 0
  first = df.index[df.tag & ~ df.tag.shift(1).fillna(False)]
  last = df.index[df.tag & ~ df.tag.shift(-1).fillna(False)]

  droughts = []
  for i,j in zip(first,last):
    if j > i + pd.tseries.offsets.DateOffset(months=3) and (df.ssi.loc[i:j] < -1).any():
      info = {}
      info['start'] = i 
      info['end'] = j
      info['severity'] = np.sum(df.ssi.loc[i:j])
      droughts.append(info)

  return droughts
