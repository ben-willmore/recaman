'''
Plot generalized Recaman sequences in Numberphile-style
'''

import numpy as np
import matplotlib.pyplot as plt

def recaman(num, orig=0, start=1, skip=1):
    '''
    orig: the first number in the list
    start: size of the first jump
    skip: how mmuch the jump will increase each time
    '''
    lst = [orig]
    n = start
    while len(lst) <= num:
        yield lst[-1]
        if lst[-1]-n >= 0 and lst[-1]-n not in lst:
            lst.append(lst[-1]-n)
        else:
            lst.append(lst[-1]+n)
        n = n + skip

def semicircle(mn, mx, n_segments=51):
    d = n_segments
    rev = mn > mx
    if rev:
        mn2 = mx
        mx = mn
        mn = mn2
    th = np.arange(np.pi, 0 - np.pi/d/2, -np.pi/d)
    c = (mn + mx)/2
    r = (mx - mn)/2
    x = np.zeros(th.shape)+10
    y = np.zeros(th.shape)+10
    for i in range(0, len(th)):
        x[i] = c + r*np.cos(th[i])
        y[i] = r*np.sin(th[i])
    if rev:
        x = x[::-1]
        y = y[::-1]

    return x, y

def draw_recaman(n, orig=0, start=0, skip=1, scale=1, offset=0, stop_approx=False,
                 remove_last=False, new_plot=True, linewidth=1.5):
    '''
    n, orig, start, skip: parameters for recaman()
    scale, offset: multiplier and constant offset for plotting
    stop_approx: True -> stop the sequence before a big jump to the right, rather than exactly
       at the nth term
    remove_last: True -> if stop_approx==True, stop one term earlier than normal (in many cases,
    this means that the end of the line is less noticeable
    '''
    r = list(recaman(max(n*4, 30), orig=orig, start=start, skip=skip))
    if stop_approx:
        mx = np.zeros(len(r))
        mx_skip = np.zeros(len(r))
        for i in range(len(r)):
            mx[i] = np.max(r[:i+1])
        dff = np.diff(mx) > 2
        dff[:n-1] = False
        last_chosen = np.where(dff)[0][0]-1
        if remove_last:
            r = r[:min(last_chosen+1, len(r))]
        else:
            r = r[:min(last_chosen+2, len(r))]
    else:
        r = r[:n]
    n = len(r)-1
    flip = -1
    x = np.zeros((0))
    y = np.zeros((0))
    for i in range(0, n):
        nx, ny = semicircle(r[i], r[i+1])
        x = np.concatenate((x, nx))
        y = np.concatenate((y, flip * ny))
        flip = -flip
    x = x*scale+offset
    y = y*scale
    if new_plot:
        plt.figure(figsize=(12, 6))
    plt.plot(x, y, zorder=10000000-n, linewidth=linewidth)
    plt.axis('equal')
    plt.axis('off')
    return n+1
