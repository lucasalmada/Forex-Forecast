import pandas as pd


"""Detect peaks in data based on their amplitude and other features."""

import numpy as np



def detect_peaks(x, mph=None, mpd=1, threshold=0, edge='rising',
                 kpsh=False, valley=False, show=False, ax=None, title=True):


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


    return ind






def calculate_peak(df, dist = 300, plot = False,tam_stop = 0.0002, valley = False):

    x = df['Close']
    ind = detect_peaks(x,show=False,mpd = dist,valley = valley)
    
    lista_signal = [0] * len(df)
    lista_stop = [0] * len(df)
    lista_tp = [0] * len(df)
    lista_close = df['Close'].values

    if not valley:

        for i in ind:

            try:
                tamanho_stop = lista_close[i] - lista_close[i+2]
                if tamanho_stop > tam_stop:
                    lista_signal[i+2] = 2
                    lista_stop[i+2] = lista_close[i]
                    lista_tp[i+2] = lista_close[i+2] - (tamanho_stop)
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



    df['acao'] = df['signal'].apply(lambda x: 'sell' if x == 2 else 'call' if x == 1 else 0)

    return df.tail(1)



