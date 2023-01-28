import pandas as pd
import talib as ta
from backtesting import Strategy, Backtest

'''import plotly 
import plotly.io as pio
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots'''


"""Detect peaks in data based on their amplitude and other features."""

import numpy as np



def detect_peaks(x, mph=None, mpd=1, threshold=0, edge='rising',
                 kpsh=False, valley=False, show=False, ax=None, title=True):

    """Detect peaks in data based on their amplitude and other features.

    Parameters
    ----------
    x : 1D array_like
        data.
    mph : {None, number}, optional (default = None)
        detect peaks that are greater than minimum peak height (if parameter
        `valley` is False) or peaks that are smaller than maximum peak height
         (if parameter `valley` is True).
    mpd : positive integer, optional (default = 1)
        detect peaks that are at least separated by minimum peak distance (in
        number of data).
    threshold : positive number, optional (default = 0)
        detect peaks (valleys) that are greater (smaller) than `threshold`
        in relation to their immediate neighbors.
    edge : {None, 'rising', 'falling', 'both'}, optional (default = 'rising')
        for a flat peak, keep only the rising edge ('rising'), only the
        falling edge ('falling'), both edges ('both'), or don't detect a
        flat peak (None).
    kpsh : bool, optional (default = False)
        keep peaks with same height even if they are closer than `mpd`.
    valley : bool, optional (default = False)
        if True (1), detect valleys (local minima) instead of peaks.
    show : bool, optional (default = False)
        if True (1), plot data in matplotlib figure.
    ax : a matplotlib.axes.Axes instance, optional (default = None).
    title : bool or string, optional (default = True)
        if True, show standard title. If False or empty string, doesn't show
        any title. If string, shows string as title.

    Returns
    -------
    ind : 1D array_like
        indeces of the peaks in `x`.

    Notes
    -----
    The detection of valleys instead of peaks is performed internally by simply
    negating the data: `ind_valleys = detect_peaks(-x)`

    The function can handle NaN's

    See this IPython Notebook [1]_.

    References
    ----------
    .. [1] http://nbviewer.ipython.org/github/demotu/BMC/blob/master/notebooks/DetectPeaks.ipynb

    Examples
    --------
    >>> from detect_peaks import detect_peaks
    >>> x = np.random.randn(100)
    >>> x[60:81] = np.nan
    >>> # detect all peaks and plot data
    >>> ind = detect_peaks(x, show=True)
    >>> print(ind)

    >>> x = np.sin(2*np.pi*5*np.linspace(0, 1, 200)) + np.random.randn(200)/5
    >>> # set minimum peak height = 0 and minimum peak distance = 20
    >>> detect_peaks(x, mph=0, mpd=20, show=True)

    >>> x = [0, 1, 0, 2, 0, 3, 0, 2, 0, 1, 0]
    >>> # set minimum peak distance = 2
    >>> detect_peaks(x, mpd=2, show=True)

    >>> x = np.sin(2*np.pi*5*np.linspace(0, 1, 200)) + np.random.randn(200)/5
    >>> # detection of valleys instead of peaks
    >>> detect_peaks(x, mph=-1.2, mpd=20, valley=True, show=True)

    >>> x = [0, 1, 1, 0, 1, 1, 0]
    >>> # detect both edges
    >>> detect_peaks(x, edge='both', show=True)

    >>> x = [-2, 1, -2, 2, 1, 1, 3, 0]
    >>> # set threshold = 2
    >>> detect_peaks(x, threshold = 2, show=True)

    >>> x = [-2, 1, -2, 2, 1, 1, 3, 0]
    >>> fig, axs = plt.subplots(ncols=2, nrows=1, figsize=(10, 4))
    >>> detect_peaks(x, show=True, ax=axs[0], threshold=0.5, title=False)
    >>> detect_peaks(x, show=True, ax=axs[1], threshold=1.5, title=False)

    Version history
    ---------------
    '1.0.6':
        Fix issue of when specifying ax object only the first plot was shown
        Add parameter to choose if a title is shown and input a title
    '1.0.5':
        The sign of `mph` is inverted if parameter `valley` is True

    """

    x = np.atleast_1d(x).astype('float64')
    if x.size < 3:
        return np.array([], dtype=int)
    if valley:
        x = -x
        if mph is not None:
            mph = -mph
    # find indices of all peaks
    dx = x[1:] - x[:-1]
    # handle NaN's
    indnan = np.where(np.isnan(x))[0]
    if indnan.size:
        x[indnan] = np.inf
        dx[np.where(np.isnan(dx))[0]] = np.inf
    ine, ire, ife = np.array([[], [], []], dtype=int)
    if not edge:
        ine = np.where((np.hstack((dx, 0)) < 0) & (np.hstack((0, dx)) > 0))[0]
    else:
        if edge.lower() in ['rising', 'both']:
            ire = np.where((np.hstack((dx, 0)) <= 0) & (np.hstack((0, dx)) > 0))[0]
        if edge.lower() in ['falling', 'both']:
            ife = np.where((np.hstack((dx, 0)) < 0) & (np.hstack((0, dx)) >= 0))[0]
    ind = np.unique(np.hstack((ine, ire, ife)))
    # handle NaN's
    if ind.size and indnan.size:
        # NaN's and values close to NaN's cannot be peaks
        ind = ind[np.in1d(ind, np.unique(np.hstack((indnan, indnan-1, indnan+1))), invert=True)]
    # first and last values of x cannot be peaks
    if ind.size and ind[0] == 0:
        ind = ind[1:]
    if ind.size and ind[-1] == x.size-1:
        ind = ind[:-1]
    # remove peaks < minimum peak height
    if ind.size and mph is not None:
        ind = ind[x[ind] >= mph]
    # remove peaks - neighbors < threshold
    if ind.size and threshold > 0:
        dx = np.min(np.vstack([x[ind]-x[ind-1], x[ind]-x[ind+1]]), axis=0)
        ind = np.delete(ind, np.where(dx < threshold)[0])
    # detect small peaks closer than minimum peak distance
    if ind.size and mpd > 1:
        ind = ind[np.argsort(x[ind])][::-1]  # sort ind by peak height
        idel = np.zeros(ind.size, dtype=bool)
        for i in range(ind.size):
            if not idel[i]:
                # keep peaks with the same height if kpsh is True
                idel = idel | (ind >= ind[i] - mpd) & (ind <= ind[i] + mpd) \
                       & (x[ind[i]] > x[ind] if kpsh else True)
                idel[i] = 0  # Keep current peak
        # remove the small peaks and sort back the indices by their occurrence
        ind = np.sort(ind[~idel])

    if show:
        if indnan.size:
            x[indnan] = np.nan
        if valley:
            x = -x
            if mph is not None:
                mph = -mph
        _plot(x, mph, mpd, threshold, edge, valley, ax, ind, title)

    return ind



