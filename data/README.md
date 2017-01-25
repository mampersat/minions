To start the falcon API
```
matt@matt-ubuntu-desktop:~/minions/data$ gunicorn -b 192.168.1.114:8000 minions:app
```

To check database growth
```
SELECT table_schema "Data Base Name",
    sum( data_length + index_length ) / 1024 / 1024 "Data Base Size in MB",
    sum( data_free )/ 1024 / 1024 "Free Space in MB"
FROM information_schema.TABLES WHERE table_schema = 'minion'
GROUP BY table_schema ; 
```

On 2017-01-16 (running 2 minions for about 3 days)
```
+--------------------+----------------------+------------------+
| Data Base Name     | Data Base Size in MB | Free Space in MB |
+--------------------+----------------------+------------------+
| minion             |           2.53125000 |       4.00000000 |
+--------------------+----------------------+------------------+
```
On 2017-01-22 (running 2 minions for about 10 days)
```
+----------------+----------------------+------------------+
| Data Base Name | Data Base Size in MB | Free Space in MB |
+----------------+----------------------+------------------+
| minion         |           4.53125000 |       4.00000000 |
+----------------+----------------------+------------------+
```

