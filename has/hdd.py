import sqlite3
conn = sqlite3.connect('/home/matt/home-assistant_v2.db')
c = conn.cursor()
start = '2019-01-19 18:25'
end = '2019-01-20 19:10'

c.execute('select strftime("%s",?) - strftime("%s",?) as seconds;', (end, start))
s = c.fetchone()[0]
print s

c.execute('select sum(state) as burnseconds FROM states'
    ' where entity_id = "sensor.furnace_burntime" AND'
    ' created > ? AND created < ?;', (start, end))
b = c.fetchone()[0]
print b

c.execute('select 65 - (max(state) + min(state)) /2 as heatingdegrees FROM states'
    ' where entity_id = "sensor.outside_north" and state != "unknown" AND'
    ' created > ? AND created < ?;', (start, end))
h = c.fetchone()[0]
print h
