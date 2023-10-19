# NKMS TCP

`nkms-tcp` switches keyboard and mouse input between muliple computers connected via the network using TCP. This allows you to keep a single keyboard and mouse on your desk even if you are using mulitple computers at once. The right control key switches the input between machines.

## Usage

The `nkms-server.py` script should be run on the machine the has the keyboard and mouse. The `nkms-client.py` script should be run on the machines you want to transfer that keyboard and mouse input to.

Both scripts must be run as root.

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