#!/usr/bin/env python
'''Command line for expanding Jinja2 templates.
    Template variables can be passed either via the command line (using -vX=Y) or
    via a JSON/YAML configuration file (using -i /path/to/vars.json)
    Example:
        $ echo 'Hello {{name}}' > template.txt
        $ jj2.py -v name=Bugs template.txt
        Hello Bugs
        $
'''

import os, sys, json, yaml
from argparse import ArgumentParser, FileType
from jinja2 import meta, Environment, FileSystemLoader, StrictUndefined

if __name__ == "__main__":
    fileDir = os.path.dirname(os.path.dirname(os.path.realpath('__file__')))
else:
    fileDir = os.path.dirname(os.path.realpath('__file__'))

class TemplateParser:

    def __init__(self):
        pass

    def template_parse(self, input_yml_file, template_jinja_file):

        os.chdir(fileDir)
        os.chdir("..")
        pwd = os.getcwd()

        with open(pwd + "\\libraries\\CGW_config\\" + input_yml_file) as fp1:
        #with open("C:\\NV_REPOSITORY\\csit\\libraries\\CGW_config\\" + input_yml_file) as fp1:
            input_data = yaml.safe_load(fp1)

        self.template_vars = {}
        self.template_vars.update(input_data)

        # Fail on undefined
        self.env = Environment(undefined=StrictUndefined, trim_blocks=True, lstrip_blocks=True)
        self.env.loader = FileSystemLoader('.')

        with open(pwd + "\\libraries\\CGW_config\\" + template_jinja_file) as fp2:
        #with open("C:\\NV_REPOSITORY\\csit\\libraries\\CGW_config\\" + template_jinja_file) as fp2:
            template_str = fp2.read()

        self.template = self.env.from_string(template_str)
        self.cmds = self.template.render(self.template_vars)
        self.device_name = self.template_vars["HOSTNAME"]

        return {"commands" : self.cmds, "device_name" : self.device_name}

# obj = TemplateParser()
# print obj.template_parse("cgw_primary.yml", 'cgw_tenant_creation.j2')
# print obj.template_parse("cgw_secondary.yml", 'cgw_tenant_creation.j2')
# print obj.template_parse("wc_primary.yml", 'wc_tenant_creation.j2')
# print obj.template_parse("wc_secondary.yml", 'wc_tenant_creation.j2')
