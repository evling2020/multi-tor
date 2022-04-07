#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Project : tools
# @File : init.py
# @Software: PyCharm
# @Author : 易雾君
# @Email : evling2020@gmail.com
# @公众号 : 易雾山庄
# @Site : https://www.evling.tech
# @Describe : 家庭基建，生活乐享. 
# @Time : 2022/3/22 8:24 PM

import os
import shutil
import yaml


port_num = int(os.getenv('TOR_NUM')) if os.getenv('TOR_NUM') else 10
port_num = port_num if port_num < 65535 else 65534
tor_rotate_time = int(os.getenv('TOR_ROTATE_TIME')) if os.getenv('TOR_ROTATE_TIME') else 300
in_proxy_interval = int(os.getenv('IN_PROXY_INTERVAL')) if os.getenv('IN_PROXY_INTERVAL') else 300
in_proxy_port = 8080
in_proxy_user = os.getenv('IN_PROXY_USER')
in_proxy_pass = os.getenv('IN_PROXY_PASS')
in_program_bin = '/usr/bin/in_program'
in_program_dir = '/data/in_program/'
in_conf = os.path.join(in_program_dir, 'proxy.yaml')

tor_bin = '/usr/bin/tor'
tor_data_dir = '/data/tor/'
run_script = '/data/run.sh'

command_lines = []

if not  os.path.exists('/data'):
    os.mkdir('/data')

if not os.path.exists(in_program_dir):
    os.mkdir(in_program_dir)

if os.path.exists(tor_data_dir):
    shutil.rmtree(tor_data_dir)
os.mkdir(tor_data_dir)

def build_conf(port_list=[], in_conf='/data/in_program/proxy.yaml', username=None, passwd=None):
    base_conf_content = f'''
        mixed-port: {in_proxy_port}
        allow-lan: true
        bind-address: "*"
        mode: rule
        log-level: info
        rules:
          - MATCH,Load_Balance
    '''
    config_dic = yaml.load(base_conf_content, Loader=yaml.FullLoader)
    if 'proxies' not in config_dic:
        config_dic['proxies'] = []
    if 'proxy-groups' not in config_dic:
        config_dic['proxy-groups'] = []

    proxy_group = {
        'name': 'Load_Balance',
        'type': 'load-balance',
        'strategy': 'round-robin',
        'url': 'http://www.gstatic.com/generate_204',
        'interval': in_proxy_interval,
        'proxies': []
    }
    for port in port_list:
        proxy_name = f'tor-{port}'
        proxy_type = 'socks5'
        proxy_server = '127.0.0.1'
        proxy_port = port
        proxy_group['proxies'].append(proxy_name)
        node = {'name': proxy_name,
                'type': proxy_type,
                'server': proxy_server,
                'port': proxy_port
                }
        config_dic['proxies'].append(node)
    config_dic['proxy-groups'].append(proxy_group)
    if username is not None and passwd is not None:
        config_dic['authentication'] =[f'{username}:{passwd}']
    with open(in_conf, 'w', encoding='utf-8') as f:
        yaml.dump(config_dic, f, allow_unicode=True, sort_keys=False)
        f.close()

port_list = [x for x in range(1, port_num+1)]
if in_proxy_port in port_list:
    port_list.pop(in_proxy_port)
    port_list.append(port_num+1)

for port in port_list:
    tmp_tor_data_dir = os.path.join(tor_data_dir, f'tor-{port}')
    if os.path.exists(tmp_tor_data_dir):
        shutil.rmtree(tmp_tor_data_dir)
    os.mkdir(tmp_tor_data_dir)
    tmp_tor_conf = os.path.join(tmp_tor_data_dir, 'torrc')
    with open(tmp_tor_conf, 'w') as f:
        f.write(f'''SOCKSPort 127.0.0.1:{port}
DataDirectory {tmp_tor_data_dir}
#VirtualAddrNetworkIPv4 10.192.0.0/10
AutomapHostsOnResolve 1
#TransPort 0.0.0.0:9140
#DNSPort 0.0.0.0:9053
MaxCircuitDirtiness {tor_rotate_time}
''')
        f.close()
    command_lines.append(f'{tor_bin} -f {tmp_tor_conf} &')


build_conf(port_list, in_conf=in_conf, in_proxy_user, in_proxy_pass)
command_lines.append('sleep 30')
command_lines.append(f'{in_program_bin} -f {in_conf}')

with open(run_script, 'w') as f:
    f.write('\n'.join(command_lines))
    f.close()



