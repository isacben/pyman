import json
import configparser
import tomllib

#config = configparser.ConfigParser(allow_no_value=True)
#config.read('requests.ini')

#print(json.loads(config['Create payout']['body']))

#print(json.dumps(dict(config['Get Payouts']), indent=4))

with open("requests.toml", mode="rb") as fp:
    t = tomllib.load(fp)

print(json.dumps(t, indent=4))