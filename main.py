#!/usr/bin/env python3
import optparse
import sys
import time
import vultr


class RemoteWorkstation:
    DCID = 25  # Tokyo
    VPS_PLAN_ID = 204  # 8192 MB RAM,160 GB SSD,4.00 TB BW
    OS_ID = 387  # Ubuntu 20.04
    HOSTNAME = 'nyao'

    def __init__(self, token, server_label='remote_workstation', firewall_id=None, snapshot_id=None,
                 reserved_ip_v4=None, startup_script_id=None):
        self.token = token
        self.server_label = server_label
        self.firewall_id = firewall_id
        self.snapshot_id = snapshot_id
        self.reserved_ip_v4 = reserved_ip_v4
        self.startup_script_id = startup_script_id

    def __manager(self):
        return vultr.Vultr(self.token)

    def get_ssh_key_ids(self):
        resp = self.__manager().sshkey.list()
        if len(resp) == 0:
            return ""

        return ",".join(list(resp.keys()))

    def get_server_by_sub_id(self, sub_id):
        resp = self.__manager().server.list(sub_id)
        if len(resp) == 0:
            return None

        return resp

    def get_server_by_label(self):
        resp = self.__manager().server.list(params={"label": self.server_label})
        if len(resp) == 0:
            return None

        first_key = list(resp.keys())[0]
        return resp[first_key]

    def __create_server(self, params):
        resp = self.__manager().server.create(self.DCID, self.VPS_PLAN_ID, self.OS_ID, params)
        return resp["SUBID"]

    def get_or_create_server(self):
        s = self.get_server_by_label()
        if s is not None:
            return s

        ssh_key_ids = self.get_ssh_key_ids()
        params = {
            "label": self.server_label,
            "userdata": self.__user_data(),
            "hostname": self.HOSTNAME,
            "SSHKEYID": ssh_key_ids,
        }
        if self.snapshot_id is not None and self.snapshot_id is not "":
            params["SNAPSHOTID"] = self.snapshot_id
        if self.firewall_id is not None and self.firewall_id is not "":
            params["FIREWALLGROUPID"] = self.firewall_id
        if self.reserved_ip_v4 is not None and self.reserved_ip_v4 is not "":
            params["reserved_ip_v4"] = self.reserved_ip_v4
        if self.startup_script_id is not None and self.startup_script_id is not "":
            params["SCRIPTID"] = int(self.startup_script_id)

        server_id = self.__create_server(params)

        for _ in range(10):
            s = self.get_server_by_sub_id(server_id)
            if s is not None and s["status"] == "active":
                return s
            time.sleep(5)  # 5sec

        return server_id

    def destroy_server(self):
        s = self.get_server_by_label()
        if s is not None:
            self.__manager().server.destroy(s["SUBID"])


if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('--token', action='store', dest='token')
    parser.add_option('--snapshot-id', action='store', dest='snapshot_id')
    parser.add_option('--reserved-ip-v4', action='store', dest='reserved_ip_v4')
    parser.add_option('--firewall-id', action='store', dest='firewall_id')
    parser.add_option('--startup-script-id', action='store', dest='startup_script_id')
    options, args = parser.parse_args()

    if options.token is None or options.token == "":
        print('Error: --token is required\n', file=sys.stderr)
        sys.exit(1)

    if len(args) == 0:
        print('Error: command is required\ncreate or destroy', file=sys.stderr)
        sys.exit(1)

    cmd = args[0]
    ws = RemoteWorkstation(token=options.token,
                           snapshot_id=options.snapshot_id,
                           reserved_ip_v4=options.reserved_ip_v4,
                           firewall_id=options.firewall_id,
                           startup_script_id=options.startup_script_id)

    if cmd == "create":
        server = ws.get_or_create_server()
        print(server["SUBID"])
        print(server["main_ip"])
    elif cmd == "destroy":
        ws.destroy_server()
        print('destroyed')
    else:
        print('unknown command')
