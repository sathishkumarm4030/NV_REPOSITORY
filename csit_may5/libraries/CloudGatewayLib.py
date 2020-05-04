import os, sys, json, yaml, re, itertools,time
from argparse import ArgumentParser, FileType
from jinja2 import meta, Environment, FileSystemLoader, StrictUndefined
from csit.libraries.VersaLib import VersaLib
from csit.libraries.CiscoLib import CiscoLib
from csit.libraries.TemplateParser import TemplateParser

def try_literal_eval(s):
    try:
        return literal_eval(s)
    except ValueError:
        return s

if __name__ == "__main__":
    fileDir = os.path.dirname(os.path.dirname(os.path.realpath('__file__')))
else:
    fileDir = os.path.dirname(os.path.realpath('__file__'))

Par_Dir = os.path.dirname(fileDir)
sys.path.append(Par_Dir)


class CloudGatewayLib():
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        pass

    def cloud_gateway_command_generation(self, action, solution_type):

        res1 = res2 = res3 = res4 = {}
        obj = TemplateParser()
        if (action == "CREATE"):
            print "Cloud Gateway Tenant Create Action."
            res1 = obj.template_parse("cgw_primary.yml", 'cgw_tenant_creation.j2')
            res3 = obj.template_parse("wc_primary.yml", 'wc_tenant_creation.j2')
            res4 = obj.template_parse("wc_secondary.yml", 'wc_tenant_creation.j2')
            if (solution_type == "DUAL"):
                res2 = obj.template_parse("cgw_secondary.yml", 'cgw_tenant_creation.j2')

        elif (action == "DELETE"):
            print "Delete action"
            res1 = obj.template_parse("cgw_primary.yml", 'cgw_tenant_deletion.j2')
            res3 = obj.template_parse("wc_primary.yml", 'wc_tenant_deletion.j2')
            res4 = obj.template_parse("wc_secondary.yml", 'wc_tenant_deletion.j2')
            if (solution_type == "DUAL"):
                res2 = obj.template_parse("cgw_secondary.yml", 'cgw_tenant_deletion.j2')
        else:
            print "Incorrect action."
            return []

        result = [res1,res2,res3,res4]
        return result


    def get_cgw_cmds(self,result):

        device_list = []
        cmds_list = []

        for res in result:
            if bool(res):
                device_list.append(res["device_name"])
                cmds_list.append(res["commands"])

        return (device_list, cmds_list)

    def cgw_config_from_vd_cli(self, vd, vdnc, device_list, cmds_list):

        count = 0
        for device in device_list:
            if (device != ""):
                if (VersaLib.request_check_sync(vd, vdnc, device) == "False"):
                    if (VersaLib.request_sync_from_cpe(vd, vdnc, device) == "False"):
                        return

        for (device, cmds) in itertools.izip_longest(device_list, cmds_list):
            if ((device != "") and (cmds != "")):
                if(vd.config_devices_template_using_template_parser(nc=vdnc, cmds=cmds, device_name=device)):
                    count+=1
        if ((count == len(device_list)) and (len(device_list) != 0)):
            return 1
        else:
            return 0

    def cloud_peer_create(self, input_yml_file, input_jinja_file, solution_type):

        obj1 = CiscoLib()
        telnet_handler = obj1.shell_login_cisco(input_yml_file, solution_type)
        obj2 = TemplateParser()
        device_details = obj2.template_parse(input_yml_file, input_jinja_file)
        commands = device_details["commands"]
        device_name = device_details["device_name"]

        peer_config_result = obj1.cisco_config(telnet_handler, commands, device_name)
        telnet_handler.disconnect()

        return peer_config_result

    def cloud_peer_delete(self, input_yml_file, input_jinja_file, solution_type):

        obj1 = CiscoLib()
        telnet_handler = obj1.shell_login_cisco(input_yml_file, solution_type)
        obj2 = TemplateParser()
        device_details = obj2.template_parse(input_yml_file, input_jinja_file)
        commands = device_details["commands"]
        device_name = device_details["device_name"]

        peer_config_result = obj1.cisco_config(telnet_handler, commands, device_name)
        telnet_handler.disconnect()

        return peer_config_result

    def cpe_lan_route_verify(self, cpe_name, loopback_ip_list, solution_type, CGW1_ESP_IP, CGW2_ESP_IP=None):

        # SDWAN CPE Verification
        cpe = VersaLib(cpe_name, topofile="Devices.csv")
        lan_vrf = "1"
        main_logger = cpe.setup_logger(cpe_name, 'CPE LAN Verification')
        cnc = cpe.cross_login()

        output = cpe.check_lan_route(str(lan_vrf))
        print output
        main_logger.info(output)

        match2 = 1
        count = 0
        # Pattern match e.g. : BGP N/A +100.172.10.10/32 10.72.64.18 Indirect
        for ip in loopback_ip_list:
            regex1 = r"(BGP)\s+.*\s+\+*" + ip + "/32\s+" + CGW1_ESP_IP + "\s+Indirect"
            match1 = re.search(regex1, output)
            if (solution_type == "DUAL"):
                regex2 = r"(BGP)\s+.*\s+\+*" + ip + "/32\s+" + CGW2_ESP_IP + "\s+Indirect"
                match2 = re.search(regex2, output)

            if ((match1) and (match2)):
                count += 1
        return count

    def get_cpe_lan_ip(self, cpe_name):

        lan_ip = ""
        cpe = VersaLib(cpe_name, topofile="Devices.csv")
        self.vlan = cpe.START_VLAN
        self.lan_intf = cpe.LAN_INTF

        cnc = cpe.cross_login()
        cmd = "show interfaces brief | tab | match " + str(self.lan_intf + "." + str(self.vlan))
        output = cpe.cnc.send_command_expect(cmd, expect_string=">", strip_prompt=False, strip_command=False)
        regex = r"((\d{1,3}.){3}\d{1,3})/\d{1,2}"
        match = re.search(regex, output)

        lan_ip = match.group(1)
        print "CPE LAN1-VRF interface ip is found to be : " + lan_ip + "\n"
        return lan_ip

    def cpe_cgw_ping_test(self, cpe_name, loopback_ip_list, lan_ip):

        total = 0
        cpe = VersaLib(cpe_name, topofile="Devices.csv")
        main_logger = cpe.setup_logger(cpe_name, 'CPE to CGW Ping Test')

        cnc = cpe.cross_login()
        for ip in loopback_ip_list:
            result = cpe.ping(ip, routing_instance="LAN1-VRF", source=lan_ip)
            print result
            main_logger.info("Ping test result between CPE and CGW loopback ip : " + ip + "\n")
            main_logger.info(result)

            if (result == "True"):
                total+=1
        return total