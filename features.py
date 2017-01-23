#!/usr/bin/env python3
import json
import requests
import time
import createdb
import sqlite3
import ipaddress
import compute_statistics
import graphic_generator
import matplotlib.pyplot as plt
import os
from datetime import datetime

def compose_feature(switch, flow, count):
    match = flow["match"]
    data = ()
    npkt   = int(flow["packet_count"])
    nbytes = int(flow["byte_count"])
    nsec   = int(flow["duration_sec"])

    if npkt > 0 and nsec > 0: # and nbytes>0:
        vlan = 1
        ip_src = int(ipaddress.IPv4Address(match['ipv4_src']))
        ip_dst = int(ipaddress.IPv4Address(match['ipv4_dst']))
        in_port = 0 if match["in_port"] == "local" else int(match["in_port"])
        data += (count, int(flow["cookie"]), switch, in_port)
        data += (match["eth_src"], match["eth_dst"])
        data += (int(match["eth_type"], 16), vlan)
        data += (ip_src, ip_dst)

        if 'ip_proto' in match:
            if match['ip_proto'] == '0x6':
                data += (0x6, int(match['tcp_src']), int(match['tcp_dst']))
            elif match['ip_proto'] == '0x11':
                data += (0x11, int(match['udp_src']), int(match['udp_dst']))
        else:
            data += (0, 0, 0)

        data += (npkt, nbytes, nsec)

    return data


def extract_features(conn, count, switch_flows):
    """ Save the all flows in database and generate a matrix of unique
        flows to compute a features vector
    """

    sql  = "insert into flows (sequence, cookie,dpid,in_port,dl_src,dl_dst,type,"
    sql += "vlan,ip_src,ip_dst,ip_proto,s_port,d_port,pkts,bytes,duration) "
    sql += "values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
    list_features = []
    cookies = []
    db_features = []
    for s in switch_flows:
        for flow in switch_flows[s]['flows']:
            match = flow["match"]
            eth_type = ["0x800", "0x8100"]
            if 'eth_type' in match and match["eth_type"] in eth_type:
                data = compose_feature(s, flow, count)
                if data:
                    db_features.append(data)

                    if flow["cookie"] not in cookies:
                        cookies.append(flow["cookie"])
                        list_features.append(data[2:])
    try:
        conn.executemany(sql, db_features)
        conn.commit()
        print(' ' * 3 + str(len(db_features)) + " registers inserted")
    except:
        print("Was not possible insert " + data + "into database.")

    return list_features


def get_json(host):
    url = "http://" + host + ":8080/wm/core/switch/all/flow/json"
    try:
        response = requests.get(url)
        switch_flows = json.loads(response.content.decode("utf-8"))
        return switch_flows
    except requests.ConnectionError as e:
        print("Was not possible to connect to server " + host)
        print(e)
        return None


def compute_features(index, host='localhost', stime=5, rounds=5, prefix="local", save=False):
    db_name = createdb.create_db()
    print("DB_Name: " + db_name)
    count = 1
    with sqlite3.connect(db_name, detect_types=sqlite3.PARSE_COLNAMES) as conn:
        list_features = []
        while count <= rounds:
            print('\n***Round: %d\n   Getting flows informations:' % count)
            switch_flows = get_json(host)
            if switch_flows:
                try:
                    features = extract_features(conn, count, switch_flows)

                    # Compute the statistics and stores the summary
                    if features:
                        digest = compute_statistics.digest(features, stime)
                        list_features.append(digest)
                        #graphic_generator.plot(list_features, plt)
                        #if count==100: plt.show()
                    #count += 1
                except KeyboardInterrupt:
                    print("\nKeyboard interruption")
                    conn.close()
                    exit(1)
            
            count += 1
            time.sleep(stime)
        graphic_generator.plot(list_features, plt)
        #plt.show()
        if save:
            rootdir=os.path.dirname(os.path.abspath(__file__))      
            #end = str(datetime.now()).replace('-','').replace(' ','-').replace(':','')[2:13]
            dtime = str(datetime.now()).replace('-','').replace(':','')
            end_date = dtime[2:8]
            end_time = dtime[9:15]
            fig_dir = os.path.join(rootdir,prefix,end_date)
            if not os.path.exists(fig_dir):
                os.makedirs(fig_dir)
            fig_name = 'fig%s.png'%end_time
            plt.savefig( os.path.join(fig_dir,fig_name) )
