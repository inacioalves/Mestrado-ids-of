#!/usr/bin/env python3

#import scipy.stats as stats
import numpy as np
#from scipy import median
#from math import log


def entropy(data):
    if not data:
        return 0

    entropy = 0
    l = len(data)
    for v in set(data):
        px = data.count(v) / l
        #entropy -= px * np.log2(px, 2)
        entropy -= px * np.log2(px)
    return entropy

def complement(fbt):
    fbt = np.array(fbt)
    nflows = len(fbt[0])

    bps = np.divide(fbt[1],fbt[2]) #bytes/sec
    pps = np.divide(fbt[0],fbt[2]) #packets/sec
    bpp = np.divide(fbt[1],fbt[0]) #bytes/packet

    bpf = np.sum(fbt[1])/nflows # bytes/flow
    ppf = np.sum(fbt[0])/nflows # packets/flow
    dpf = np.sum(fbt[2])/nflows # durarion/flow

    s = (np.min(bps), np.mean(bps), np.std(bps), np.max(bps),
         np.min(pps), np.mean(pps), np.std(pps), np.max(pps),
         np.min(bpp), np.mean(bpp), np.std(bpp), np.max(bpp),
         bpf, ppf, dpf, nflows, 
        )
    print("   %d unique flows\n***"% nflows)
    return s

def digest(features, stime):
    """
    Return a tuple containing a 'summary' of the features.
        features: a list of flow's features containing some descriptive attributes
                  and some numerical atributes
    The summary consists of 'entropy' of descriptive attributes and min, mean, stdv
    and max values of numerical values. Some attributes are not summarized, but
    continues in the list for future use.

    The attributes are:
    [ 0: dpid,   1: in_port, 2: dl_src,   3: dl_dst,  4: type,  5: vlan
      6: ip_src, 7: ip_dst,  8: ip_proto, 9: s_port, 10: d_port
     11: pkts, 12: bytes, 13: duration ]
    """

    fbt = list(zip(*features)) # features by type
    summary = (entropy(fbt[6]), entropy(fbt[7]), entropy(fbt[8]),
        entropy(fbt[9]), entropy(fbt[10]),
        np.min(fbt[11]), np.mean(fbt[11]), np.std(fbt[11]), np.max(fbt[11]),
        np.min(fbt[12]), np.mean(fbt[12]), np.std(fbt[12]), np.max(fbt[12]),
        np.min(fbt[13]), np.mean(fbt[13]), np.std(fbt[13]), np.max(fbt[13]),
    ) + complement(fbt[-3:]) + ( len(features)/stime, )

    #print("\nsummary: ",len(summary))
    #print(summary)
    return(summary)
