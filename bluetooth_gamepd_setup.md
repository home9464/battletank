
https://bluedot.readthedocs.io/en/latest/pairpipi.html#using-the-command-line

### Run the tool

```
bluetoothctl
```


### See connected devices

```bash
paired-devices

Device D2:3E:21:FF:12:8E StadiaMFMP-027f
```

### Remove malfunctional device

```bash
remove D2:3E:21:FF:12:8E

```

### Find the MAC address of the gamepad Google Stadia
```
scan on
```


### Connect and trust the gamepad
```
trust D2:3E:21:FF:12:8E
connect D2:3E:21:FF:12:8E
pair D2:3E:21:FF:12:8E
```
