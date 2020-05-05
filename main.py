#!/usr/bin/env python3
import optparse
import sys
import textwrap
import time
import digitalocean as do


class RemoteWorkstation:
    REGION = 'SGP1'  # Singapore
    SIZE_SLUG = 's-6vcpu-16gb'  # 6vCPUs, 16GB, 320GB, 6TB BW
    IMAGE = 'ubuntu-20-04-x64'  # Ubuntu 20.04 LTS

    def __init__(self,
                 token,
                 server_name='remote-workstation',
                 server_tag='remote-workstation',
                 firewall_id=None,
                 snapshot_id=None,
                 floating_ip=None):
        self.token = token
        self.server_name = server_name
        self.server_tag = server_tag
        self.firewall_id = firewall_id
        self.snapshot_id = snapshot_id
        self.floating_ip = floating_ip

    def __manager(self):
        return do.Manager(token=self.token)

    def get_ssh_keys(self):
        return self.__manager().get_all_sshkeys()

    def get_server_by_tag(self):
        droplets = self.__manager().get_all_droplets(tag_name=self.server_tag)

        for d in droplets:
            if d.name == self.server_name:
                return d

        return None

    def get_server_by_id(self, server_id):
        return self.__manager().get_droplet(server_id)

    def __create_server(self):
        image = self.snapshot_id \
            if self.snapshot_id is not None and self.snapshot_id != "" \
            else self.IMAGE

        ssh_keys = self.get_ssh_keys()

        droplet = do.Droplet(
            token=self.token,
            name=self.server_name,
            tags=[self.server_tag],
            region=self.REGION,
            size=self.SIZE_SLUG,
            image=image,
            ssh_keys=ssh_keys,
            user_data=self.__user_data(),
        )
        droplet.create()

        if self.firewall_id is not None and self.firewall_id != "":
            firewall = self.__manager().get_firewall(self.firewall_id)
            firewall.add_droplets(droplet_ids=[droplet.id])

        if self.floating_ip is not None and self.floating_ip != "":
            actions = droplet.get_actions()
            if len(actions) > 0:
                action = actions[0]
                action.wait()
            floating_ip = self.__manager().get_floating_ip(self.floating_ip)
            floating_ip.assign(droplet_id=droplet.id)

        return droplet.id

    def get_or_create_server(self):
        s = self.get_server_by_tag()
        if s is not None:
            return s

        server_id = self.__create_server()

        for _ in range(10):
            s = self.get_server_by_id(server_id)
            if s is not None:
                return s
            time.sleep(3)

        return server_id

    def destroy_server(self):
        s = self.get_server_by_tag()
        if s is not None:
            if self.floating_ip is not None and self.floating_ip != "":
                ip = self.__manager().get_floating_ip(self.floating_ip)
                ip.unassign()
            s.destroy()

    @staticmethod
    def __user_data():
        return textwrap.dedent('''
        #cloud-config

        runcmd:  
          - mkdir -p /root/.bootstrap
          - curl -sL https://github.com/itamae-kitchen/mitamae/releases/latest/download/mitamae-x86_64-linux.tar.gz | tar xvz
          - mv ./mitamae-x86_64-linux /root/.bootstrap/mitamae
          - curl -sLO https://raw.githubusercontent.com/upamune/remote-workstation/master/recipe.rb
          - mv ./recipe.rb /root/.bootstrap/recipe.rb
          - echo "#!/bin/bash -eu" > /root/.bootstrap/bootstrap.sh
          - echo "./mitamae local recipe.rb" >> /root/.bootstrap/bootstrap.sh
          - chmod +x /root/.bootstrap/bootstrap.sh
        ''').strip()


if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('--token', action='store', dest='token')
    parser.add_option('--snapshot-id', action='store', dest='snapshot_id')
    parser.add_option('--floating-ip', action='store', dest='floating_ip')
    parser.add_option('--firewall-id', action='store', dest='firewall_id')
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
                           floating_ip=options.floating_ip,
                           firewall_id=options.firewall_id)

    if cmd == "create":
        server = ws.get_or_create_server()
        print(server.id)
        print(server.ip_address)
    elif cmd == "destroy":
        ws.destroy_server()
        print('destroyed')
    else:
        print('unknown command')
