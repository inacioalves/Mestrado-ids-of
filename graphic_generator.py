#!/usr/bin/env python3

import numpy as np
#import matplotlib.pyplot as plt

def graphic(features, plt, title, sequence, colors):

    l = len(features[0])
    x = np.linspace(0,l*5,l,endpoint=True)

    plt.subplot(3, 4, sequence)
    plt.title(title)

    # print(features)
    # print(colors)

    for i in range(len(features)):        
        if np.max(features[i])>10000:
        #    #ax.ticklabel_format(style='sci',axis='y')
            plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        if type(colors[i])==str:
            plt.plot(x, features[i], color=colors[i])
        else:
            plt.errorbar(x,features[i],fmt='--o', color=colors[i][1])
            #plt.plot(x, features[i], fmt=colors[i][0], color=colors[i][1])


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
    fig.dpi=80

    c1 = ['blue']
    c2 = ['blue', 'green']
    c4 = ['blue', 'green', ['--o','red'],'black']

    #print(dir(fig))

    # plt.subplot(3, 4, 1)
    # plt.title('H(ip_src)')
    # plt.plot(x, f[0], color="blue")
    # plt.plot(x, f[1], color="green")
    graphic([f[0],f[1]], plt, 'H(ip)', 1, c2)
    

    # plt.subplot(3, 4, 2)
    # plt.title('H(port)')
    # plt.plot(x, f[3], color="blue")
    # plt.plot(x, f[4], color="green")
    graphic([f[3],f[4]], plt, 'H(port)', 2, c2)

    # plt.subplot(3, 4, 3)
    # plt.title('packets')
    # plt.plot(x, f[5], color="green")
    # plt.plot(x, f[6], color="blue")
    # plt.errorbar(x,f[7],fmt='--o', color="red")
    # plt.plot(x, f[8], color="black")
    graphic([f[5],f[6], f[7], f[8]], plt, 'packets', 3, c4)
    

    # plt.subplot(3, 4, 4)
    # plt.title('bytes')
    # plt.plot(x, f[9], color="green")
    # plt.plot(x, f[10], color="blue")
    # plt.errorbar(x,f[11],fmt='--o', color="red")
    # plt.plot(x, f[12], color="black")
    graphic([f[9],f[10], f[11], f[12]], plt, 'bytes', 4, c4)

    # plt.subplot(3, 4, 5)
    # plt.title('duration')
    # plt.plot(x, f[13], color="green")
    # plt.plot(x, f[14], color="blue")
    # plt.errorbar(x,f[15],fmt='--o', color="red")
    # plt.plot(x, f[16], color="black")
    graphic([f[14],f[15], f[15], f[16]], plt, 'duration', 5, c4)

    # plt.subplot(3, 4, 6)
    # plt.title('bytes/sec')
    # plt.plot(x, f[17], color="green")
    # plt.plot(x, f[18], color="blue")
    # plt.errorbar(x,f[19],fmt='--o', color="red")
    # plt.plot(x, f[20], color="black")
    graphic([f[17],f[18], f[19], f[20]], plt, 'bytes/sec', 6, c4)

    # plt.subplot(3, 4, 7)
    # plt.title('packets/sec')
    # plt.plot(x, f[21], color="green")
    # plt.plot(x, f[22], color="blue")
    # plt.errorbar(x,f[23],fmt='--o', color="red")
    # plt.plot(x, f[24], color="black")
    graphic([f[21],f[22], f[23], f[24]], plt, 'packets/sec', 7, c4)

    # plt.subplot(3, 4, 8)
    # plt.title('bytes/packet')
    # plt.plot(x, f[25], color="green")
    # plt.plot(x, f[26], color="blue")
    # plt.errorbar(x,f[27],fmt='--o', color="red")
    # plt.plot(x, f[28], color="black")
    graphic([f[25],f[26], f[27], f[28]], plt, 'bytes/packets', 8, c4)

    # plt.subplot(3, 4, 9)
    # plt.title('bytes/flow')
    # plt.plot(x, f[29], color="green")
    graphic([f[29]], plt, 'bytes/flow', 9, c1)

    # plt.subplot(3, 4, 10)
    # plt.title('packets/flow')
    # plt.plot(x, f[30], color="green")
    graphic([f[30]], plt, 'packets/flow', 10, c1)

    # plt.subplot(3, 4, 11)
    # plt.title('flow duration')
    # plt.plot(x, f[31], color="green")
    graphic([f[31]], plt, 'flow duration', 11, c1)

    # plt.subplot(3, 4, 12)
    # plt.title('flows/sec')
    # plt.plot(x, f[32], color="green")
    graphic([f[32]], plt, 'flows/sec', 12, c1)
    


    #plt.show()

    #print(features)
