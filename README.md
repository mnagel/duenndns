# duenndns

this is the duenndns tool to update dynamic dns records

## Installation

Make the script executable and drop it somewhere in your `$PATH`.

You need to have a nameserver somewhere that accepts updates via `nsupdate`
and you will need the respective private key.

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
  --ip=IP               ip.
  --ttl=TTL             ttl.
```

## Contact

via https://github.com/mnagel/duenndns

## Credits

inspired by and a lot of initial help from: Philipp Kern

## License

Files:

* `*.*`

Copyright:

* 2013 Michael Nagel ubuntu@nailor.devzero.de

License:

* Michael Nagel: "Donated into the Public Domain."
