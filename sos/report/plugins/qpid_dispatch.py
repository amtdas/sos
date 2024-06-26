# Copyright (C) 2015 Red Hat, Inc., Pavel Moravec <pmoravec@redhat.com>

# This file is part of the sos project: https://github.com/sosreport/sos
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# version 2 of the GNU General Public License.
#
# See the LICENSE file in the source distribution for further information.

from socket import gethostname
from sos.report.plugins import Plugin, RedHatPlugin, PluginOpt


class QpidDispatch(Plugin, RedHatPlugin):

    short_desc = 'Qpid dispatch router'

    plugin_name = 'qpid_dispatch'
    profiles = ('services',)

    packages = ('qdrouterd', 'qpid-dispatch-tools', 'qpid-dispatch-router')
    option_list = [
        PluginOpt('port', default='', val_type=int,
                  desc='listening port to connect to'),
        PluginOpt('ssl-certificate', default='', val_type=str,
                  desc='Path to file containing client SSL certificate'),
        PluginOpt('ssl-key', default='', val_type=str,
                  desc='Path to file containing client SSL private key'),
        PluginOpt('ssl-trustfile', default='', val_type=str,
                  desc='trusted CA database file')
    ]

    def setup(self):
        """ performs data collection for qpid dispatch router """
        options = ""
        if self.get_option("port"):
            options = (options + " -b " + gethostname() +
                       f":{self.get_option('port')}")
        # gethostname() is due to DISPATCH-156

        # for either present option, add --option=value to 'options' variable
        for option in ["ssl-certificate", "ssl-key", "ssl-trustfile"]:
            if self.get_option(option):
                options = (options + f" --{option}=" +
                           self.get_option(option))

        self.add_cmd_output([
            "qdstat -a" + options,  # Show Router Addresses
            "qdstat -n" + options,  # Show Router Nodes
            "qdstat -c" + options,  # Show Connections
            "qdstat -m" + options   # Show Broker Memory Stats
        ])

        self.add_copy_spec([
            "/etc/qpid-dispatch/qdrouterd.conf"
        ])

# vim: et ts=4 sw=4
