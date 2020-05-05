# remote-workstation

Do not use this repository if you are not upamune.

## Requirements

- Python 3.6.10
- Pipenv

## Preparation
1. Add SSH Keys in [web console](https://my.vultr.com/settings/#settingssshkeys)
1. Enable API in [web console](https://my.vultr.com/settings/#settingsapi)
1. (optional) Add a startup script in [web console](https://my.vultr.com/startup/manage)
1. (optional) Add a firewall in [web console](https://my.vultr.com/firewall/)
1. (optional) Add a Reserved IP in [web console](https://my.vultr.com/network/#network-reservedips)

## Execute

### Create

Idempotently by label. Default label is `remote-workstation`.

#### Options

- `--firewall-id`
  - optional
- `--reserved-ip-v4`
  - optional
- `--startup-script-id`
  - optional
- `--snapshot-id`
  - optional


#### Example 

```shell script
# Create an instance from startup script.
$ python ./main.py create --token "${VULTR_API_KEY}" --firewall-id foo --startup-script-id bar --reserved-ip-v4 203.0.113.1

# Create an instance from snapshot.
$ python ./main.py create --token "${VULTR_API_KEY}" --firewall-id foo --snapshot-id bar --reserved-ip-v4 203.0.113.1
```

### Destroy

```shell script
$ python ./main.py destroy --token "${VULTR_API_KEY}"
```

## Development

1. `pipenv sync`
1. `pipenv shell`
1. `pipenv run format`
1. `pipenv run lint`
