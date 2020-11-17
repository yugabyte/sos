# Copyright (C) 2020 Yugabyte, Tyler Ramer <tramer@yugabyte.com>, Jim Doty <jdoty@yugabyte.com>
#
# See the LICENSE file in the source distribution for further information.

from sos.plugins import Plugin, RedHatPlugin, DebianPlugin, UbuntuPlugin



class Yugabyte(Plugin, RedHatPlugin, DebianPlugin, UbuntuPlugin):
    """Yugabyte
    """

    short_desc = 'Yugabyte Database'

    plugin_name = 'yugabyte'
    profiles = ('services',)
    files = ('/home/yugabyte/bin/ycqlsh',)

    option_list = [
        ("master_port","master server management port number", "", 7100),
        ("tserver_port","tserver management port number", "", 9100),
    ]


    def setup(self):
        self.add_copy_spec([
            "/home/yugabyte/tserver/logs",
            "/home/yugabyte/master/logs",
            "/home/yugabyte/cores",
        ])
        self.add_cmd_output([
            "/home/yugabyte/bin/yb-admin -master_addresses localhost:%s,127.0.0.1:%s dump_masters_state CONSOLE" % (self.get_option("master_port"), self.get_option("master_port")),
            "curl localhost:7000/table-servers", # can these ports change?
            "curl localhost:7000/vars",
            "curl localhost:7000/cluster-config",
            "curl localhost:7000/tables",
        ])


# TODO
#class YugabytePostgres(Yugabyte, IndependentPlugin):
#    files ('/home/yugabyte/bin/postgres',) # is this file only present if postgres is enabled?
#
#    def setup(self):
#        super(YugabytePostgres, self).setup()
#


