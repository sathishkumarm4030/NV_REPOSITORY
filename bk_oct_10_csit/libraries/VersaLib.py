#!/usr/bin/env python

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
            csv_data_read = pd.read_csv(curr_file_dir + "/Topology/" + self.topofile, dtype=object)
            self.Device_name = device_name
            data = csv_data_read.loc[csv_data_read['Device_name'] == device_name]
            csv_dict = data.set_index('Device_name').T.to_dict()
            for k, v in csv_dict[self.Device_name].iteritems():
                if isinstance(v, float):
                    if math.isnan(v):
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
                self.vddata = csv_data_read.loc[csv_data_read['device_type'] == 'versa_director']
                self.vdcsv_dict = self.vddata.set_index('Device_name').T.to_dict()
                self.vddata_dict = {}
                self.vdcsv_dict['VD1']['Device_name'] = 'VD1'
                for i, k  in self.vdcsv_dict['VD1'].iteritems():
                    self.vddata_dict[i] = k
                self.vdhead = 'https://' + self.vddata_dict['mgmt_ip'] + ':9182'
        self.main_logger = self.setup_logger(device_name, 'MAIN', level=logging.DEBUG)
        self.curr_file_dir = os.path.dirname(os.path.dirname(os.path.realpath('__file__')))
        # logger.info("intialized", also_console=True)

    def setup_logger(self, name, filename, level=logging.DEBUG):
        # name = self.Device_name
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        formatter1 = logging.Formatter("%(message)s")
        console = logging.StreamHandler()
        if "loglevel" in self.__dict__:
            console.setLevel(logging.DEBUG)
        else:
            console.setLevel(logging.INFO)
        #console.setFormatter(formatter)
        #console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)
        log_file = logfile_dir + filename + ".log"
        handler = logging.FileHandler(log_file)
        handler.setFormatter(formatter)
        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(handler)
        logger = logging.getLogger(name)
        self.logfile = log_file
        return logger


    def create_cpe_data(self):
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
        # if "MPLS" in self.Solution_type:
        #     self.FW_PROFILE = "GENERIC-SFW-TEMPLATE"
        # elif self.WAN2_LIB == "YES" or self.WAN1_LIB == "YES":
        #     self.FW_PROFILE = "COMMON-SFW-TEMPLATE"
        # else:
        #     self.FW_PROFILE = "GENERIC-SFW-TEMPLATE"

        if "SINGLE-CPE-HYBRID" in self.Solution_type:
            if "LIB1" in self.__dict__ and self.LIB1 == "YES":
                self.FW_PROFILE = "COMMON-SFW-TEMPLATE"
            else:
                self.FW_PROFILE = "GENERIC-SFW-TEMPLATE"
        if "SINGLE-CPE-INTERNET-ONLY" in self.Solution_type:
            if self.LIB1 == "YES":
                self.FW_PROFILE = "COMMON-SFW-TEMPLATE"
            else:
                self.FW_PROFILE = "GENERIC-SFW-TEMPLATE"

        if "SINGLE-CPE-MPLS-ONLY" == self.Solution_type:
            self.FW_PROFILE = "GENERIC-SFW-TEMPLATE"

        if "SINGLE-CPE-DUAL-INTERNET" == self.Solution_type:
            if ("LIB1" in self.__dict__ and self.LIB1 == "ACTIVE") or ("LIB2" in self.__dict__ and self.LIB2 == "ACTIVE"):
                self.FW_PROFILE = "COMMON-SFW-TEMPLATE"
            else:
                self.FW_PROFILE = "GENERIC-SFW-TEMPLATE"

            self.WAN1_NAME = WAN_INTERFACES[self.Solution_type]['WAN1']
            self.WAN2_NAME = WAN_INTERFACES[self.Solution_type]['WAN2']
            self.ST_Wan1 = self.WAN1_NAME
            self.ST_Wan2 = self.WAN2_NAME
            if self.LIB1 == "STANDBY" and self.LIB2 == "ACTIVE":
                self.ST_Wan1 = self.WAN2_NAME
                self.ST_Wan2 = self.WAN1_NAME

        if "DUAL-CPE-DUAL-INTERNET" == self.Solution_type:
            self.WAN1_NAME = WAN_INTERFACES[self.Solution_type]['WAN1']
            self.WAN2_NAME = WAN_INTERFACES[self.Solution_type]['WAN2']
            self.ST_Wan1 = self.WAN1_NAME
            self.ST_Wan2 = self.WAN2_NAME
            if self.LIB1 == "STANDBY" and self.LIB2 == "ACTIVE":
                self.ST_Wan1 = self.WAN2_NAME
                self.ST_Wan2 = self.WAN1_NAME
            if self.LIB1 == "ACTIVE" and self.LIB2 == "ACTIVE":
                self.LIB_LOADSHARING = "YES"

        if 'PS_TEMPLATE_NAME' not in self.__dict__:
            self.PS_TEMPLATE_NAME = self.ORG_NAME + "-" + self.NODE + "-PS-" #JAN23-MUM-PS-HS-LIB
            if "SINGLE-CPE-HYBRID" in self.Solution_type:
                self.PS_TEMPLATE_NAME = self.PS_TEMPLATE_NAME + "H"
                if self.WAN2_IP_ALLOC == "DHCP":
                    self.PS_TEMPLATE_NAME = self.PS_TEMPLATE_NAME + "D"
                elif self.WAN2_IP_ALLOC == "STATIC":
                    self.PS_TEMPLATE_NAME = self.PS_TEMPLATE_NAME + "S"
                if "LIB1" in self.__dict__ and self.LIB1 == "YES":
                    self.PS_TEMPLATE_NAME = self.PS_TEMPLATE_NAME + "-LIB"

            if "SINGLE-CPE-INTERNET-ONLY" in self.Solution_type:
                self.PS_TEMPLATE_NAME = self.PS_TEMPLATE_NAME + "I"
                if self.WAN1_IP_ALLOC == "DHCP":
                    self.PS_TEMPLATE_NAME = self.PS_TEMPLATE_NAME + "D"
                elif self.WAN1_IP_ALLOC == "STATIC":
                    self.PS_TEMPLATE_NAME = self.PS_TEMPLATE_NAME + "S"
                if "LIB1" in self.__dict__ and self.LIB1 == "YES":
                    self.PS_TEMPLATE_NAME = self.PS_TEMPLATE_NAME + "-LIB"

            if "DUAL-CPE-DUAL-MPLS" == self.Solution_type:
                if self.DUAL == "PRIMARY":
                    post_staging_temp_name1 =  self.PS_TEMPLATE_NAME + "D"
                    self.PS_TEMPLATE_NAME = post_staging_temp_name1 + "-MOP"
                    self.SECONDARY_PS_TEMPLATE_NAME = post_staging_temp_name1 + "-MOS"
                elif self.DUAL == "SECONDARY":
                    self.SECONDARY_PS_TEMPLATE_NAME = self.PS_TEMPLATE_NAME + "D-MOS"

            if "SINGLE-CPE-DUAL-INTERNET" == self.Solution_type:
                post_staging_temp_name =  self.PS_TEMPLATE_NAME
                if self.WAN1_IP_ALLOC == "DHCP" and self.WAN2_IP_ALLOC == "DHCP":
                    if self.LIB1 == "ACTIVE" and self.LIB2 == "ACTIVE":
                        post_staging_temp_name = post_staging_temp_name + "DID-LIB"
                    elif self.LIB1 == "ACTIVE" and self.LIB2 == "STANDBY":
                        post_staging_temp_name = post_staging_temp_name + "DID-LIB1"
                    elif self.LIB1 == "STANDBY" and self.LIB2 == "ACTIVE":
                        post_staging_temp_name = post_staging_temp_name + "DID-LIB2"
                    else:
                        post_staging_temp_name = post_staging_temp_name + "DID"
                elif self.WAN1_IP_ALLOC == "DHCP" and self.WAN2_IP_ALLOC == "STATIC":
                    if self.LIB1 == "ACTIVE" and self.LIB2 == "ACTIVE":
                        post_staging_temp_name = post_staging_temp_name + "DIDS-LIB"
                    elif self.LIB1 == "ACTIVE" and self.LIB2 == "STANDBY":
                        post_staging_temp_name = post_staging_temp_name + "DIDS-LIB1"
                    elif self.LIB1 == "STANDBY" and self.LIB2 == "ACTIVE":
                        post_staging_temp_name = post_staging_temp_name + "DIDS-LIB2"
                    else:
                        post_staging_temp_name = post_staging_temp_name + "DIDS"
                elif self.WAN1_IP_ALLOC == "STATIC" and self.WAN2_IP_ALLOC == "DHCP":
                    if self.LIB1 == "ACTIVE" and self.LIB2 == "ACTIVE":
                        post_staging_temp_name = post_staging_temp_name + "DISD-LIB"
                    elif self.LIB1 == "ACTIVE" and self.LIB2 == "STANDBY":
                        post_staging_temp_name = post_staging_temp_name + "DISD-LIB1"
                    elif self.LIB1 == "STANDBY" and self.LIB2 == "ACTIVE":
                        post_staging_temp_name = post_staging_temp_name + "DISD-LIB2"
                    else:
                        post_staging_temp_name = post_staging_temp_name + "DISD"
                elif self.WAN1_IP_ALLOC == "STATIC" and self.WAN2_IP_ALLOC == "STATIC":
                    if self.LIB1 == "ACTIVE" and self.LIB2 == "ACTIVE":
                        post_staging_temp_name = post_staging_temp_name + "DIS-LIB"
                    elif self.LIB1 == "ACTIVE" and self.LIB2 == "STANDBY":
                        post_staging_temp_name = post_staging_temp_name + "DIS-LIB1"
                    elif self.LIB1 == "STANDBY" and self.LIB2 == "ACTIVE":
                        post_staging_temp_name = post_staging_temp_name + "DIS-LIB2"
                    else:
                        post_staging_temp_name = post_staging_temp_name + "DIS"
                self.PS_TEMPLATE_NAME = post_staging_temp_name

            if "DUAL-CPE-HYBRID" == self.Solution_type:
                if self.DUAL == "PRIMARY":
                    post_staging_temp_name1 =  self.PS_TEMPLATE_NAME + "D"
                    self.PS_TEMPLATE_NAME = post_staging_temp_name1 + "-MPLS"
                    self.SECONDARY_PS_TEMPLATE_NAME = post_staging_temp_name1 + "-INT"
                elif self.DUAL == "SECONDARY":
                    self.SECONDARY_PS_TEMPLATE_NAME = self.PS_TEMPLATE_NAME + "D-INT"

            if "DUAL-CPE-DUAL-INTERNET" == self.Solution_type:
                post_staging_temp_name =  self.PS_TEMPLATE_NAME
                sec_post_staging_temp_name = self.PS_TEMPLATE_NAME
                # self.WAN1_NAME = WAN_INTERFACES[self.Solution_type]['WAN1']
                # self.WAN2_NAME = WAN_INTERFACES[self.Solution_type]['WAN2']
                # self.ST_Wan1 = self.WAN1_NAME
                # self.ST_Wan2 = self.WAN2_NAME
                if self.WAN1_IP_ALLOC == "DHCP" and self.WAN2_IP_ALLOC == "DHCP":
                    if self.LIB1 == "ACTIVE" and self.LIB2 == "ACTIVE":
                        post_staging_temp_name = post_staging_temp_name + "D-IOD-LIB"
                        secondary_post_staging_temp_name = sec_post_staging_temp_name + "D-IOD-LIB-LS"
                        # self.LIB_LOADSHARING = "YES"
                    elif self.LIB1 == "ACTIVE" and self.LIB2 == "STANDBY":
                        post_staging_temp_name = post_staging_temp_name + "D-IOD-LIB1"
                        secondary_post_staging_temp_name = sec_post_staging_temp_name + "D-IOD-LIB-S"

                    elif self.LIB1 == "STANDBY" and self.LIB2 == "ACTIVE":
                        post_staging_temp_name = post_staging_temp_name + "D-IOD-LIB2"
                        secondary_post_staging_temp_name = sec_post_staging_temp_name + "D-IOD-LIB-A"
                        # self.ST_Wan1 = self.WAN2_NAME
                        # self.ST_Wan2 = self.WAN1_NAME
                    else:
                        post_staging_temp_name = post_staging_temp_name + "DID"
                        secondary_post_staging_temp_name = sec_post_staging_temp_name + "DID-SEC"
                elif self.WAN1_IP_ALLOC == "DHCP" and self.WAN2_IP_ALLOC == "STATIC":
                    if self.LIB1 == "ACTIVE" and self.LIB2 == "ACTIVE":
                        post_staging_temp_name = post_staging_temp_name + "D-IODS-LIB"
                        secondary_post_staging_temp_name = sec_post_staging_temp_name + "D-IODS-LIB-LS"
                        # self.LIB_LOADSHARING = "YES"
                    elif self.LIB1 == "ACTIVE" and self.LIB2 == "STANDBY":
                        post_staging_temp_name = post_staging_temp_name + "D-IODS-LIB1"
                        secondary_post_staging_temp_name = sec_post_staging_temp_name + "D-IODS-LIB-S"
                    elif self.LIB1 == "STANDBY" and self.LIB2 == "ACTIVE":
                        post_staging_temp_name = post_staging_temp_name + "D-IODS-LIB2"
                        secondary_post_staging_temp_name = sec_post_staging_temp_name + "D-IODS-LIB-A"
                        # self.ST_Wan1 = self.WAN2_NAME
                        # self.ST_Wan2 = self.WAN1_NAME
                    else:
                        post_staging_temp_name = post_staging_temp_name + "DIDS"
                        secondary_post_staging_temp_name = sec_post_staging_temp_name + "DIDS-SEC"
                elif self.WAN1_IP_ALLOC == "STATIC" and self.WAN2_IP_ALLOC == "DHCP":
                    if self.LIB1 == "ACTIVE" and self.LIB2 == "ACTIVE":
                        post_staging_temp_name = post_staging_temp_name + "D-IOSD-LIB"
                        secondary_post_staging_temp_name = sec_post_staging_temp_name + "D-IOSD-LIB-LS"
                        # self.LIB_LOADSHARING = "YES"
                    elif self.LIB1 == "ACTIVE" and self.LIB2 == "STANDBY":
                        post_staging_temp_name = post_staging_temp_name + "D-IOSD-LIB1"
                        secondary_post_staging_temp_name = sec_post_staging_temp_name + "D-IOSD-LIB-A"
                    elif self.LIB1 == "STANDBY" and self.LIB2 == "ACTIVE":
                        post_staging_temp_name = post_staging_temp_name + "D-IOSD-LIB2"
                        secondary_post_staging_temp_name = sec_post_staging_temp_name + "D-IOSD-LIB-S"
                        # self.ST_Wan1 = self.WAN2_NAME
                        # self.ST_Wan2 = self.WAN1_NAME
                    else:
                        post_staging_temp_name = post_staging_temp_name + "DISD"
                        secondary_post_staging_temp_name = sec_post_staging_temp_name + "DISD-SEC"
                elif self.WAN1_IP_ALLOC == "STATIC" and self.WAN2_IP_ALLOC == "STATIC":
                    if self.LIB1 == "ACTIVE" and self.LIB2 == "ACTIVE":
                        post_staging_temp_name = post_staging_temp_name + "D-IOS-LIB"
                        secondary_post_staging_temp_name = sec_post_staging_temp_name + "D-IOS-LIB-LS"
                        self.LIB_LOADSHARING = "YES"
                    elif self.LIB1 == "ACTIVE" and self.LIB2 == "STANDBY":
                        post_staging_temp_name = post_staging_temp_name + "D-IOS-LIB1"
                        secondary_post_staging_temp_name = sec_post_staging_temp_name + "D-IOS-LIB-S"
                    elif self.LIB1 == "STANDBY" and self.LIB2 == "ACTIVE":
                        post_staging_temp_name = post_staging_temp_name + "D-IOS-LIB2"
                        secondary_post_staging_temp_name = sec_post_staging_temp_name + "D-IOS-LIB-A"
                        # self.ST_Wan1 = self.WAN2_NAME
                        # self.ST_Wan2 = self.WAN1_NAME
                    else:
                        post_staging_temp_name = post_staging_temp_name + "DIS"
                        secondary_post_staging_temp_name = sec_post_staging_temp_name + "DIS-SEC"
                self.PS_TEMPLATE_NAME = post_staging_temp_name
                self.SECONDARY_PS_TEMPLATE_NAME = secondary_post_staging_temp_name

            if "SINGLE-CPE-MPLS-ONLY" == self.Solution_type:
                self.PS_TEMPLATE_NAME = self.PS_TEMPLATE_NAME + "M"
        else:
            if "DUAL-CPE" in self.Solution_type:
                # self.SECONDARY_PS_TEMPLATE_NAME = self.PS_TEMPLATE_NAME + "-SEC"
                if "PRIMARY" == self.DUAL:
                    if "SECONDARY_PS_TEMPLATE_NAME" not in self.__dict__:
                        self.main_logger.error("\n\n------->SECONDARY_PS_TEMPLATE_NAME is mandatory field for DUAL PRIMARY CPE. please enter data in csv.\n------->Script exited")
                        exit()
                    # if "DUAL-CPE-DUAL-MPLS" == self.Solution_type:
                    #     post_staging_temp_name1 = self.PS_TEMPLATE_NAME
                    #     self.SECONDARY_PS_TEMPLATE_NAME = post_staging_temp_name1.replace("MOP", "MOS")
                    #
                    # if "DUAL-CPE-HYBRID" == self.Solution_type:
                    #     post_staging_temp_name1 = self.PS_TEMPLATE_NAME
                    #     self.SECONDARY_PS_TEMPLATE_NAME = post_staging_temp_name1.replace("MPLS", "INT")
                elif "SECONDARY" == self.DUAL:
                    self.SECONDARY_PS_TEMPLATE_NAME = self.PS_TEMPLATE_NAME
                    # if "DUAL-CPE-DUAL-MPLS" == self.Solution_type:
                    #     self.SECONDARY_PS_TEMPLATE_NAME = self.PS_TEMPLATE_NAME
                    #
                    # if "DUAL-CPE-HYBRID" == self.Solution_type:
                    #     self.SECONDARY_PS_TEMPLATE_NAME = self.PS_TEMPLATE_NAME


        if 'DG_TEMPLATE_NAME' not in self.__dict__:
            if "DUAL-CPE" in self.Solution_type:
                if "PRIMARY" == self.DUAL:
                    self.DG_TEMPLATE_NAME = self.PS_TEMPLATE_NAME + "-DG"
                    #self.SECONDARY_DG_TEMPLATE_NAME = self.SECONDARY_PS_TEMPLATE_NAME + "-DG"
                elif "SECONDARY" == self.DUAL:
                    self.SECONDARY_DG_TEMPLATE_NAME = self.SECONDARY_PS_TEMPLATE_NAME + "-DG"
            else:
                self.DG_TEMPLATE_NAME = self.PS_TEMPLATE_NAME + "-DG"
        else:
            if "DUAL-CPE" == self.Solution_type:
                if "PRIMARY" == self.DUAL:
                    self.SECONDARY_DG_TEMPLATE_NAME = self.DG_TEMPLATE_NAME
                elif "SECONDARY" == self.DUAL:
                    self.SECONDARY_DG_TEMPLATE_NAME = self.DG_TEMPLATE_NAME

        self.AUTH_KEY = self.Device_name
        self.AUTH_STRING = self.Device_name + "@colt.net"
        self.LCC = self.LCC_dict[self.NODE]
        self.WC1_NAME = ctlr_dict[self.NODE][0]
        self.WC2_NAME = ctlr_dict[self.NODE][1]
        self.GW1_NAME = gw_dict[self.NODE][0]
        self.GW2_NAME = gw_dict[self.NODE][1]
        self.WC1_ESP_IP = self.ndb[self.WC1_NAME]['ESP_IP']
        self.WC2_ESP_IP = self.ndb[self.WC2_NAME]['ESP_IP']
        self.WC1_local_ike_key = self.AUTH_KEY
        self.WC2_local_ike_key = self.AUTH_KEY
        self.WC1_local_ike_id = self.AUTH_STRING
        self.WC2_local_ike_id = self.AUTH_STRING
        self.MGMT_NW_SBNT = MGMT_NW_SBNT
        self.VNF_IPADDRESS1 = VNF_IPADDRESS[0]
        self.VNF_IPADDRESS2 = VNF_IPADDRESS[1]
        self.NO_OF_VRFS = int(self.NO_OF_VRFS)
        self.INTF_LAN_SET = ""
        self.WAN_ST_LAN_SET = ""
        self.LAN_ST_LAN_SET = ""
        self.WAN1_NAME = WAN_INTERFACES[self.Solution_type]['WAN1']
        if 'WAN2' in WAN_INTERFACES[self.Solution_type]:
            self.WAN2_NAME = WAN_INTERFACES[self.Solution_type]['WAN2']
        for i in range(1, self.NO_OF_VRFS + 1):
            self.INTF_LAN_SET += "Intf-LAN" + str(i) + "-Zone " #Intf-LAN1-Zone
            self.WAN_ST_LAN_SET += "W-ST-LAN" + str(i) + "-VRF-INT-WAN "  #W-ST-LAN1-VRF-INT-WAN
            self.LAN_ST_LAN_SET += "L-ST-LAN" + str(i) + "-VRF-INT-WAN "  # L-ST-LAN1-VRF-INT-WAN
        return


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

    # def set_vlan_items(self, START_VLAN):
    #     self.data_dict['lan_vlan'] = []
    #     vlan_id_genr = (i for i in range(START_VLAN, START_VLAN+11))
    #     for i in range(1, 11):
    #         nw_addr = next(vlan_id_genr)
    #         self.data_dict['lan_vlan'].append(nw_addr)
    #     return


    def set_network_items(self, START_LAN_IP_SUBNET):
        self.set_vlan_items(self.START_VLAN)
        # self.data_dict['lan_network'] = {}
        # self.data_dict['lan_first_host'] = {}
        # self.data_dict['lan_second_host'] = {}
        # self.data_dict['lan_netmask'] = {}
        # network = CalcIPv4Network(unicode(START_LAN_IP_SUBNET))
        # network_address = (network + (i + 1) * network.size() for i in it.count())
        # nw_addr = network
        # for i in self.lan_vlan:
        #     self.data_dict['lan_network'][i] = nw_addr
        #     n = ipaddress.ip_network(nw_addr)
        #     self.data_dict['lan_first_host'][i] = str(n[1])
        #     self.data_dict['lan_second_host'][i] = str(n[2])
        #     self.data_dict['lan_netmask'][i] = str(n.netmask)
        #     nw_addr = next(network_address)
        network = CalcIPv4Network(unicode(START_LAN_IP_SUBNET))
        network_address = (network + (i + 1) * network.size() for i in it.count())
        nw_addr = network
        for i in range(1, int(self.NO_OF_VRFS) + 1):
            self.lan[i]['nw'] = nw_addr
            n = ipaddress.ip_network(nw_addr)
            self.lan[i]['first_host'] = str(n[1])
            self.lan[i]['second_host'] = str(n[2])
            self.lan[i]['third_host'] = str(n[3])
            self.lan[i]['netmask'] = str(n.netmask)
            self.lan[i]['prefixlen'] = str(n.prefixlen)
            self.lan[i]['nw_with_prefixlen'] = str(n.with_prefixlen)
            nw_addr = next(network_address)
        return self.lan



    # def set_network_items(self, START_LAN_IP_SUBNET):
    #     self.set_vlan_items(self.START_VLAN)
    #     self.lan_network = {}
    #     self.lan_first_host = {}
    #     self.lan_second_host = {}
    #     self.lan_netmask = {}
    #     network = CalcIPv4Network(unicode(START_LAN_IP_SUBNET))
    #     network_address = (network + (i + 1) * network.size() for i in it.count())
    #     nw_addr = network
    #     for i in range(1, 11):
    #         self.lan[i]['nw'] = nw_addr
    #         n = ipaddress.ip_network(nw_addr)
    #         self.lan[i]['first_host'] = str(n[1])
    #         self.lan[i]['second_host'] = str(n[2])
    #         self.lan[i]['netmask'] = str(n.netmask)
    #         nw_addr = next(network_address)
    #     return


    def set_peer_network_items(self, START_LAN_IP_SUBNET):
        # self.data_dict['peer_lan_network'] = {}
        # self.data_dict['peer_lan_first_host'] = {}
        # self.data_dict['peer_lan_second_host'] = {}
        # self.data_dict['peer_lan_netmask'] = {}
        # network = CalcIPv4Network(unicode(START_LAN_IP_SUBNET))
        # network_address = (network + (i + 1) * network.size() for i in it.count())
        # nw_addr = network
        # for i in self.lan_vlan:
        #     self.data_dict['peer_lan_network'][i] = nw_addr
        #     n = ipaddress.ip_network(nw_addr)
        #     self.data_dict['peer_lan_first_host'][i] = str(n[1])
        #     self.data_dict['peer_lan_second_host'][i] = str(n[2])
        #     self.data_dict['peer_lan_netmask'][i] = str(n.netmask)
        #     nw_addr = next(network_address)
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

    # def set_peer_network_items(self, START_LAN_IP_SUBNET):
    #     self.set_vlan_items(self.START_VLAN)
    #     self.peer_lan_network = {}
    #     self.peer_lan_first_host = {}
    #     self.peer_lan_second_host = {}
    #     self.peer_lan_netmask = {}
    #     network = CalcIPv4Network(unicode(START_LAN_IP_SUBNET))
    #     network_address = (network + (i + 1) * network.size() for i in it.count())
    #     nw_addr = network
    #     for i in self.lan_vlan:
    #         self.peer_lan_network[i] = nw_addr
    #         n = ipaddress.ip_network(nw_addr)
    #         self.peer_lan_first_host[i] = str(n[1])
    #         self.peer_lan_second_host[i] = str(n[2])
    #         self.peer_lan_netmask[i] = str(n.netmask)
    #         nw_addr = next(network_address)
    #     return



    def print_args(self):
        # print(self.data_dict)
        # print self.data_dict
        return self.data_dict

    def login(self, **kwargs):
        if 'vd_login' in kwargs and kwargs['vd_login'] == 'yes':
            device_dict= {
                    'device_type': 'versa',
                    'ip': self.vddata_dict['mgmt_ip'],
                    'username': self.vddata_dict['username'],
                    'password': self.vddata_dict['password'],
                    'port': '22',
                }
        elif self.device_type == 'versa_director':
            device_dict= {
                    'device_type': 'versa',
                    'ip': self.mgmt_ip,
                    'username': self.username,
                    'password': self.password,
                    'port': '22',
                }
        else:
            device_dict = {
                'device_type': 'versa',
                'ip': self.ESP_IP,
                'username': self.username,
                'password': self.password,
                'port': '22',
            }
        self.nc = ConnectHandler(**device_dict)
        if self.device_type != 'linux':
            self.nc.enable()
        self.main_logger.debug(self.nc)
        time.sleep(5)
        self.main_logger.debug("{}: {}".format(self.nc.device_type, self.nc.find_prompt()))
        return self.nc

    def shell_login(self, **kwargs):
        device_dict = {
            'device_type': 'linux',
            'ip': self.mgmt_ip,
            'username': self.username,
            'password': self.password,
            'port': '22',
        }
        self.shell_nc = ConnectHandler(**device_dict)
        self.main_logger.debug(self.shell_nc)
        self.main_logger.debug(self.shell_nc.send_command_expect('sudo bash', expect_string='password'))
        self.main_logger.debug(self.shell_nc.send_command_expect(self.password, expect_string='\~|#'))
        self.main_logger.debug(self.shell_nc.send_command_expect('exit', expect_string='\$|#'))
        # ur = self.shell_nc.send_command_expect('ls -ltr')
        # print ur
        # time.sleep(5)
        self.main_logger.debug("{}: {}".format(self.shell_nc.device_type, self.shell_nc.find_prompt()))
        return self.shell_nc


    def close(self, nc):
        nc.disconnect()
        self.main_logger.debug(str(nc) + " connection closed")

    def cross_login(self):
        self.cnc = self.login(vd_login='yes')
        self.cnc.write_channel("ssh " + self.username + "@" + self.ESP_IP + "\n")
        time.sleep(5)
        output = self.cnc.read_channel()
        print(output)
        if 'assword:' in output:
            self.cnc.write_channel(self.password + "\n")
            time.sleep(5)
            output = self.cnc.read_channel()
            print(output)
        elif 'yes' in output:
            print "am in yes condition"
            self.cnc.write_channel("yes\n")
            time.sleep(5)
            output = self.cnc.read_channel()
            print(output)
            time.sleep(1)
            self.cnc.write_channel(self.data_dict["password"] + "\n")
            time.sleep(5)
            output = self.cnc.read_channel()
            print(output)
        else:
            # cpe_logger.info(output)
            return "VD to CPE " + self.data_dict["ip"] + "ssh Failed."
        # self.cnc.write_channel("cli\n")
        # time.sleep(2)
        # output1 = self.cnc.read_channel()
        # print(output1)
        # time.sleep(2)
        try:
            print("doing redispatch")
            redispatch(self.cnc, device_type='versa')
        except ValueError as Va:
            print(Va)
            print("Not able to get router prompt from CPE" + self.ESP_IP + " CLI. please check")
            return "Redispatch not Success"
        time.sleep(2)
        return self.cnc


    def post_operation(self, url, headers, body=""):
        if body != "":
            json_data = json.loads(body)
        else:
            json_data = ""
        response = requests.post(self.vdhead + url,
                                 auth=(self.vddata_dict['GUIusername'], self.vddata_dict['GUIpassword']),
                                 headers=headers,
                                 json=json_data,
                                 verify=False)
        self.main_logger.debug(response)

        if response.status_code == 200:
            return 'PASS'
        elif response.status_code == 201:
            return 'PASS'
        elif response.status_code == 500:
            self.main_logger.error(response.content)
            return 'FAIL : ' + str(response.content)
        else:
            self.main_logger.error(response.content)
            return 'FAIL : ' + str(response.content)
        # data = response.json()
        # print data
        # taskid = str(data['output']['result']['task']['task-id'])
        # return taskid


    def put_operation(self, url, headers, body=""):
        print body
        if body != "":
            json_data = json.loads(body)
        else:
            json_data = ""
        response = requests.put(self.vdhead + url,
                                 auth=(self.vddata_dict['GUIusername'], self.vddata_dict['GUIpassword']),
                                 headers=headers,
                                 json=json_data,
                                 verify=False)
        print response.content
        print response

        if response.status_code == '200':
            return 'PASS'
        else:
            print response.content
            return 'FAIL'
        # data = response.json()
        # print data
        # taskid = str(data['output']['result']['task']['task-id'])
        # return taskid


    def rest_operation_ret_task_id(self, url, headers, body=""):
        if body != "":
            json_data = json.loads(body)
        else:
            json_data = ""
        response = requests.post(self.vdhead + url,
                                 auth=(self.vddata_dict['GUIusername'], self.vddata_dict['GUIpassword']),
                                 headers=headers,
                                 json=json_data,
                                 verify=False)

        self.main_logger.debug(response.text)
        data = response.json()
        taskid = str(data['TaskResponse']['task-id'])
        return taskid

    def check_task_status(self, taskid):
        response1 = requests.get(self.vdhead + task_url + taskid,
                                 auth=(self.vddata_dict['GUIusername'], self.vddata_dict['GUIpassword']),
                                 headers=headers3,
                                 verify=False)
        data1 = response1.json()
        self.main_logger.debug(data1)
        percent_completed = data1['versa-tasks.task']['versa-tasks.percentage-completion']
        task_result = data1['versa-tasks.task']['versa-tasks.task-status']
        self.main_logger.debug(percent_completed)
        # if task_result == 'FAILED':
        #     error_info = data1['versa-tasks.errormessages']['versa-tasks.errormessage']['versa-tasks.error-message']
        self.main_logger.info("Sleeping for 5 seconds")
        time.sleep(5)
        # return data1['task']['task-status']
        return str(percent_completed)

    def get_task_result(self, taskid):
        response1 = requests.get(self.vdhead + task_url + taskid,
                                 auth=(self.vddata_dict['GUIusername'], self.vddata_dict['GUIpassword']),
                                 headers=headers3,
                                 verify=False)
        self.main_logger.debug(response1.text)
        data1 = response1.json()
        task_result = data1['versa-tasks.task']['versa-tasks.task-status']
        if task_result == 'FAILED':
            error_info = data1['versa-tasks.task']['versa-tasks.errormessages']['versa-tasks.errormessage'][
                'versa-tasks.error-message']
            task_result_cons = task_result + " : " + error_info
            task_desc = data1['versa-tasks.task']['versa-tasks.task-description']
            try:
                get_CPE_name = re.search('Upgrade Appliance: (\S+)', task_desc).group(1)
                self.main_logger.debug(get_CPE_name)
            except AttributeError as AE:
                self.main_logger.debug(AE)
                get_CPE_name = ""
            self.main_logger.debug(get_CPE_name)
            return str(task_result_cons)
        else:
            #return "PASSED : " + str(task_result)
            return "PASS"

    def get_operation(self, url, headers):
        response = requests.get(self.vdhead + url,
                                 auth=(self.vddata_dict['GUIusername'], self.vddata_dict['GUIpassword']),
                                 headers=headers,
                                 verify=False)
        #print response
        return response.json()

    def delete_operation(self, url, headers):
        response = requests.delete(self.vdhead + url,
                                 auth=(self.vddata_dict['GUIusername'], self.vddata_dict['GUIpassword']),
                                 headers=headers,
                                 verify=False)
        print response
        return response

    def check_vsh_status(self):
        pass

    def request_sync_from_device(self, net_connect, device):
        cmd = "request devices device " + device + " sync-from"
        print "CMD>> : " + cmd
        output = net_connect.send_command_expect(cmd, strip_prompt=False, strip_command=False, max_loops=5000)
        print output
        return str(" result true" in output)

    def get_controllers_info(self):
        data1 = self.get_operation(read_controllers_url, headers3)
        print data1
        self.Controllers_list = []
        for i in data1['versanms.sdwan-controller-list']:
            self.Controllers_list.append(i['controllerName'])
        return self.Controllers_list

    def get_controller_detail(self, host_name):

        return

    def get_device_info(self):
        #abc.get_operation(template_url+"/"+ PS_template_name, headers3)
        data1 = self.get_operation(appliance_url, headers3)
        self.dev_dict = {}
        self.dev_present = 'false'
        for i in data1['versanms.ApplianceStatusResult']['appliances']:
            if i['name'] == self.Device_name and i['ipAddress'] == self.ESP_IP:
                # print i
                # if i['ping-status'] != 'REACHABLE':
                #     return "Device Ping failed"
                # if i['sync-status'] != 'IN_SYNC':
                #     return "Device not in Sync"
                self.dev_present = 'true'
                self.dev_dict['name'] = i['name']
                self.dev_dict['uuid'] = i['uuid']
                self.dev_dict['ipAddress'] = i['ipAddress']
                self.dev_dict['ownerOrg'] = i['ownerOrg']
                self.dev_dict['type'] = i['type']
                self.dev_dict['ping_status'] = i['ping-status']
                self.dev_dict['sync_status'] = i['sync-status']
                try:
                    if i['controllers'] != "":
                        self.dev_dict['controllers'] = i['controllers']
                except KeyError as ke:
                    print "Controller Info NIL"
                    self.dev_present = 'false'
                    break
                self.dev_dict['softwareVersion'] = i['softwareVersion']
                try:
                    if i['Hardware'] != "":
                        self.dev_dict['serialNo'] = i['Hardware']['serialNo']
                        self.dev_dict['model'] = i['Hardware']['model']
                        self.dev_dict['packageName'] = i['Hardware']['packageName']
                except KeyError as ke:
                    print i['name']
                    print "Hardware Info NIL"
                    print "sleeping 10 secs"
                    # time.sleep(10)
                    # self.get_device_info()
        if self.dev_present == 'false':
            self.main_logger.info("checking device info in VD.")
            self.main_logger.info("sleeping 60 secs")
            time.sleep(60)
            self.get_device_info()
        return self.dev_dict

    def get_interface_data_from_vd(self, interface_name):
        self.vni_interface_url = "/api/config/devices/device/" + self.Device_name + "/config/interfaces/vni/%22" + interface_name + "%22"
        data1 = self.get_operation(self.vni_interface_url, headers3)
        return data1



    def create_template(self, template_name):
        template = env.get_template(template_name)
        return template.render(self.__dict__)

    def load_and_create_template(self, template_name):
        curr_file_loader = FileSystemLoader(curr_file_dir + "/libraries/J2_temps/ORG_CREATION")
        curr_env = Environment(loader=curr_file_loader)
        template = curr_env.get_template(template_name)
        template = env.get_template(template_name)
        return template.render(self.__dict__)

    def device_config_commands(self, nc_handler, cmds):
        self.main_logger.debug(nc_handler.config_mode(config_command='config private'))
        self.main_logger.debug(nc_handler.check_config_mode())
        for cmd in cmds.split("\n"):
            self.main_logger.debug(nc_handler.send_command_expect(cmd, expect_string='%', strip_prompt=False, strip_command=False))
        self.main_logger.debug(nc_handler.send_command_expect('commit and-quit', expect_string='>', strip_prompt=False, strip_command=False))

    def device_config_commands_wo_split(self, nc_handler, cmds):
        # nc_handler.config_mode(config_command='config private')
        # nc_handler.check_config_mode()
        return nc_handler.send_config_set(config_commands=cmds, strip_prompt=False, strip_command=False, \
                                          max_loops=5000, delay_factor=0.0001, exit_config_mode=False)


    def linux_device_config_commands(self, nc_handler, cmds, expect_string="\$"):
        for cmd in cmds.split("\n"):
            # print cmd
            self.main_logger.info(nc_handler.send_command_expect(cmd, expect_string=expect_string, strip_prompt=False, strip_command=False))

    def cpe_onboard_call(self):
        self.main_logger.info("\nSTEP :ONBOARD CALL")
        curr_file_loader = FileSystemLoader(curr_file_dir + "/libraries/J2_temps/Solution/" + self.Solution_type)
        curr_env = Environment(loader=curr_file_loader)
        self.Staging_command = curr_env.get_template("staging_cpe.j2")
        self.Staging_command_template = self.Staging_command.render(self.__dict__)
        self.main_logger.debug(self.Staging_command_template)
        cpe_shell_login = self.shell_login()
        # print cpe_shell_login.send_command_expect('sudo bash', expect_string='password', strip_prompt=False, strip_command=False)
        # print cpe_shell_login.send_command_expect(self.password, expect_string='#')
        # print cpe_shell_login.send_command_expect('exit', expect_string='\$')
        self.main_logger.debug(cpe_shell_login.send_command_expect('vsh allow-cli', expect_string='password', strip_prompt=False, strip_command=False))
        self.main_logger.debug(cpe_shell_login.send_command_expect(self.password, expect_string='CLI now allowed', strip_prompt=False, strip_command=False))
        self.main_logger.debug(cpe_shell_login.send_command_expect('cli', expect_string='>', strip_prompt=False, strip_command=False))
        self.main_logger.debug(cpe_shell_login.send_command_expect('request erase running-config', expect_string='yes', strip_prompt=False, strip_command=False))
        self.main_logger.debug(cpe_shell_login.send_command_expect('yes', expect_string='\$|#', strip_prompt=False, strip_command=False))
        op = cpe_shell_login.send_command_expect('vsh status', expect_string='\$|#', strip_prompt=False, strip_command=False)
        while "Stopped" in op or "Netconf traffic yet to be allowed" in op:
            self.main_logger.debug("process not up. Please wait for it to come up")
            op = cpe_shell_login.send_command_expect('vsh status', expect_string='\$|#', strip_prompt=False, strip_command=False)
            self.main_logger.debug(op)
            time.sleep(10)
        self.main_logger.debug("After breaking while")
        self.main_logger.debug(cpe_shell_login.send_command_expect('vsh status', expect_string='\$|#'))
        self.main_logger.debug(cpe_shell_login.send_command_expect('vsh show-serialnum', expect_string='\$|#'))
        self.main_logger.debug(cpe_shell_login.send_command_expect('vsh set-serialnum ' + self.Serial_Number,
                                                  expect_string='\$|#'))
        self.main_logger.debug(cpe_shell_login.send_command_expect('vsh show-serialnum', expect_string='\$|#'))
        self.main_logger.debug(cpe_shell_login.send_command_expect(self.Staging_command_template, expect_string='\$|#'))
        time.sleep(20)

