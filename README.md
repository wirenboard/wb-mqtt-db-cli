Examples
---------

Outputs at max 10 points per channel trying to evenly distribute the data points. Note the "-a" switch.


```
$ wb-mqtt-db-cli -h 192.168.0.175 --from "2017-06-01" --to "2017-06-02" --decimal-places 2 --limit 10 -a  wb-adc/5Vout wb-adc/Vin
channel time    average min max
wb-adc/5Vout    2017-06-01 00:00:46.269996  5.10    5.09    5.11
wb-adc/5Vout    2017-06-01 00:24:46.311995  5.10    5.09    5.11
wb-adc/5Vout    2017-06-01 01:52:46.267987  5.10    5.09    5.11
wb-adc/5Vout    2017-06-01 03:20:46.274994  5.10    5.09    5.11
wb-adc/5Vout    2017-06-01 04:56:46.329006  5.10    5.08    5.12
wb-adc/5Vout    2017-06-01 06:18:46.279990  5.10    5.09    5.11
wb-adc/5Vout    2017-06-01 07:46:46.291987  5.10    5.08    5.11
wb-adc/5Vout    2017-06-01 09:16:46.297016  5.10    5.09    5.11
wb-adc/5Vout    2017-06-01 10:44:46.296983  5.10    5.09    5.11
wb-adc/5Vout    2017-06-01 12:12:58.520983  5.10    5.09    5.11
wb-adc/Vin  2017-06-01 00:06:46.257986  11.98   11.94   12.02
wb-adc/Vin  2017-06-01 00:26:46.305993  11.98   11.94   12.02
wb-adc/Vin  2017-06-01 01:56:46.262983  11.98   11.92   12.02
wb-adc/Vin  2017-06-01 03:20:46.270005  11.98   11.93   12.02
wb-adc/Vin  2017-06-01 04:50:46.323998  11.98   11.93   12.02
wb-adc/Vin  2017-06-01 06:18:46.275002  11.98   11.94   12.02
wb-adc/Vin  2017-06-01 07:52:46.294017  11.98   11.93   12.02
wb-adc/Vin  2017-06-01 09:20:46.314986  11.98   11.93   12.02
wb-adc/Vin  2017-06-01 10:46:46.292993  11.98   11.92   12.02
wb-adc/Vin  2017-06-01 12:18:58.514002  11.98   11.93   12.02
```


Without "-a" switch the behaviour is different: only the first 10 data points are returned:


```
wb-mqtt-db-cli -h 192.168.0.175 --from "2017-06-01" --decimal-places 2 --limit 10  wb-adc/5Vout 
channel time    average min max
wb-adc/5Vout    2017-06-01 00:00:46.269996  5.10    5.09    5.11
wb-adc/5Vout    2017-06-01 00:02:46.265000  5.10    5.09    5.11
wb-adc/5Vout    2017-06-01 00:04:46.270988  5.10    5.09    5.11
wb-adc/5Vout    2017-06-01 00:06:46.263980  5.10    5.09    5.11
wb-adc/5Vout    2017-06-01 00:08:46.262002  5.10    5.09    5.11
wb-adc/5Vout    2017-06-01 00:10:46.265012  5.10    5.09    5.11
wb-adc/5Vout    2017-06-01 00:12:46.267982  5.10    5.09    5.11
wb-adc/5Vout    2017-06-01 00:14:46.270993  5.10    5.09    5.11
wb-adc/5Vout    2017-06-01 00:16:46.270020  5.10    5.09    5.11
wb-adc/5Vout    2017-06-01 00:18:46.264983  5.10    5.09    5.11
```

The custom delimiter can be specified using "-d" switch:

```
$ wb-mqtt-db-cli -h 192.168.0.175 --from "2017-06-01" --limit 5 -d';'  wb-adc/5Vout  
channel;time;average;min;max
wb-adc/5Vout;2017-06-01 00:00:46.269996;5.10218045112783;5.09;5.11
wb-adc/5Vout;2017-06-01 00:02:46.265000;5.10255639097746;5.09;5.11
wb-adc/5Vout;2017-06-01 00:04:46.270988;5.10195488721806;5.09;5.11
wb-adc/5Vout;2017-06-01 00:06:46.263980;5.10150375939851;5.09;5.11
wb-adc/5Vout;2017-06-01 00:08:46.262002;5.10142857142858;5.09;5.11
```

Custom time format example:

```
$ wb-mqtt-db-cli -h 192.168.0.175 --from "2017-06-01" --time-format="%Y/%m/%d %H:%M:%S" --decimal-places 2 --limit 10  wb-adc/5Vout 
channel time    average min max
wb-adc/5Vout    2017/06/01 00:00:46 5.10    5.09    5.11
wb-adc/5Vout    2017/06/01 00:02:46 5.10    5.09    5.11
wb-adc/5Vout    2017/06/01 00:04:46 5.10    5.09    5.11
wb-adc/5Vout    2017/06/01 00:06:46 5.10    5.09    5.11
wb-adc/5Vout    2017/06/01 00:08:46 5.10    5.09    5.11
wb-adc/5Vout    2017/06/01 00:10:46 5.10    5.09    5.11
wb-adc/5Vout    2017/06/01 00:12:46 5.10    5.09    5.11
wb-adc/5Vout    2017/06/01 00:14:46 5.10    5.09    5.11
wb-adc/5Vout    2017/06/01 00:16:46 5.10    5.09    5.11
wb-adc/5Vout    2017/06/01 00:18:46 5.10    5.09    5.11
```