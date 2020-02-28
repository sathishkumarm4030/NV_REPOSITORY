#!/usr/bin/env python

import os, sys, json, yaml, urllib3
from argparse import ArgumentParser, FileType
from jinja2 import meta, Environment, FileSystemLoader, StrictUndefined
import errno
from netmiko import ConnectHandler
from datetime import datetime

currtime = str(datetime.now())
currtime = currtime.replace(" ", "_").replace(":", "_").replace("-", "_").replace(".", "_")
from ast import literal_eval
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from csit.libraries.VersaLib import VersaLib
from csit.libraries.VersaLib import write_result_from_dict
from TemplateParser import *

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

logfile_dir = os.path.dirname(os.path.dirname(os.path.realpath('__file__'))) + "/LOGS/"+ currtime + "/"
if not os.path.exists(os.path.dirname(logfile_dir)):
    try:
        os.mkdir(os.path.dirname(logfile_dir))
    except OSError as exc:  # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise

class CiscoLib():
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        pass

    def shell_login_cisco(self, input_yml_file, solution_type):

        os.chdir(fileDir)
        os.chdir("..")
        pwd = os.getcwd()

        with open(pwd + "\\libraries\\CGW_config\\" + input_yml_file) as fp1:
        #with open("C:\\NV_REPOSITORY\\csit\\libraries\\CGW_config\\" + input_yml_file) as fp1:
            input_data = yaml.safe_load(fp1)

        device_dict = {
            'device_type': 'cisco_ios_telnet',
            'ip': input_data["MGMT_IP"],
            'username': input_data["USERNAME"],
            'password': input_data["PASSWORD"],
        }
        input_data["SOLUTION_TYPE"] = solution_type

        with open(pwd + "\\libraries\\CGW_config\\" + input_yml_file, 'w') as outfile:
        #with open("C:\\NV_REPOSITORY\\csit\\libraries\\CGW_config\\" + input_yml_file, 'w') as outfile:
            yaml.dump(input_data, outfile, default_flow_style=False)

        try:
            self.shell_nc = ConnectHandler(**device_dict)
            print self.shell_nc.send_command_expect('config terminal', expect_string='#')
            return self.shell_nc
        except Exception as e:
            print "Error found : " + str(e)

    def cisco_config(self, shell_nc, cmds, device_name):

        obj = VersaLib(device_name)
        start_time = datetime.now()
        main_logger = obj.setup_logger("Cisco device configuration for Cloud Peering Services", 'Config_devices_template')
        result_dict = {}
        res_check = ""
        dev_dict = {}

        dev_dict['NAME'] = device_name
        main_logger.info(cmds)
        result = obj.device_config_commands_wo_split(shell_nc, cmds)
        main_logger.info(result)
        result_dict[dev_dict['NAME']] = res_check

        main_logger.info("CONFIG_RESULT:")
        for k, v in result_dict.iteritems():
            main_logger.info([k, v])
        write_result_from_dict(result_dict)
        main_logger.info("Time elapsed: {}\n".format(datetime.now() - start_time))
        main_logger.info("LOGS Stored in : " + logfile_dir)

        res_check += result
        if "% IPv4" in result:
            return 1
        elif "% " in result:
            return 0
        else:
            return 1

# obj = CiscoLib()
# obj.shell_login_cisco("cisco_device_details.yml", "DUAL")