#    def create_PS_and_DG(self, Post_staging_template, Device_group_template, PS_main_template_modify):
    def config_devices_vrrp_and_lib(self):
        if "DUAL-CPE" in self.Solution_type:
            self.main_logger.info("\n\nSTEP :CONFIG VRRP TRACK ROUTE & QOS RULE MATCH WAN in Secondary CPE\n")
            curr_file_loader = FileSystemLoader(curr_file_dir + "/libraries/J2_temps/Solution/" + self.Solution_type)
            curr_env = Environment(loader=curr_file_loader)
            if self.DUAL == "PRIMARY":
                self.DEVICE_template_modify = curr_env.get_template("Primary_Device_template_modify.j2")
                self.DEVICE_template_modify_config = self.DEVICE_template_modify.render(self.__dict__)
            elif self.DUAL == "SECONDARY":
                self.DEVICE_template_modify = curr_env.get_template("Secondary_Device_template_modify.j2")
                self.DEVICE_template_modify_config = self.DEVICE_template_modify.render(self.__dict__)
            self.vdnc = self.login(vd_login='yes')
            self.device_config_commands(self.vdnc, self.DEVICE_template_modify_config)
            self.close(self.vdnc)
            self.main_logger.info(">>>>>>>>>> CONFIG VRRP TRACK ROUTE passed. <<<<<<<<<<<")


    def check_org_for_controller(self, controller):
        data1 = self.get_operation(org_url + "/" + self.ORG_NAME, headers3)
        self.main_logger.debug(data1)
        self.main_logger.info("\nSTEP :CHECK ORG is available in Controller " + controller )
        if data1.has_key('versanms.sdwan-org-workflow'):
            if controller not in data1['versanms.sdwan-org-workflow']['controllers']:
                self.main_logger.error("*" * 50)
                self.main_logger.error("Org is not available in node ---> " + self.NODE)
                self.main_logger.error("*" * 50)
                exit()
            else:
                self.main_logger.info("PASS")
        elif data1.has_key('error'):
            self.main_logger.error("*" * 50)
            self.main_logger.error("Org is not Created. pls check VD")
            self.main_logger.error("*" * 50)
            exit()



    def create_and_deploy_poststaging_template(self):
        curr_file_loader = FileSystemLoader(
            curr_file_dir + "/libraries/J2_temps/Solution/" + self.Solution_type)
        curr_env = Environment(loader=curr_file_loader)
        if "DUAL-CPE" in self.Solution_type:
            if self.DUAL == "PRIMARY":
                self.main_logger.info("\nSTEP :POST STAGING TEMPLATE CREATION AND DEPLOYMENT")
                # self.main_logger = self.setup_logger('Versa-director', 'Onboarding')
                curr_file_loader = FileSystemLoader(
                    curr_file_dir + "/libraries/J2_temps/Solution/" + self.Solution_type)
                curr_env = Environment(loader=curr_file_loader)
                ps_template = curr_env.get_template("Post_staging_template.j2")
                self.ps_template_body = ps_template.render(self.__dict__)
                self.main_logger.debug(self.ps_template_body)
                ps_creation_result = self.post_operation(template_url, headers3, self.ps_template_body)
                self.main_logger.debug("\n" + ps_creation_result)
                if 'FAIL' in ps_creation_result:
                    self.main_logger.info(">>>>>>>>>> POST STAGING TEMPLATE CREATION FAILED. <<<<<<<<<<<")
                    exit()
                else:
                    self.main_logger.info(">>>>>>>>>> POST STAGING TEMPLATE CREATION PASSED. <<<<<<<<<<<")
                time.sleep(5)
                Primary_PS_main_template = curr_env.get_template("Primary_PS_main_template_modify.j2")
                #Secondary_PS_main_template = curr_env.get_template("Secondary_PS_main_template_modify.j2")
                Primary_PS_main_template_modify = Primary_PS_main_template.render(self.__dict__)
                #Secondary_PS_main_template_modify = Secondary_PS_main_template.render(self.__dict__)
                ps_deploy_result = self.post_operation(
                    template_url + "/deploy/" + self.PS_TEMPLATE_NAME + "?verifyDiff=true", headers3,
                    self.ps_template_body)
                time.sleep(5)
                self.main_logger.debug("\n" + ps_deploy_result)
                if 'FAIL' in ps_deploy_result:
                    self.main_logger.info(">>>>>>>>>> POST STAGING TEMPLATE DEPLOY FAILED. <<<<<<<<<<<")
                    exit()
                else:
                    self.main_logger.info(">>>>>>>>>> POST STAGING TEMPLATE DEPLOY PASSED. <<<<<<<<<<<")
                time.sleep(5)
                self.main_logger.debug(self.get_operation(template_url + "/" + self.PS_TEMPLATE_NAME, headers3))
                time.sleep(5)
                main_template_modify_result = self.Modify_main_template(Primary_PS_main_template_modify)
                self.main_logger.debug("\n" + main_template_modify_result)
                if 'failed' in main_template_modify_result:
                    self.main_logger.info(">>>>>>>>>> PS MAIN TEMPLATE MODIFY FAILED. <<<<<<<<<<<")
                    exit()
                else:
                    self.main_logger.info(">>>>>>>>>> PS MAIN TEMPLATE MODIFY PASSED. <<<<<<<<<<<")
                time.sleep(5)
            if self.DUAL == "SECONDARY":
                Secondary_PS_main_template = curr_env.get_template("Secondary_PS_main_template_modify.j2")
                Secondary_PS_main_template_modify = Secondary_PS_main_template.render(self.__dict__)
                main_template_modify_result = self.Modify_main_template(Secondary_PS_main_template_modify)
                self.main_logger.debug("\n" + main_template_modify_result)
                if 'failed' in main_template_modify_result:
                    self.main_logger.info(">>>>>>>>>> Secondary PS MAIN TEMPLATE MODIFY FAILED. <<<<<<<<<<<")
                    exit()
                else:
                    self.main_logger.info(">>>>>>>>>> Secondary PS MAIN TEMPLATE MODIFY PASSED. <<<<<<<<<<<")
                time.sleep(5)
        else:
            self.main_logger.info("\nSTEP :POST STAGING TEMPLATE CREATION AND DEPLOYMENT")
            # self.main_logger = self.setup_logger('Versa-director', 'Onboarding')
            curr_file_loader = FileSystemLoader(curr_file_dir + "/libraries/J2_temps/Solution/" + self.Solution_type)
            curr_env = Environment(loader=curr_file_loader)
            ps_template = curr_env.get_template("Post_staging_template.j2")
            self.ps_template_body = ps_template.render(self.__dict__)
            self.main_logger.debug(self.ps_template_body)
            ps_creation_result = self.post_operation(template_url, headers3, self.ps_template_body)
            self.main_logger.debug("\n" + ps_creation_result)
            if 'FAIL' in ps_creation_result:
                self.main_logger.info(">>>>>>>>>> POST STAGING TEMPLATE CREATION FAILED. <<<<<<<<<<<")
                exit()
            else:
                self.main_logger.info(">>>>>>>>>> POST STAGING TEMPLATE CREATION PASSED. <<<<<<<<<<<")
            time.sleep(5)
            PS_main_template = curr_env.get_template("PS_main_template_modify.j2")
            PS_main_template_modify = PS_main_template.render(self.__dict__)

            assoc_template_url = sfw_template_assc_url + self.PS_TEMPLATE_NAME + "/associations"
            assc_body = '[{"organization":"'+ self.ORG_NAME + '","serviceTemplate":"' + self.FW_PROFILE + str(self.NO_OF_VRFS) + '"}]'
            self.main_logger.debug(assc_body)
            fw_association = self.post_operation(assoc_template_url, headers3, assc_body)
            self.main_logger.debug("\n" + fw_association)
            if 'FAIL' in fw_association:
                self.main_logger.info(">>>>>>>>>> FW PROFILE ASSOCIATION WITH POST STAGING TEMPLATE FAILED. <<<<<<<<<<<")
                exit()
            else:
                self.main_logger.info(">>>>>>>>>> FW PROFILE ASSOCIATION WITH POST STAGING TEMPLATE PASSED. <<<<<<<<<<<")
            time.sleep(5)
            ps_deploy_result = self.post_operation(template_url + "/deploy/" + self.PS_TEMPLATE_NAME + "?verifyDiff=true", headers3,
                                self.ps_template_body)
            time.sleep(5)
            self.main_logger.debug("\n" + ps_deploy_result)
            if 'FAIL' in ps_deploy_result:
                self.main_logger.info(">>>>>>>>>> POST STAGING TEMPLATE DEPLOY FAILED. <<<<<<<<<<<")
                exit()
            else:
                self.main_logger.info(">>>>>>>>>> POST STAGING TEMPLATE DEPLOY PASSED. <<<<<<<<<<<")
            time.sleep(5)
            self.main_logger.debug(self.get_operation(template_url + "/" + self.PS_TEMPLATE_NAME, headers3))
            self.main_logger.debug(self.get_operation(assoc_template_url, headers3))
            time.sleep(5)
            main_template_modify_result = self.Modify_main_template(PS_main_template_modify)
            self.main_logger.debug("\n" + main_template_modify_result)
            if 'failed' in main_template_modify_result:
                self.main_logger.info(">>>>>>>>>> PS MAIN TEMPLATE MODIFY FAILED. <<<<<<<<<<<")
                exit()
            else:
                self.main_logger.info(">>>>>>>>>> PS MAIN TEMPLATE MODIFY PASSED. <<<<<<<<<<<")
            time.sleep(5)


    def create_and_deploy_device_group(self):
        # self.main_logger = self.setup_logger('Versa-director', 'Onboarding')
        self.main_logger.info("\nSTEP :DEVICE GROUP CREATION AND DEPLOYMENT")
        curr_file_loader = FileSystemLoader(curr_file_dir + "/libraries/J2_temps/Solution/" + self.Solution_type)
        curr_env = Environment(loader=curr_file_loader)
        if "DUAL-CPE" in self.Solution_type:
            if self.DUAL == "PRIMARY":
                DG_template = curr_env.get_template("Primary_Device_group_template.j2")
            elif self.DUAL == "SECONDARY":
                DG_template = curr_env.get_template("Secondary_Device_group_template.j2")
        else:
            DG_template = curr_env.get_template("Device_group_template.j2")
        self.DG_template_body = DG_template.render(self.__dict__)
        self.main_logger.debug(self.DG_template_body)
        dg_template_creation_result = self.post_operation(device_grp_url, headers3, self.DG_template_body)
        self.main_logger.debug("\n" + dg_template_creation_result)
        if 'FAIL' in dg_template_creation_result:
            self.main_logger.error(" >>>>>>>>>> DEVICE GROUP TEMPLATE CREATION FAILED. <<<<<<<<<<<")
            exit()
        else:
            self.main_logger.info(">>>>>>>>>> DEVICE GROUP TEMPLATE CREATION PASSED. <<<<<<<<<<<")
        time.sleep(5)

    def create_PS_and_DG(self):
        # self.main_logger = self.setup_logger('Versa-director', 'Onboarding')
        curr_file_loader = FileSystemLoader(curr_file_dir + "/libraries/J2_temps/Solution/" + self.Solution_type)
        curr_env = Environment(loader=curr_file_loader)
        # template = curr_env.get_template(org_template)
        ps_template = curr_env.get_template("Post_staging_template.j2")
        DG_template = curr_env.get_template("Device_group_template.j2")
        PS_main_template = curr_env.get_template("PS_main_template_modify.j2")

        self.ps_template_body = ps_template.render(self.__dict__)
        self.DG_template_body = DG_template.render(self.__dict__)
        PS_main_template_modify = PS_main_template.render(self.__dict__)
        print self.ps_template_body
        print self.DG_template_body
        self.main_logger.info(self.post_operation(template_url, headers3, self.ps_template_body))
        time.sleep(5)
        assoc_template_url = sfw_template_assc_url + self.PS_TEMPLATE_NAME + "/associations"
        assc_body = '[{"organization":"'+ self.ORG_NAME + '","serviceTemplate":"COMMON-SFW-TEMPLATE10"}]'
        print assc_body
        self.main_logger.info(self.post_operation(assoc_template_url, headers3, assc_body))
        time.sleep(5)
        self.main_logger.info(self.post_operation(template_url + "/deploy/" + self.PS_TEMPLATE_NAME + "?verifyDiff=true", headers3,
                           self.ps_template_body))
        time.sleep(5)
        self.main_logger.info(self.get_operation(template_url + "/" + self.PS_TEMPLATE_NAME, headers3))
        self.main_logger.info(self.get_operation(assoc_template_url, headers3))
        time.sleep(5)
        result = self.Modify_main_template(PS_main_template_modify)
        self.main_logger.info(result)
        self.main_logger.info(self.post_operation(device_grp_url, headers3, self.DG_template_body))
        time.sleep(5)

    def Modify_main_template(self, PS_main_template_modify):
        res_check = ""
        # self.main_logger = self.setup_logger('Versa-director', 'Onboarding')
        self.ps_main_template_modify = PS_main_template_modify
        # print self.ps_main_template_modify
        self.vdnc = self.login(vd_login='yes')
        nc = self.vdnc
        device_cmds = self.ps_main_template_modify
        # self.main_logger.info(self.device_config_commands(self.vdnc, self.ps_main_template_modify))
        self.main_logger.debug(device_cmds)
        result = self.device_config_commands_wo_split(nc, device_cmds)
        self.main_logger.debug(result)
        if "syntax error:" in result:
            res_check += "syntax error found."
        elif "Error: element not found" in result:
            res_check += "element not found error."
        # else:
        commit_result = nc.send_command_expect("commit", \
                                               expect_string='%', \
                                               strip_prompt=False, strip_command=False, max_loops=5000)
        self.main_logger.debug(commit_result)
        if "No modifications to commit." in commit_result:
            res_check += "No modifications to commit."
        elif "Commit complete." in commit_result:
            res_check += "Commit success."
        else:
            res_check += "Commit failed."
        # self.main_logger.info(self.Device_name + " : " + res_check)
        self.close(self.vdnc)
        return self.Device_name + " : " + res_check


    def pre_onboard_work(self):
        self.main_logger.info("\nSTEP :PRE-ONBOARD WORK")
        # self.main_logger = self.setup_logger('Versa-director', 'Onboarding')
        #(self, Device_template, Staging_server_config_template, Staging_cpe_config_template):
        curr_file_loader = FileSystemLoader(curr_file_dir + "/libraries/J2_temps/Solution/" + self.Solution_type)
        curr_env = Environment(loader=curr_file_loader)
        if "DUAL-CPE" in self.Solution_type:
            if self.DUAL == "PRIMARY":
                self.DEVICE_template = curr_env.get_template("Primary_Device_template.j2")
            elif self.DUAL == "SECONDARY":
                self.DEVICE_template = curr_env.get_template("Secondary_Device_template.j2")
        else:
            self.DEVICE_template = curr_env.get_template("Device_template.j2")
        self.Staging_config = curr_env.get_template("Staging_server_config.j2")
        self.Staging_command = curr_env.get_template("staging_cpe.j2")
        self.DEVICE_template_body = self.DEVICE_template.render(self.__dict__)
        self.Staging_config_template = self.Staging_config.render(self.__dict__)
        self.Staging_command_template = self.Staging_command.render(self.__dict__)
        self.main_logger.debug(self.Staging_command_template)
        self.main_logger.debug(self.DEVICE_template_body)
        device_tempalte_creation_result = self.post_operation(device_template_url, headers3, self.DEVICE_template_body)
        self.main_logger.debug("\n" + device_tempalte_creation_result)
        if 'FAIL' in device_tempalte_creation_result:
            self.main_logger.error(" >>>>>>>>>> DEVICE TEMPLATE CREATION FAILED. <<<<<<<<<<<")
            exit()
        else:
            self.main_logger.info(">>>>>>>>>> DEVICE TEMPLATE CREATION PASSED. <<<<<<<<<<<")
        time.sleep(5)
        time.sleep(5)
        task_id = self.rest_operation_ret_task_id(device_template_url + "/deploy/" + self.Device_name,
                                                 headers3)
        time.sleep(5)
        self.main_logger.debug(task_id)
        task_state = "0"
        while task_state != "100":
            task_state = self.check_task_status(task_id)
        task_result = self.get_task_result(task_id)
        if task_result == "PASS":
            self.main_logger.info(">>>>>>>>>> Device deployed  <<<<<<<<<<<")
        else:
            self.main_logger.error(">>>>>>>>>>Device deployment failed <<<<<<<<<<<")
            self.main_logger.error("TASK RESULT : " + task_result)
            exit()
        get_device_data = self.get_operation(device_template_url + "/" + self.Device_name, headers3)
        self.main_logger.debug(get_device_data)
        time.sleep(5)
        self.vdnc = self.login(vd_login='yes')
        self.device_config_commands(self.vdnc, self.Staging_config_template)
        self.main_logger.info(">>>>>>>>>> Staging profile config done  <<<<<<<<<<<")
        self.close(self.vdnc)
        
    def VM_pre_op(self):
        self.VM_nc = self.shell_login()
        self.linux_device_config_commands(self.VM_nc, "sudo bash", expect_string=":")
        self.linux_device_config_commands(self.VM_nc, self.password, expect_string="#")
        self.linux_device_config_commands(self.VM_nc, "exit", expect_string="\$")
        self.linux_device_config_commands(self.VM_nc, "sudo ifconfig " + self.LAN_INTF + " up")
        for vlan in self.lan_vlan:
            intf = str(self.LAN_INTF)
            ip = str(self.lan_second_host[vlan])
            gw = str(self.lan_first_host[vlan])
            nmask = str(self.lan_netmask[vlan])
            destination_nw = str(self.peer_lan_network[vlan])
            vlan = str(vlan)
            self.linux_device_config_commands(self.VM_nc, "sudo vconfig add " + intf + " " + vlan)
            self.linux_device_config_commands(self.VM_nc, "sudo ifconfig " + intf + "." + vlan + " up")
            self.linux_device_config_commands(self.VM_nc,
                                             "sudo ifconfig " + intf + "." + vlan + " " + ip + " netmask " + nmask)
            self.linux_device_config_commands(self.VM_nc, "sudo ip route add " + destination_nw + " via " + gw +" dev " + intf + "." + vlan)

    def shell_ping(self, dest_ip, count=5, **kwargs):
        cmd = "sudo ping " + str(dest_ip) + " -c " + str(count)
        paramlist = ['count', 'df_bit', 'interface', 'packet_size', 'rapid', 'record-route', 'routing_instance',
                     'source']
        for element in paramlist:
            if element in kwargs.keys():
                cmd = cmd + " " + element.replace('_', '-') + " " + str(kwargs[element])
        print cmd

        output = self.VM_nc.send_command_expect(cmd, strip_prompt=False, strip_command=False)
        print output
        # logger.info(output, also_console=True)
        return str(" 0% packet loss" in output)

    def ping(self,  dest_ip, **kwargs):
        cmd = "ping " + str(dest_ip)
        paramlist = ['count', 'df_bit', 'interface', 'packet_size', 'rapid', 'record-route', 'routing_instance',
                     'source']
        for element in paramlist:
            if element in kwargs.keys():
                cmd = cmd + " " + element.replace('_', '-') + " " + str(kwargs[element])
        print cmd
        output = self.cnc.send_command_expect(cmd, expect_string=">", strip_prompt=False, strip_command=False)
        print output
        return str(" 0% packet loss" in output)


    def get_interface_status(self, intf_name):
        cmd = "show interfaces brief | tab | match " + str(intf_name)
        output = self.cnc.send_command_expect(cmd, expect_string=">", strip_prompt=False, strip_command=False)
        return output

    def get_bgp_nbr_status(self, nbr_ip):
        cmd = "show bgp neighbor org " + self.ORG_NAME + " brief " + self.ORG_NAME+"-Control-VR | match " + nbr_ip
        output = self.cnc.send_command_expect(cmd, expect_string=">", strip_prompt=False, strip_command=False)
        return output

    def parse_send_command(self, output, parse_template):
        time.sleep(1)
        template = open(parse_template)
        re_table = textfsm.TextFSM(template)
        fsm_results = re_table.ParseText(output.encode("utf-8"))
        fsm_result_str = ""
        fsm_result_str += "     ".join(re_table.header) + "\n"
        for row in fsm_results:
            fsm_result_str += " ".join(row) + "\n"
        # print fsm_result_str
        return fsm_result_str


    def check_lan_route(self, lan):
        cmd = "show route routing-instance LAN"+ lan + "-VRF | nomore"
        output = self.cnc.send_command_expect(cmd, expect_string=">", strip_prompt=False, strip_command=False)
        output = self.parse_send_command(output, route_template)
        return output


    def send_commands_and_expect(self, cmds, expect_string=">|%"):
        for cmd in cmds.split("\n"):
            print cmd
            output = self.cnc.send_command_expect(cmd, expect_string=expect_string, strip_prompt=False,
                                                 strip_command=False)
        logger.info(output, also_console=True)
        return output

    def shutdown_interface(self, intf_name):
        data = self.get_interface_data_from_vd(intf_name)
        data['vni']['enable'] = False
        data1 = json.dumps(data)
        self.put_operation(self.vni_interface_url, headers2, data1)

    def unshutdown_interface(self, intf_name):
        data = self.get_interface_data_from_vd(intf_name)
        data['vni']['enable'] = True
        data1 = json.dumps(data)
        self.put_operation(self.vni_interface_url, headers2, data1)

    def request_ping(self, net_connect, cpe):
        net_connect.send_command_expect("cli", strip_prompt=False, strip_command=False, expect_string=">")
        cmd = "request devices device " + cpe + " ping"
        self.main_logger.info("CMD>> : " + cmd)
        output = net_connect.send_command_expect(cmd, strip_prompt=False, strip_command=False, expect_string=">")
        # net_connect.send_command_expect("quit", strip_prompt=False, strip_command=False)
        self.main_logger.info(output)
        return str(", 0% packet loss," in output)

    def request_connect(self, net_connect, cpe):
        cmd = "request devices device " + cpe + " connect"
        self.main_logger.info("CMD>> : " + cmd)
        output = net_connect.send_command_expect(cmd, strip_prompt=False, strip_command=False)
        self.main_logger.info(output)
        return str(" Connected to" in output)

    def request_check_sync(self, net_connect, cpe):
        cmd = "request devices device " + cpe + " check-sync"
        self.main_logger.info("CMD>> : " + cmd)
        output = net_connect.send_command_expect(cmd, strip_prompt=False, strip_command=False)
        self.main_logger.info(output)
        return str("result in-sync" in output)

    def request_sync_from_cpe(self, net_connect, cpe):
        cmd = "request devices device " + cpe + " sync-from"
        self.main_logger.info("CMD>> : " + cmd)
        output = net_connect.send_command_expect(cmd, strip_prompt=False, strip_command=False)
        self.main_logger.info(output)
        return str(" result true" in output)

    def check_device_status(self, nc, device_name):
        if self.request_ping(nc, device_name) == "True":
            if self.request_connect(nc, device_name) == "True":
                if self.request_sync_from_cpe(nc, device_name):
                    return "PASS"
                else:
                    return "VD --> CPE req sync failed"
            else:
                return "VD --> CPE Request connect failed."
        else:
            return "VD --> CPE Request ping failed."

    def config_devices_template(self, nc, device_file, command_template_file):
        start_time = datetime.now()
        main_logger = self.setup_logger('Versa-director', 'Config_devices_template')
        # print device_file
        # print command_template_file
        curr_file_dir = os.path.dirname(command_template_file)
        curr_file_name = os.path.basename(command_template_file)
        curr_file_loader = FileSystemLoader(curr_file_dir)
        curr_env = Environment(loader=curr_file_loader)
        template = curr_env.get_template(curr_file_name)
        csv_data_read = pd.read_csv(device_file)
        result_dict = {}
        for idx, row in csv_data_read.iterrows():
            res_check = ""
            dev_dict = row.to_dict()
            if isinstance(dev_dict['SITE_TYPE'], float):
                if math.isnan(dev_dict['SITE_TYPE']):
                    res_check += "Site type is empty"
                    result_dict[dev_dict['NAME']] = res_check
                    continue
            elif dev_dict['SITE_TYPE'] == 'mpls':
                if dev_dict['DUAL_CPE'] == 'Y':
                    dev_dict['SITE_TYPE'] = 'dual_mpls'
                else:
                    res_check += "Single MPLS site. No changes commited"
                    result_dict[dev_dict['NAME']] = res_check
                    continue
            # print Solution_type[dev_dict['SITE_TYPE']]
            device_cmds =  template.render(dev_dict, **Solution_type[dev_dict['SITE_TYPE']])
            main_logger.info(device_cmds)
            result = self.device_config_commands_wo_split(nc, device_cmds)
            main_logger.info(result)
            if "syntax error:" in result:
                res_check += "syntax error found."
            elif "Error: element not found" in result:
                res_check += "element not found error."
            # else:
            commit_result = nc.send_command_expect("commit", \
                                                   expect_string='%', \
                                                   strip_prompt=False, strip_command=False, max_loops=5000)
            main_logger.info(commit_result)
            if "No modifications to commit." in commit_result:
                res_check += "No modifications to commit."
            elif "Commit complete." in commit_result:
                res_check += "Commit success."
            else:
                res_check += "commit failed.Check log"
            result_dict[dev_dict['NAME']] = res_check
            # main_logger.info(result_dict)
            main_logger.info("CONFIG_RESULT:")
            for k, v in result_dict.iteritems():
                main_logger.info([k , v])
        write_result_from_dict(result_dict)
        main_logger.info("Time elapsed: {}\n".format(datetime.now() - start_time))
        main_logger.info("LOGS Stored in : " + logfile_dir)
        return

    def config_function(self, nc, config_for, csv_file, template_file, type=""):
        start_time = datetime.now()
        # self.main_logger = self.setup_logger('Versa-director', 'Config_devices_template')
        curr_file_loader = FileSystemLoader(curr_file_dir + "/libraries/J2_temps/PROD_CONFIG/")
        curr_env = Environment(loader=curr_file_loader)
        template = curr_env.get_template(template_file)
        csv_data_read = pd.read_csv(curr_file_dir + "/Topology/" + csv_file )
        result_dict = {}
        device_cmds = ""
        for idx, row in csv_data_read.iterrows():
            res_check = ""
            dev_dict = row.to_dict()
            if config_for == "ckt_pri":
                if isinstance(dev_dict['SITE_TYPE'], float):
                    if math.isnan(dev_dict['SITE_TYPE']):
                        res_check += "Site type is empty"
                        result_dict[dev_dict['NAME']] = res_check
                        continue
                elif dev_dict['SITE_TYPE'] == 'mpls':
                    if dev_dict['DUAL_CPE'] == 'Y':
                        dev_dict['SITE_TYPE'] = 'dual_mpls'
                    else:
                        res_check += "Single MPLS site. No changes commited"
                        result_dict[dev_dict['NAME']] = res_check
                        continue
                # print Solution_type[dev_dict['SITE_TYPE']]
                device_cmds =  template.render(dev_dict, **Solution_type[dev_dict['SITE_TYPE']])
            elif config_for == "tacacs":
                if type == "devices":
                    check_state_result = self.check_device_status(nc, dev_dict['NAME'])
                    if check_state_result != "PASS":
                        res_check += check_state_result
                        result_dict[dev_dict['NAME']] = res_check
                        self.main_logger.info("CONFIG_RESULT:")
                        for k, v in result_dict.iteritems():
                            self.main_logger.info([k, v])
                        continue
                elif type == "ps":
                    pass
                device_cmds = template.render(dev_dict)
            self.main_logger.info(device_cmds)
            result = self.device_config_commands_wo_split(nc, device_cmds)
            self.main_logger.info(result)
            if "syntax error:" in result:
                res_check += "syntax error found."
            elif "Error: element not found" in result:
                res_check += "element not found error."
            # else:
            commit_result = nc.send_command_expect("commit", \
                                                   expect_string='%', \
                                                   strip_prompt=False, strip_command=False, max_loops=5000)
            self.main_logger.info(commit_result)
            ex_result = nc.send_command_expect("exit no-confirm", expect_string=">", strip_prompt=False,
                                                            strip_command=False, max_loops=5000)
            self.main_logger.info(ex_result)
            if "No modifications to commit." in commit_result:
                res_check += "No modifications to commit."
            elif "Commit complete." in commit_result:
                res_check += "Commit success."
            else:
                res_check += "commit failed.Check log"
            result_dict[dev_dict['NAME']] = res_check
            # main_logger.info(result_dict)
            self.main_logger.info("CONFIG_RESULT:")
            for k, v in result_dict.iteritems():
                self.main_logger.info([k , v])
        write_result_from_dict(result_dict)
        self.main_logger.info("Time elapsed: {}\n".format(datetime.now() - start_time))
        self.main_logger.info("LOGS Stored in : " + logfile_dir)
        return

    def get_device_list_from_vd_using_rest(self, oper_type='patch_upgrade', dev_type="", ping_status_check="no"):
        global batch, devices_list
        data1 = self.get_operation(appliance_url, headers3)
        count, day, batch = 1, 1, 1
        # print data1
        devices_list = []
        for i in data1['versanms.ApplianceStatusResult']['appliances']:
            device_list = []
            if dev_type != "":
                if i['type'] == dev_type:
                    pass
                else:
                    continue
            if ping_status_check == "yes":
                if i['ping-status'] != 'REACHABLE':
                    continue
            # if i['ownerOrg'] != 'Colt':
            # if i['ping-status'] == 'REACHABLE':
            if oper_type == 'file_transfer':
                if count % 5 == 0:
                    batch += 1
            else:
                if count % 9 == 0:
                    batch += 1
            device_list.append(i['name'])
            device_list.append(i['ipAddress'])
            device_list.append(day)
            device_list.append(batch)
            # device_list.append(i['ownerOrg'])
            device_list.append(i['type'])
            if 'softwareVersion' in i:
                device_list.append(i['softwareVersion'])
            else:
                device_list.append("Nil info")
            device_list.append(i['ping-status'])
            device_list.append(i['sync-status'])
            # try:
            #     if i['Hardware']!="":
            #         device_list.append(i['Hardware']['serialNo'])
            #         device_list.append(i['Hardware']['model'])
            #         device_list.append(i['Hardware']['packageName'])
            # except KeyError as ke:
            #     print i['name']
            #     print "Hardware Info NIL"
            # print count, day, batch
            count += 1
            devices_list.append(device_list)
        # print devices_list
        return devices_list

    def build_csv(self, device_list):
        with open(curr_file_dir + "/Topology/" + self.cpe_list_file_name, 'w') as file_writer1:
            data_header = ['NAME', 'ip', 'day', 'batch', 'type', 'softwareVersion', 'ping-status',
                           'sync-status']
            writer = csv.writer(file_writer1)
            writer.writerow(data_header)
            for item in device_list:
                writer.writerow(item)


    def get_PS_templates(self):
        data = self.get_operation(get_template_url , headers3)
        tempalte_dict = {}
        for idx, i in enumerate(data['versanms.sdwan-template-list']):
            print idx
            tempalte_dict[idx] = str(i['templateName'])
        return tempalte_dict

    def Create_Controller_List(self,org_name, org_id, no_of_vrfs, nodes):
        nodes_list = nodes.split(" ")
        node_type = "WC"
        for node in nodes_list:
            if not self.ctlr_dict.has_key(node):
                print "Enter Node is not availble ---> " + str(node)
                exit()
            else:
                for i in self.ctlr_dict[node]:
                    if i not in self.ctlr_list:
                        self.ctlr_list.append(i)
        for ctlr in ctlr_list:
            self.Create_Node_Data(ctlr, "WC", org_name, org_id)
        return self.ctlr_list


    def Create_Gateway_List(self,org_name, org_id, no_of_vrfs, nodes):
        nodes_list = nodes.split(" ")
        for node in nodes_list:
            if not self.gw_dict.has_key(node):
                print "Enter Node is not availble ---> " + str(node)
                exit()
            else:
                for i in self.gw_dict[node]:
                    if i not in self.gw_list:
                        self.gw_list.append(i)
        for gw in gw_list:
            self.Create_Node_Data(gw, "GW", org_name, org_id)
        return self.gw_list

    def Create_Node_Data(self, node_dev, node_type, org_name="", org_id="", wan=""):
        csv_data_read = pd.read_csv(curr_file_dir + "/libraries/NODEDB/" + node_type + ".csv")
        csv_data_read = csv_data_read.loc[csv_data_read['DEVICE_NAME'] == node_dev]
        if node_type == "WC|GW":
            csv_data_read = csv_data_read.loc[csv_data_read['ORG_NAME'] == "temporgname"]
        if node_type == "SS":
            if self.Solution_type == "SINGLE-CPE-DUAL-INTERNET":
                csv_data_read = csv_data_read.loc[csv_data_read['WAN'] == "INT"]
            else:
                csv_data_read = csv_data_read.loc[csv_data_read['WAN'] == wan]
        for idx, row in csv_data_read.iterrows():
            res_check = ""
            node_device_data = row.to_dict()
            for k, v in node_device_data.iteritems():
                if isinstance(v, str):
                    if "temporgname" in v:
                        v = v.replace("temporgname", str(org_name))
                    if "temporgid" in v:
                        v = v.replace("temporgid", str(org_id))
                    if "tempdevicename" in v:
                        v = v.replace("tempdevicename", str(node_dev))
                    if re.search("^{", v):
                        v = try_literal_eval(v)
                    node_device_data[k] = v
                if isinstance(v, float):
                    if math.isnan(v):
                        node_device_data[k] = ""
                    else:
                        node_device_data[k] = int(v)
            node_device_data["DEVICE_TYPE"] = node_type
            if node_type == "WC":
                node_device_data["VNF_GWS"] = gw_dict[node_device_data['NODE']]
                if RR_Clients.has_key(node_dev):
                    node_device_data["RR_CLIENTS"] = RR_Clients[node_dev]
                else:
                    for k, v in RR_Clients.iteritems():
                        if node_dev in RR_Clients[k]:
                            if k in RR_SERVER:
                                node_device_data["RR_SERVER"] = k
            if node_type == "GW":
                node_device_data["WC_list"] = ctlr_dict[node_device_data['NODE']]
            if "NODE" in self.__dict__:
                node_device_data["LCC"] = LCC_dict[self.NODE]
            else:
                node_device_data["LCC"] = LCC_dict[node_device_data['NODE']]
            if node_type == "SS":
                self.ndb[node_type] = {}
                self.ndb[node_type][node_dev] = node_device_data
                self.STAGING_SERVER = node_dev
                self.STAGING_ORG = node_device_data['ORG_NAME']
                self.STAGING_PROFILE_NAME = node_device_data['PROFILE']
                self.STAGING_CTRLR_IP = node_device_data['IP']
                self.Staging_remote_id = node_device_data['ID']
                self.Staging_remote_key = node_device_data['KEY']
                self.STAGING_ID = self.ORG_NAME + "-" + self.Device_name + "@colt.net"
                self.STAGING_id_type = "email"
                self.STAGING_KEY = self.Device_name
                # if self.Solution_type == "SINGLE-CPE-DUAL-INTERNET":
                #     # self.STAGING_INTF = self.__dict__[wan + "_WAN_INTF"][-1]
                #     self.STAGING_Local_ip_with_mask =  self.__dict__[wan + "_WAN_INTF_IP"]
                # else:
                #     # self.STAGING_INTF = self.__dict__[wan + "_WAN_INTF"][-1]
                # self.STAGING_Local_ip_with_mask =  self.__dict__["WAN" + self.STAGING_INTF + "_INTF_IP"]
                # self.STAGING_nexthop = self.__dict__["WAN" + self.STAGING_INTF + "_INTF_NEXTHOP"]
                self.STAGING_Local_ip_with_mask = self.__dict__[self.STAGING_INTF + "_INTF_IP"]
                self.STAGING_nexthop = self.__dict__[self.STAGING_INTF + "_INTF_NEXTHOP"]
                STAGINGWAN_INTF = self.__dict__[self.STAGING_INTF + "_INTF"]
                self.STAGING_INTF = STAGINGWAN_INTF[-1]
                self.WAN1_NAME = WAN_INTERFACES[self.Solution_type]['WAN1']
                if "WAN2" in WAN_INTERFACES[self.Solution_type]:
                    self.WAN2_NAME = WAN_INTERFACES[self.Solution_type]['WAN2']
            else:
                self.ndb[node_dev] = node_device_data
        return

    def create_fowarding_profile(self, profilename, preferwan):
        self.main_logger.info("\nCREATE FWD PROFILE\n")
        curr_file_loader = FileSystemLoader(curr_file_dir + "/libraries/J2_temps/FWD_PROFILE/" + self.Solution_type)
        fwd_profile_url_mod = fwd_profile_url.replace("temporgname" , self.ORG_NAME)
        fwd_profile_url_mod = fwd_profile_url_mod.replace("tempdevicename", self.Device_name)
        self.FW_PROFILE_NAME = profilename
        curr_env = Environment(loader=curr_file_loader)
        FWP_template = curr_env.get_template("PREFER_" + preferwan + ".j2")
        self.fw_profile_template_body = FWP_template.render(self.__dict__)
        print self.fw_profile_template_body
        fwd_profile_creation_result = self.post_operation(fwd_profile_url_mod, headers2, self.fw_profile_template_body)
        self.main_logger.info("\n" + fwd_profile_creation_result)
        if 'FAIL' in fwd_profile_creation_result:
            self.main_logger.info(">>>>>>>>>> FORWARDING PROFILE CREATION FAILED. <<<<<<<<<<<")
            return "FAIL"
        else:
            self.main_logger.info(">>>>>>>>>> FORWARDING PROFILE CREATION PASSED. <<<<<<<<<<<")
            return "PASS"
        time.sleep(5)

    def Create_Org(self, org_name, org_id, WC_list, no_of_vrfs):
        # main_logger = self.setup_logger('Versa-director', 'Create_org')
        org_template = "org_creation_template.j2"
        org_data = "ORG_DATA.csv"
        # curr_file_dir = os.path.dirname(org_template)
        # curr_file_name = os.path.basename(org_template)
        # curr_file_loader = FileSystemLoader(curr_file_dir)
        # curr_env = Environment(loader=curr_file_loader)
        # template = curr_env.get_template(curr_file_name)
        # curr_file_dir = os.path.curdir
        curr_file_loader = FileSystemLoader(curr_file_dir + "/libraries/J2_temps/ORG_CREATION")
        curr_env = Environment(loader=curr_file_loader)
        template = curr_env.get_template(org_template)
        # csv_data_read = pd.read_csv(curr_file_dir + "/Topology/" + org_data)
        # # csv_data_read = pd.read_csv(org_data)
        # if org_name != "":
        #     csv_data_read = csv_data_read.loc[csv_data_read['ORG_NAME'] == "temporgname"]
        # for idx, row in csv_data_read.iterrows():
        res_check = ""
        self.org_data = {}
        # print self.org_data
        self.org_data['NO_OF_VRFS'] = int(no_of_vrfs)
        self.org_data['ORG_ID'] = int(org_id)
        self.org_data['ORG_NAME'] = org_name
        self.org_data['CONTROLLERS'] = WC_list
        print org_id
        if int(org_id) in range(1, 207):
            print "org_id is ok "
        else:
            print " org id entered is not range 1 - 206"
            return "FAIL:  org id entered is not range 1 - 206. Enter ORG ID : " + org_id
        org_body =  template.render(self.org_data)
        self.WC_list = WC_list
        # self.GW_list = self.org_data['GATEWAYS'].replace('"', "").split(", ")
        self.main_logger.debug(org_body)
        # return "PASS"
        print org_url
        print headers3
        print org_body
        result = self.post_operation(org_url, headers3, org_body)
        self.main_logger.info(result)
        if "error" in result:
            print "Error occured : " + result
            return result
        time.sleep(5)
        task_id = self.rest_operation_ret_task_id(org_url+ "/deploy/" + \
                                                        self.org_data['ORG_NAME'], headers3, org_body)
        time.sleep(5)
        self.main_logger.info(task_id)
        task_state = "0"
        while task_state != "100":
            task_state = self.check_task_status(task_id)
        task_result = self.get_task_result(task_id)
        self.main_logger.info(task_result)
        return task_result
        if task_result == "PASS":
            self.main_logger.info("Org deployed")
        else:
            self.main_logger.info("Org deployment failed")
            return "FAIL: " + task_result
        get_device_data = self.get_operation(org_url + "/" + self.org_data['ORG_NAME'], headers3)
        print get_device_data
        time.sleep(5)
        self.main_logger.info(self.org_data)
        return task_result

    def Config_Node_Devices(self, device_name, node_type, nodes, action="set", **kwargs):
        # main_logger = self.setup_logger('Versa-director', 'Create_org')
        nc = self.login()
        #nc = "xyz"
        org_name = self.org_data['ORG_NAME']
        # curr_file_dir = os.path.dirname(node_template)
        # curr_file_name = os.path.basename(node_template)
        curr_file_loader = FileSystemLoader(curr_file_dir + "/libraries/J2_temps/ORG_CREATION")
        curr_env = Environment(loader=curr_file_loader)
        template = curr_env.get_template(node_type+"_Template.j2")

        csv_data_read = pd.read_csv(curr_file_dir + "/libraries/NODEDB/" + node_type + ".csv")
        csv_data_read = csv_data_read.loc[csv_data_read['DEVICE_NAME'] == device_name]
        csv_data_read = csv_data_read.loc[csv_data_read['ORG_NAME'] == "temporgname"]
        res_check = ""
        org_data = self.ndb[device_name]
        if org_data['DEVICE_TYPE'] == "WC":
            ORG_ID = int(org_data['ORG_ID'])
            org_data['ORG_ID'] = int(org_data['ORG_ID'])
            # org_data['NO_OF_VRFS'] = int(org_data['NO_OF_VRFS'])
            org_data['VRF1_ID']	=	ORG_ID * 10 + 120
            org_data['VXLAN_TVI_INTERFACE']	=	"tvi-0/" + str(ORG_ID * 2)
            org_data['ESP_TVI_INTERFACE']	=	"tvi-0/" + str(ORG_ID * 2 + 1)
            org_data['PTVI_INTERFACE1']	=	"ptvi" + str(ORG_ID * 2)
            org_data['PTVI_INTERFACE2']	=	"ptvi" + str(ORG_ID * 2 + 1)

            org_data['EXPORT_VRFS_SET'] = ""
            org_data['LAN_VRFS_SET'] = ""
            org_data['PAIRED_TVI_INTERFACE_SET'] =""
            org_data['MPLS_NW_SET'] = ""
            dup_rrc_list = []
            org_data['RRCDICT'] = {}
            org_data['RRSDICT'] = {}
            if org_data.has_key('RR_CLIENTS'):
                for RRC in org_data['RR_CLIENTS']:
                    if self.ndb.has_key(RRC):
                        org_data['RRCDICT'][RRC] = self.ndb[RRC]
                        dup_rrc_list.append(RRC)
                    # else:
                    #     org_data['RR_CLIENTS'].remove(RRC)
            org_data['RR_CLIENTS'] = dup_rrc_list
            if org_data.has_key('RR_SERVER') :
                if org_data['RR_SERVER'] != "":
                    if self.ndb.has_key(org_data['RR_SERVER']):
                        org_data['RRSDICT'][org_data['RR_SERVER']] = self.ndb[org_data['RR_SERVER']]
            org_data["GWDICT"] = {}
            print org_data['NODE']
            print nodes
            if org_data['NODE'] in nodes:
                for VNF_GW in org_data['VNF_GWS']:
                    org_data["GWDICT"][VNF_GW] = self.ndb[VNF_GW]
            else:
                org_data['VNF_GWS'] = []
            print org_data
            # for i in range(1, org_data['NO_OF_VRFS'] + 1):
            #     org_data['EXPORT_VRFS_SET'] += org_data['ORG_NAME'] + "-EXPORT" + str(i) + "-VRF "
            #     org_data['LAN_VRFS_SET'] += org_data['ORG_NAME'] + "-LAN" + str(i) + "-VRF "
            #     org_data['PAIRED_TVI_INTERFACE_SET'] += "tvi-0/" + str(ORG_ID * 10 + 120  + i-1) + ".0 "
            #     org_data['PAIRED_TVI_INTERFACE_SET'] += "tvi-0/" + str(ORG_ID * 10 + 2020  + i-1) + ".0 "
            #     org_data['MPLS_NW_SET'] += org_data['ORG_NAME'] + "-MPLS" + str(i) + " "
        if org_data['DEVICE_TYPE'] == "GW":
            if kwargs['no_of_vrfs']:
                org_data['NO_OF_VRFS'] = int(kwargs['no_of_vrfs'])
            ORG_ID = int(org_data['ORG_ID'])
            org_data['ORG_ID'] = int(org_data['ORG_ID'])
            # org_data['NO_OF_VRFS'] = int(org_data['NO_OF_VRFS'])
            org_data['VRF1_ID']	=	ORG_ID * 10 + 120
            org_data['VXLAN_TVI_INTERFACE']	=	"tvi-0/" + str(ORG_ID * 2)
            org_data['ESP_TVI_INTERFACE']	=	"tvi-0/" + str(ORG_ID * 2 + 1)
            # org_data['PAIRED_TVI_INTERFACE1']	=	"tvi-0/" + str(ORG_ID * 10 + 120)
            # org_data['PAIRED_TVI_INTERFACE2']	=	"tvi-0/" + str(ORG_ID * 10 + 2020)
            org_data['PTVI_INTERFACE1']	=	"ptvi" + str(ORG_ID * 2)
            org_data['PTVI_INTERFACE2']	=	"ptvi" + str(ORG_ID * 2 + 1)
            org_data['PTVI_INTERFACES'] = {}
            org_data['PTVI_INTERFACES'][1] = "ptvi" + str(ORG_ID * 2)
            org_data['PTVI_INTERFACES'][2] = "ptvi" + str(ORG_ID * 2 + 1)
            if org_data['GW_NUMBER'] == 1 :
                org_data['NNI1_VLAN']	=	ORG_ID * 10 + 120
            elif org_data['GW_NUMBER'] == 2:
                org_data['NNI1_VLAN'] = ORG_ID * 10 + 1020
            self.START_VLAN = int(org_data['NNI1_VLAN'])
            org_data['NNI_LAN'] = self.set_network_items(org_data['NNI1_SUBNET'])
            org_data['PAIRED_TVI_LAN'] = self.set_network_items(org_data['PAIRED_TVI_SUBNET'])

            org_data['EXPORT_VRFS_SET'] = ""
            org_data['LAN_VRFS_SET'] = ""
            org_data['PAIRED_TVI_INTERFACE_SET'] =""
            org_data['MPLS_NW_SET'] = ""
            org_data['WC_LIST'] = ctlr_dict[org_data['NODE']]
            org_data['WCDICT'] = {}
            for WC in org_data['WC_LIST']:
                org_data['WCDICT'][WC] = self.ndb[WC]

            for i in range(1, org_data['NO_OF_VRFS'] + 1):
                org_data['EXPORT_VRFS_SET'] += org_data['ORG_NAME'] + "-EXPORT" + str(i) + "-VRF "
                org_data['LAN_VRFS_SET'] += org_data['ORG_NAME'] + "-LAN" + str(i) + "-VRF "
                org_data['PAIRED_TVI_INTERFACE_SET'] += "tvi-0/" + str(ORG_ID * 10 + 120  + i-1) + ".0 "
                org_data['PAIRED_TVI_INTERFACE_SET'] += "tvi-0/" + str(ORG_ID * 10 + 2020  + i-1) + ".0 "
                org_data['MPLS_NW_SET'] += org_data['ORG_NAME'] + "-MPLS" + str(i) + " "
        device_cmds =  template.render(org_data)
        # template_source = curr_env.loader.get_source(curr_env, node_type+"_Template.j2")[0]
        # parsed_content = curr_env.parse(template_source)
        # variables = meta.find_undeclared_variables(parsed_content)
        # print variables
        if action == "delete":
            device_cmds = re.sub("^set ", "delete ", device_cmds, flags=re.M)
        self.main_logger.info(device_cmds)
        # return "PASS"
        result = self.device_config_commands_wo_split(nc, device_cmds)
        self.main_logger.info(result)
        if "syntax error:" in result:
            res_check += "syntax error found."
        elif "Error: element not found" in result:
            res_check += "element not found error."
        # else:
        commit_result = nc.send_command_expect("commit", \
                                               expect_string='%', \
                                               strip_prompt=False, strip_command=False, max_loops=5000)
        self.main_logger.info(commit_result)
        if "No modifications to commit." in commit_result:
            res_check += "No modifications to commit."
        elif "Commit complete." in commit_result:
            res_check += "Commit success."
        else:
            res_check += "Commit failed."
        self.main_logger.info(org_data['DEVICE_NAME'] + " : " + res_check)
        return res_check



