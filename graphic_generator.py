#!/usr/bin/env python3

import numpy as np

def graphic(features, plt, title, sequence, colors):

    l = len(features[0])
    x = np.linspace(0,l*5,l,endpoint=True)

    #fig, ax = plt.subplot(3, 4, sequence)
    plt.subplot(3, 4, sequence)
    plt.xlabel('time(sec)')
    plt.ylabel(title)
    
    l2 = ['src','dst']
    l3 = ['min', 'mean', 'max']
    lf = len(features)

    if lf==3:
        l0=l3
    elif lf==2:
        l0=l2
    else:
        l0=['data']

    for i in range(lf):
        
        #if np.max(features[i])>1000:
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        plt.plot(x, features[i], color=colors[i], label=l0[i])

        if lf == 3 and i==1:
            stdv = np.std(features[i])*np.ones(len(features[i]))            
            plt.errorbar(x,features[i], yerr=stdv, fmt='ro')

        plt.legend(loc='upper center', frameon=False, ncol=lf)
        #plt.legend(loc='upper left', frameon=False)
    

def plot(features, plt):
    """
    'features' is a 'matrix' containing 'n' (variable) rows with 34 columns.
    Each  column refer to an attribute generate by compute_statistics.digest
    method.
    The attributes are:
     0: H(ip_src),      1: H(ip_dst),       2: H(ip_proto),    3: H(s_port), 4: H(d_port),
     5: min(pkts),      6: mean(pkts),      7: std(pkts),      8: max(pkts),
     9: min(bytes),    10: mean(bytes),    11: std(bytes),    12: max(bytes),
    13: min(duration), 14: mean(duration), 15: std(duration), 16: max(duration),
    17: min(bps),      18: mean(bps),      19: std(bps),      20: max(bps),
    21: min(pps),      22: mean(pps),      23: std(pps),      24: max(pps),
    25: min(bpp),      26: mean(bpp),      27: std(bpp),      28: max(bpp),
    29: bpf,           30: ppf,            31: dpf,           32: nflows,
    33: fps
    """
    #print("   Plotting graphics")


    f = np.array(features).transpose()
    l = len(f[0])
    x = np.linspace(0, l, l, endpoint=True )

    fig = plt.figure(1)
    fig.clf()
    f2 = plt.gcf()
    DPI = 80
    f2.set_size_inches(1910.0/float(DPI),976.0/float(DPI))
    fig.dpi = DPI
    #fig.figsize=(2100,1220)


    c1 = ['blue']
    c2 = ['blue', 'green']
    c3 = ['blue', 'green', 'black']
    c4 = ['blue', 'green', ['--o','red'],'black']

    graphic([f[0],f[1]], plt, 'H(ip)', 1, c2)
    graphic([f[3],f[4]], plt, 'H(port)', 2, c2)
    graphic([f[5],f[6], f[8]], plt, 'packets', 3, c3)
    graphic([f[9],f[10], f[12]], plt, 'bytes', 4, c3)

    graphic([f[13],f[14], f[16]], plt, 'duration', 5, c3)
    graphic([f[17],f[18], f[20]], plt, 'bytes/sec', 6, c3)
    graphic([f[21],f[22], f[24]], plt, 'packets/sec', 7, c3)
    graphic([f[25],f[26], f[28]], plt, 'bytes/packets', 8, c3)

    graphic([f[29]], plt, 'bytes/flow', 9, c1)
    graphic([f[30]], plt, 'packets/flow', 10, c1)
    graphic([f[31]], plt, 'flow duration', 11, c1)
    graphic([f[33]], plt, 'flows/sec', 12, c1)
    


    #plt.show()

    #print(features)
