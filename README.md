# NKMS TCP

NKMS is an acronym for Network Keyboard Mouse Switch. `nkms-tcp` switches keyboard and mouse input between muliple computers connected via the network using TCP. This allows you to only have one keyboard and mouse on your desk even if you are using mulitple computers at once. The right control key switches the input between machines.

There is virtually no lag when used with a good ethernet connection, but if you use it over wifi, be prepared to experience a few glitches, especially if the signal is weak.

## Usage

The `nkms-server.py` script should be run on the machine that has the keyboard and mouse. The `nkms-client.py` script should be run on the machines to which you want to transfer that keyboard and mouse input.

Both scripts must be run as root. You will need to install `evdev` if it is not already present in your python environment.

### Server

Normal usage:
```
sudo nkms-server.py
```

Options:

* `-a` or `--address`  
    Address to listen on. Default `0.0.0.0`.
* `-p` or `--port`   
    Port to listen on. Default `4777`.

### Client

Normal usage assuming that the servers IP address is `192.168.1.25`:

```
sudo nkms-client.py --server 192.168.1.25
```

Options:

* `-s` or `--server`  
    Server's address or hostname
* `-p` or `--port`   
    Port to connect to. Default `4777`.