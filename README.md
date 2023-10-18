## A toy project to implement the software for a Remote Controlled Toy Tank

##

```bash
gunicorn "camera:start()" -w 2 --timeout 120 -b 0.0.0.0:5000
```