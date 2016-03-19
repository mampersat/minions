# Minions
Deploying a fleet of raspberry pi's in various places with various sensors. This is a place to keep the code they run 

```
git clone https://github.com/mampersat/minions.git
```

Add to /etc/rc.local for auto starting
```
sudo python /home/pi/minions/loop.py &
```
