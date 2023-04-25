import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.sandbox.regression.gmm import GMM

class DynamicPanelGMM(GMM):

    def __init__(self, data, y_col, x_cols, n_lags, *args, **kwds):
        self.y_col = y_col
        self.x_cols = x_cols
        self.n_lags = n_lags

        y = data[self.y_col]
        x = data[self.x_cols]
        z = self._create_instruments(data, n_lags)

        # Align the data
        y, _ = y.align(x, join='inner', axis=0)
        x, _ = x.align(z, join='inner', axis=0)
        z, _ = z.align(y, join='inner', axis=0)

        super(DynamicPanelGMM, self).__init__(endog=y, exog=x, instrument=z, *args, **kwds)


    def _create_instruments(self, data, n_lags):
        instruments = []
        for i in range(1, n_lags + 1):
            instruments.append(data[self.x_cols].shift(i))
        return pd.concat(instruments, axis=1).dropna()

    def momcond(self, params):
        y = self.endog
        x = self.exog
        z = self.instrument
        e = y - np.dot(x, params)
        g = np.dot(z.T, e)
        return g

# Read your data
df = pd.read_csv('merged_data_new.csv')

# Set the index
df = df.set_index(['Country code', 'Year'])

# Define your dependent and independent variables
y_col = 'GDP per capita growth (annual %)'
x_cols = df.drop(columns=[y_col]).columns.tolist()

# Estimate the model
model = DynamicPanelGMM(df, y_col, x_cols, n_lags=1)
result = model.fit()

print(result.summary())
