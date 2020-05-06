# remote-workstation

![test](https://github.com/upamune/remote-workstation/workflows/test/badge.svg?branch=master)

Do not use this repository if you are not upamune.

## Requirements

- Python 3.6.10
- Pipenv

## Preparation
1. Add SSH Keys in [web console](https://cloud.digitalocean.com/account/security)
1. Generate a personal access token in [web console](https://cloud.digitalocean.com/account/api/tokens)
1. (optional) Add a firewall in [web console](https://cloud.digitalocean.com/networking/firewalls)
1. (optional) Add a floating IP in [web console](https://cloud.digitalocean.com/networking/floating_ips)

## Execute

### Create

Idempotently by name. Default name is `remote-workstation`.

#### Options

- `--token`
  - required
- `--firewall-id`
  - optional
- `--floating-ip`
  - optional
- `--snapshot-id`
  - optional

#### Example 

```shell script
# Create an instance.
$ python ./main.py create --token "${DIGITAL_OCEAN_API_KEY}" --firewall-id "${FIREWALL_ID}" --floating-ip "${FLOATING_IP}"

# Create an instance from snapshot.
$ python ./main.py create --token "${DIGITAL_OCEAN_API_KEY}" --firewall-id "${FIREWALL_ID}" --floating-ip "${FLOATING_IP}" --snapshot-id "${SNAPSHOT_ID}"
```

### Destroy

```shell script
$ python ./main.py destroy --token "${DIGITAL_OCEAN_API_KEY}"
```

## Development

1. `pipenv sync`
1. `pipenv shell`
1. `pipenv run format`
1. `pipenv run lint`
