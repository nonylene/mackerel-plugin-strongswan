# mackerel-plugin-strongswan

`mackerel-plugin-strongswan` is a mackerel-agent plugin for StrongSwan. This monitors StrongSwan Charon status via [vici](https://wiki.strongswan.org/projects/strongswan/wiki/VICI) interface.

## Metrics

### `custom.strongswan.sas.*`

Active `IKE_SA` counts

### `custon.strongswan.pools.*`

Usage of IP address pools

## Reqruirements

- StrongSwan
  - vici plugin is required (enabled by default)
  - Tested manually with 5.5.x
- Python 3.4 ~
- [Pipenv](https://github.com/pypa/pipenv)

## Usage

```
$ pipenv install
$ sudo pipenv run main.py # should output metrics
```

### Example mackerel config

```
[plugin.metrics.strongswan]
command = "/opt/mackerel-plugin-strongswan/.venv/bin/python3 /opt/mackerel-plugin-strongswan/main.py"
```
