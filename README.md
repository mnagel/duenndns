# duenndns

this is the duenndns tool to update dynamic dns records

## Installation

Make the script executable and drop it somewhere in your `$PATH`.

You need to have a nameserver somewhere that accepts updates via `nsupdate`
and you will need the respective private key.

For information how to configure BIND in a compatible way,
see e.g. http://andrwe.org/linux/own-ddns.

## Usage

Usage: duenndns.py [options]

You need to specify all the options like in the example below.

```
python duenndns.py \
  --key Kxxx.tsigkey.+111+11111.private \
  --nameserver ns0.example.com \
  --zone dyn.example.com \
  --client funny-hostname \
  --ip 127.0.0.1
```

You can enable IP autodiscovery by skipping the `--ip` option like so:

```
python duenndns.py \
  --key Kxxx.tsigkey.+111+11111.private \
  --nameserver ns0.example.com \
  --zone dyn.example.com \
  --client funny-hostname
```
  
Expected output:

```
[...]
ip is None, starting autodiscovery
autodiscovery found 8.8.8.8
[...]
```

## Options

```
Usage: duenndns.py [options]

this is the duenndns tool to update dynamic dns records

Options:
  -h, --help            show this help message and exit
  --key=KEY             key.
  --nameserver=NAMESERVER
                        nameserver.
  --zone=ZONE           zone.
  --client=CLIENT       client.
  --ip=IP               ip. skip this option to trigger autodiscovery.
  --ttl=TTL             ttl.
  --check               check only via dig, do not update.
```

## Contact

via https://github.com/mnagel/duenndns

## Credits

inspired by and a lot of initial help from: Philipp Kern

## License

Files:

* `*`

Copyright:

* 2013 Michael Nagel ubuntu@nailor.devzero.de

License:

* Michael Nagel: "Donated into the Public Domain."