def main():
    print datetime.now()
    cpe1 = VersaLib('VD1', topofile=fileDir + "/Topology/Devices.csv")
    # #
    # # cpe1.Create_Org(org_template=fileDir + "/libraries/J2_temps/org_creation_template.j2", org_data=fileDir + "/Topology/ORG_DATA.csv")
    # cpe1.Create_Org(org_template=fileDir + "/libraries/J2_temps/ORG_CREATION/org_creation_template.j2", org_data=fileDir + "/Topology/ORG_DATA.csv", org_name="JAN18")
    # result = cpe1.Config_Node_Devices("NV-WC01-N2-BLR", "JAN18", node_template="WC_Template.j2", node_data="WC.csv")
    # result = cpe1.Config_Node_Devices("NV-WC02-N2-BLR", "JAN18", node_template="WC_Template.j2", node_data="WC.csv")
    # result = cpe1.Config_Node_Devices("NV-WC01-N4-MUM", "JAN18", node_template="WC_Template.j2", node_data="WC.csv")
    # result = cpe1.Config_Node_Devices("NV-WC02-N4-MUM", "JAN18", node_template="WC_Template.j2", node_data="WC.csv")
##GW
    result = cpe1.Config_Node_Devices("NV-GW01-N2-BLR", "JAN18", node_template="GW_Template.j2", node_data="GW.csv")
    result = cpe1.Config_Node_Devices("NV-GW02-N2-BLR", "JAN18", node_template="GW_Template.j2", node_data="GW.csv")
    result = cpe1.Config_Node_Devices("NV-GW01-N4-MUM", "JAN18", node_template="GW_Template.j2", node_data="GW.csv")
    result = cpe1.Config_Node_Devices("NV-GW02-N4-MUM", "JAN18", node_template="GW_Template.j2", node_data="GW.csv")

    # print result
    # cpe1 = VersaLib('AADEC26_CPE1_MUM', topofile=fileDir + "/Topology/Devices.csv")
    # main_logger = setup_logger('Versa-director', 'Post_staging_templates')
    # temp_data = cpe1.get_PS_templates()
    # for idx , i in  temp_data.iteritems():
    #     main_logger.info(i)
    cpe1 = VersaLib('JAN18_CPE2_BLR', topofile=fileDir + "/Topology/Devices.csv")
    # # print cpe1.ESP_IP
    # # val =  cpe1.get_data_dict()
    # # print val['ORG_NAME']
    # cpe1.create_PS_and_DG('Post_staging_template.j2', 'Device_group_template.j2', 'PS_main_template_modify.j2')
    # cpe1.pre_onboard_work('Device_template.j2', 'Staging_server_config.j2', 'staging_cpe.j2')
    # cpe1.cpe_onboard_call()
    # cpe1_dev_info_on_vd =  cpe1.get_device_info()
    # print cpe1_dev_info_on_vd
    # cpe1.shutdown_interface(cpe1.MPLS_WAN_INTF)
    # time.sleep(5)
    # print cpe1.get_interface_data_from_vd(cpe1.MPLS_WAN_INTF)
    # time.sleep(20)
    # cpe1.unshutdown_interface(cpe1.MPLS_WAN_INTF)
    # time.sleep(5)
    # print cpe1.get_interface_data_from_vd(cpe1.MPLS_WAN_INTF)
    # cpe1_shell_nc =  cpe1.shell_login()
    # cpe1_vd_nc = cpe1.cross_login()
    # vd_nc = cpe1.login(vd_login='yes')
    # print cpe1_vd_nc
    # print cpe1_shell_nc.send_command_expect("cli", expect_string=">", strip_prompt=False, strip_command=False)
    # result = cpe1.ping(cpe1.data_dict['peer_lan_first_host'][cpe1.data_dict['lan_vlan'][0]], count=4, routing_instance=routing_instances[0], source=cpe1.data_dict['lan_first_host'][cpe1.data_dict['lan_vlan'][0]])
    # print "*" * 20 + "\n" +result
    # result = cpe1.send_commands_and_expect("show interfaces brief | match ptvi33 | tab")
    # print "*" * 20 + "\n" + result
    ##########################################
    # result = cpe1.ping(cpe1.data_dict['peer_lan_first_host'][cpe1.data_dict['lan_vlan'][0]], count=4, routing_instance=routing_instances[0], source=cpe1.data_dict['lan_first_host'][cpe1.data_dict['lan_vlan'][0]])
    # print "*" * 20 + "\n" +result
    # result = cpe1.send_commands_and_expect("show interfaces brief | match ptvi33 | tab")
    # print "*" * 20 + "\n" + result
    # ##############################################
    # cpe2 = VersaLib('CPE-46', topofile=fileDir + "/Topology/Devices.csv")
    # cpe2.create_PS_and_DG('Post_staging_template.j2', 'Device_group_template.j2', 'PS_main_template_modify.j2')
    # cpe2.pre_onboard_work('Device_template.j2', 'Staging_server_config.j2', 'staging_cpe.j2')
    # cpe2.cpe_onboard_call()
    # cpe2_dev_info_on_vd =  cpe2.get_device_info()
    # print cpe2_dev_info_on_vd
    # VM1 = VersaLib('VM1_MUM', fileDir + "/Topology/Devices.csv")
    # VM2 = VersaLib('VM2_MUM', fileDir + "/Topology/Devices.csv")
    # VM1_data = VM1.get_data_dict()
    # print VM1_data
    # VM1.VM_nc = VM1.shell_login()
    # VM2.VM_nc = VM2.shell_login()
    # VM1.VM_pre_op()
    # VM2.VM_pre_op()
    # print VM1.shell_ping(VM1.data_dict['peer_lan_second_host'][VM1.data_dict['lan_vlan'][0]])
    # print VM2.shell_ping(VM2.data_dict['peer_lan_second_host'][VM2.data_dict['lan_vlan'][0]])
    print datetime.now()


if __name__ == "__main__":
    main()