def _plot(x, mph, mpd, threshold, edge, valley, ax, ind, title):
    """Plot results of the detect_peaks function, see its help."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print('matplotlib is not available.')
    else:
        if ax is None:
            _, ax = plt.subplots(1, 1, figsize=(8, 4))
            no_ax = True
        else:
            no_ax = False

        ax.plot(x, 'b', lw=1)
        if ind.size:
            label = 'valley' if valley else 'peak'
            label = label + 's' if ind.size > 1 else label
            ax.plot(ind, x[ind], '+', mfc=None, mec='r', mew=2, ms=8,
                    label='%d %s' % (ind.size, label))
            ax.legend(loc='best', framealpha=.5, numpoints=1)
        ax.set_xlim(-.02*x.size, x.size*1.02-1)
        ymin, ymax = x[np.isfinite(x)].min(), x[np.isfinite(x)].max()
        yrange = ymax - ymin if ymax > ymin else 1
        ax.set_ylim(ymin - 0.1*yrange, ymax + 0.1*yrange)
        ax.set_xlabel('Data #', fontsize=14)
        ax.set_ylabel('Amplitude', fontsize=14)
        if title:
            if not isinstance(title, str):
                mode = 'Valley detection' if valley else 'Peak detection'
                title = "%s (mph=%s, mpd=%d, threshold=%s, edge='%s')"% \
                        (mode, str(mph), mpd, str(threshold), edge)
            ax.set_title(title)
        # plt.grid()
        if no_ax:
            plt.show()


def calculate_peak(df, dist = 300, plot = False, valley = False,tam_stop = 0.0003):

    df['RSI'] = ta.RSI(df['Close'],timeperiod = 14)

    x = df['Close']
    ind = detect_peaks(x,show=False,mpd = dist,valley = valley)

    #ind = [i for i in ind if df.loc[i]['RSI'] > 70]
    
    lista_signal = [0] * len(df)
    lista_stop = [0] * len(df)
    lista_tp = [0] * len(df)
    lista_close = df['Close'].values

    if not valley:

        for i in ind:

            try:
                valor_pra_frente = 2
                tamanho_stop = lista_close[i] - lista_close[i+valor_pra_frente]
                #tamanho_stop = 0.000
                if tamanho_stop > tam_stop:
                    lista_signal[i+valor_pra_frente] = 2
                    lista_stop[i+valor_pra_frente] = lista_close[i]
                    #lista_stop[i+valor_pra_frente] = lista_close[i] + tamanho_stop
                    lista_tp[i+valor_pra_frente] = lista_close[i+valor_pra_frente] - (tamanho_stop)
            except:
                pass


        df['signal'] = lista_signal
        df['stop'] = lista_stop
        df['tp'] = lista_tp
        df['tamanho'] = df['stop'] - df['Close']

        df['Data'] = pd.to_datetime(df['Data'])
        df = df.set_index('Data')

    else:

        for i in ind:

            try:
                tamanho_stop = lista_close[i+2] - lista_close[i] 
                if tamanho_stop > tam_stop:
                    lista_signal[i+2] = 1
                    lista_stop[i+2] = lista_close[i]
                    lista_tp[i+2] = lista_close[i+2] + (tamanho_stop)
            except:
                pass

        df['signal'] = lista_signal
        df['stop'] = lista_stop
        df['tp'] = lista_tp
        df['tamanho'] = df['stop'] - df['Close']

        df['Data'] = pd.to_datetime(df['Data'])
        df = df.set_index('Data')
        
    def SMA(array, n):
        """Simple moving average"""
        return pd.Series(array).rolling(n).mean()

    def teste(x):
        a = [1.0885] * len(x)
        return pd.Series(a)
    
    def SIGNAL():
        return df.signal

    class MyCandlesStrat(Strategy):
        def init(self):
            super().init()
            self.signal1 = self.I(SIGNAL)
            self.ema = self.I(ta.EMA, self.data.Close, 89)
            self.rsi = self.I(ta.RSI, self.data.Close, 14)
            #self.teste = self.I(teste,self.data.Close)

        def next(self):
            super().next() 
            if self.signal1==1:
                sl1 = self.data.stop[-1]
                tp1 = self.data.tp[-1]
                self.buy(sl=sl1, tp=tp1)
            elif self.signal1==2 and self.data.Close < self.ema:
                sl1 = self.data.stop[-1]
                tp1 = self.data.tp[-1]
                self.sell(sl=sl1, tp=tp1)

    bt = Backtest(df, MyCandlesStrat, cash=100000000, commission=0,hedging=True)
    stats = bt.run()

    if plot:
        bt.plot()

    return stats

def full_table(stats, dist = 300,timeframe = 5,tam_stop = 0.0003):



    df_trades = stats['_trades']
    n_trades = stats['# Trades']
    taxa_acerto = stats['Win Rate [%]']
    retorno = stats['Return [%]']

    pontos_total = sum(df_trades['EntryPrice'] - df_trades['ExitPrice'])


    #funciona apenas pra venda

    

    new = pd.DataFrame([[timeframe,dist,tam_stop,n_trades,taxa_acerto,pontos_total,retorno]])
    new.columns = ['Timeframe','Dist','Tam_stop','N_trades','Taxa_acerto','Pontos_total','Retorno']
    
    return new

def print_horario(stats,dist = 300,tam_stop = 0.0003):


    df_trades = stats['_trades']
    retorno = stats['Return [%]']
    #df_trades = df_trades.drop_duplicates('EntryTime')
    df_trades['Hora_h'] = df_trades['EntryTime'].apply(lambda x: x.hour)
    df_trades['resultado_binario'] = df_trades['ReturnPct'].apply(lambda x: 1 if x > 0 else 0)
    pontos = sum(df_trades['EntryPrice'] - df_trades['ExitPrice'])

    print(f'Dist: {dist}-- Tam_stop: {tam_stop} -- pontos_total: {pontos} -- retorno: {retorno}')
    df_new_hora = df_trades[['Hora_h','resultado_binario']]
    df_new_hora = df_trades.groupby(['Hora_h'],as_index=False).agg(qtd_operacoes=('resultado_binario', 'count'), taxa_acerto=('resultado_binario', 'mean'))

    #df_new_hora['pontos_liquido'] = df_new_hora.apply(calc_pontos, axis = 1)
    print(df_new_hora)