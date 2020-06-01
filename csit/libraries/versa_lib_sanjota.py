#!/usr/bin/env python
import inspect
import os
from ipcalc import IP


# frame = inspect.stack()[1]
# module = inspect.getmodule(frame[0])
# caller_filename = module.__file__
#
# print caller_filename





# from os.path import dirname, realpath, sep, pardir
# import sys
# import os
# print "*" * 20
# # print dirname(realpath(__file__))
# # sys.path.append(dirname(realpath(__file__)))
# # sys.path.append(realpath(__file__))
# sys.path.append(os.getcwd())
# print sys.path
import time
import pandas as pd
from netmiko import redispatch
from netmiko import ConnectHandler
import os
import requests
import sys
from Variables import *
# from csit.libraries.Variables import *
import json
from jinja2 import Template
from jinja2 import Environment, FileSystemLoader, meta
import ipaddress
import ipcalc
import itertools as it
from StringIO import StringIO
import re
from datetime import datetime
from CalcIPV4Network import CalcIPv4Network
from robot.api import logger
import math
import logging
import logging.handlers
import errno
import csv
import textfsm
import yaml
currtime = str(datetime.now())
currtime = currtime.replace(" ", "_").replace(":", "_").replace("-", "_").replace(".", "_")
from ast import literal_eval
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def try_literal_eval(s):
    try:
        return literal_eval(s)
    except ValueError:
        return s



if __name__ == "__main__":
    fileDir = os.path.dirname(os.path.dirname(os.path.realpath('__file__')))
else:
    fileDir = os.path.dirname(os.path.realpath('__file__'))

curr_file_dir = os.path.dirname(os.path.dirname(os.path.realpath('__file__')))


#print fileDir

# if "*.robot" not in caller_filename:
logfile_dir = os.path.dirname(os.path.dirname(os.path.realpath('__file__'))) + "/LOGS/"+ currtime + "/"
if not os.path.exists(os.path.dirname(logfile_dir)):
    try:
        os.mkdir(os.path.dirname(logfile_dir))
    except OSError as exc:  # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise

# logger.info(fileDir, also_console=True)

# def setup_logger(name, filename, level=logging.DEBUG):
#     formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
#     formatter1 = logging.Formatter("%(message)s")
#     console = logging.StreamHandler()
#     console.setLevel(logging.DEBUG)
#     console.setFormatter(formatter1)
#     logging.getLogger('').addHandler(console)
#     log_file = logfile_dir + filename  + ".log"
#     handler = logging.FileHandler(log_file)
#     handler.setFormatter(formatter1)
#     logger = logging.getLogger(name)
#     logger.setLevel(level)
#     logger.addHandler(handler)
#     logger = logging.getLogger(name)
#     return logger

def write_result_from_dict(results):
    data_header = ['Device_name', 'Config_Result']
    with open(logfile_dir + 'RESULT.csv', 'w') as file_writer:
        writer = csv.writer(file_writer)
        writer.writerow(data_header)
        for k, v in results.items():
            writer.writerow([k, v])
    print "Result stored in : " + logfile_dir + 'RESULT.csv'



file_loader = FileSystemLoader(fileDir +'/csit/libraries/J2_temps/PROD_CONFIG')
if __name__ == "__main__":
    file_loader = FileSystemLoader('./J2_temps')
env = Environment(loader=file_loader)



