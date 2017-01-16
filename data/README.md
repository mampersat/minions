To start the falcon API
```
matt@matt-ubuntu-desktop:~/minions/data$ gunicorn -b 192.168.1.114:8000 minions:app
```

To check database growth
```
SELECT table_schema "Data Base Name",
    sum( data_length + index_length ) / 1024 / 1024 "Data Base Size in MB",
    sum( data_free )/ 1024 / 1024 "Free Space in MB"
FROM information_schema.TABLES
GROUP BY table_schema ; 
```

On 2017-01-16 (running 2 minions for about 3 days)
```
+--------------------+----------------------+------------------+
| Data Base Name     | Data Base Size in MB | Free Space in MB |
+--------------------+----------------------+------------------+
| django             |           0.40625000 |      28.00000000 |
| information_schema |           0.15625000 |      80.00000000 |
| kegbot             |           1.25000000 |      56.00000000 |
| minion             |           2.53125000 |       4.00000000 |
| mysql              |           2.42857838 |       2.00047302 |
| performance_schema |           0.00000000 |       0.00000000 |
| sys                |           0.01562500 |       0.00000000 |
+--------------------+----------------------+------------------+
```