class VersaLib:
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self, device_name, **kwargs):
        self.ctlr_dict =  ctlr_dict
        self.ctlr_list =  ctlr_list
        self.staging_servers_dict = staging_servers_dict
        self.LCC_dict = LCC_dict
        self.gw_dict =  gw_dict
        self.gw_list =  gw_list
        self.SOLUTIONS_list = SOLUTIONS_list
        self.log_collector = log_collector
        self.TRACK_MANAGEMENT_SUBNET = TRACK_MANAGEMENT_SUBNET
        self.ndb = {}
        if kwargs is not None:
            for k, v in kwargs.iteritems(): exec("self."+ k+'=v')
        if 'topofile' in self.__dict__:
            if ".csv" in self.topofile:
                csv_data_read = pd.read_csv(curr_file_dir + "/Topology/" + self.topofile, dtype=object)
                self.Device_name = device_name
                data = csv_data_read.loc[csv_data_read['Device_name'] == device_name]
                csv_dict = data.set_index('Device_name').T.to_dict()
                for k, v in csv_dict[self.Device_name].iteritems():
                    if isinstance(v, float):
                        if math.isnan(v):
                            continue
                    exec("self."+ k+'=v')
            elif '.yml' in self.topofile:
                print self.topofile
                with open(curr_file_dir + "/Topology/" + self.topofile) as fp1:
                    devices_dict = yaml.safe_load(fp1)
                device_dict = devices_dict[device_name]
                self.Device_name = device_name
                for k, v in device_dict.iteritems():
                    print type(v)
                    if v == None:
                        continue
                    exec("self."+ k+'=v')

            for k, v in self.__dict__.iteritems():
                if isinstance(v, str):
                    if "temporgname" in v:
                        v = v.replace("temporgname", str(self.ORG_NAME))
                    if "temporgid" in v:
                        v = v.replace("temporgid", str(self.ORG_ID))
                    if "tempdevicename" in v:
                        v = v.replace("tempdevicename", str(self.Device_name))
                    if re.search("^{", v):
                        v = try_literal_eval(v)
                    exec ("self." + k + '=v')
            # print self.__dict__
            self.vlans = []
            if 'START_VLAN' in self.__dict__:
                self.START_VLAN = int(self.START_VLAN)
                self.set_network_items(self.START_LAN_IP_SUBNET)
                if 'peer_Start_lan_ip_subnet' in self.__dict__:
                    self.set_peer_network_items(self.peer_Start_lan_ip_subnet)
            if 'ORG_ID' in self.__dict__ :
                self.ORG_ID = int(self.ORG_ID)
                self.vxlan_tvi_interface = self.ORG_ID * 2
                self.esp_tvi_interface = self.ORG_ID * 2 + 1
                self.start_vrf_id = self.ORG_ID * 10 + 120
                self.ptvi_intf_wc1 = "ptvi" + str(self.ORG_ID * 2)
                self.ptvi_intf_wc2 = "ptvi" + str(self.ORG_ID * 2 + 1)
            if 'Site_id' in self.__dict__:
                self.Site_id = int(self.Site_id)
            if 'LCC' in self.__dict__:
                self.LCC = int(self.LCC)
            #print 'LCC' in self.__dict__
        if 'device_type' in self.__dict__:
            if self.device_type == 'versa_director':
                self.vdhead = 'https://' + self.mgmt_ip + ':9182'
                self.vddata_dict = self.__dict__
            else:
                if ".csv" in self.topofile:
                    self.vddata = csv_data_read.loc[csv_data_read['device_type'] == 'versa_director']
                    self.vdcsv_dict = self.vddata.set_index('Device_name').T.to_dict()
                    self.vddata_dict = {}
                    self.vdcsv_dict['VD1']['Device_name'] = 'VD1'
                    for i, k  in self.vdcsv_dict['VD1'].iteritems():
                        self.vddata_dict[i] = k
                elif ".yml" in self.topofile:
                    self.vdcsv_dict = devices_dict['VD1']
                    self.vddata_dict = {}
                    self.vdcsv_dict['VD1']['Device_name'] = 'VD1'
                    for i, k in self.vdcsv_dict['VD1'].iteritems():
                        self.vddata_dict[i] = k
                self.vdhead = 'https://' + self.vddata_dict['mgmt_ip'] + ':9182'

    def get_data_dict(self):
        return self.__dict__

    # def set_variable(self, var, val):
    #     self.var = val

    def set_vlan_items(self, START_VLAN):
        self.lan_vlan = []
        # self.data_dict['lan_vlan'] = []
        self.lan = {}
        vlan_id_genr = (i for i in range(START_VLAN, START_VLAN+ int(self.NO_OF_VRFS) + 1))
        for i in range(1, int(self.NO_OF_VRFS) + 1):
            self.lan[i] = {}
            lan_value = next(vlan_id_genr)
            self.lan_vlan.append(lan_value)
            # self.data_dict['lan_vlan'].append(lan_value)
            self.lan[i]['vlan'] = lan_value
        return

    def set_network_items(self, START_LAN_IP_SUBNET):
        self.set_vlan_items(self.START_VLAN)
        network = CalcIPv4Network(unicode(START_LAN_IP_SUBNET))
        network_address = (network + (i + 1) * network.size() for i in it.count())
        nw_addr = network
        for i in range(1, int(self.NO_OF_VRFS) + 1):
            self.lan[i]['nw'] = nw_addr
            n = ipaddress.ip_network(nw_addr)
            self.lan[i]['first_host'] = str(n[1])
            print ip.to_ipv6(ip)
            self.lan[i]['second_host'] = str(n[2])
            self.lan[i]['third_host'] = str(n[3])
            if n.prefixlen < 30:
                self.lan[i]['fourth_host'] = str(n[4])
                self.lan[i]['fifth_host'] = str(n[5])
                self.lan[i]['sixth_host'] = str(n[6])
                self.lan[i]['seventh_host'] = str(n[7])
                self.lan[i]['eighth_host'] = str(n[8])
                self.lan[i]['ninth_host'] = str(n[9])
                self.lan[i]['tenth_host'] = str(n[10])
            self.lan[i]['netmask'] = str(n.netmask)
            self.lan[i]['prefixlen'] = str(n.prefixlen)
            self.lan[i]['nw_with_prefixlen'] = str(n.with_prefixlen)
            nw_addr = next(network_address)
        return self.lan





    def set_peer_network_items(self, START_LAN_IP_SUBNET):
        network = CalcIPv4Network(unicode(START_LAN_IP_SUBNET))
        network_address = (network + (i + 1) * network.size() for i in it.count())
        nw_addr = network
        for i in range(1, 11):
            self.lan[i]['peer_nw'] = nw_addr
            n = ipaddress.ip_network(nw_addr)
            self.lan[i]['peer_first_host'] = str(n[1])
            self.lan[i]['peer_second_host'] = str(n[2])
            self.lan[i]['peer_netmask'] = str(n.netmask)
            nw_addr = next(network_address)
        return



    def show_session_sdwan_detail(self, **kwargs):
        cmd = "show orgs org " + self.ORG_NAME + " sessions sdwan detail"
        print cmd
        # output = self.cnc.send_command_expect(cmd, expect_string=">", strip_prompt=False, strip_command=False)
        output = """hhhhhhhhhhhhhhhhh"""
        return output



def main():
    cpe1 = VersaLib('CPE27-SIN-SINGLE-CPE-INTONLY-IPC00190', topofile="Devices.csv")
    print cpe1
    print cpe1.show_session_sdwan_detail()

if __name__ == "__main__":
    main()