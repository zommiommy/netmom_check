# NetMon check NetEye4

bisogna fare una snmpwalk per ottenere dei mac address ( ottenibili come: )

```jsx
snmpwalk -v2c -c infra-mrtg 194.244.187.251 IP-MIB::ipNetToMediaPhysAddress | awk '{print $3}'
```

[http://snmplabs.com/pysnmp/examples/hlapi/asyncore/manager/cmdgen/walking-operations.html](http://snmplabs.com/pysnmp/examples/hlapi/asyncore/manager/cmdgen/walking-operations.html)

si normalizza mac address cosi che ci sono sempre 2 numeri e lettere maiuscole in modo che possano matchare con quelli del mysql.

c'e' un db mysql che fa inventario dove devo controllare solamente quanti mac address sono presenti nella tabella. se ce ne sono i non presenti → raisa allarme

la query per mysql prendiamo da `select * from networks`

La query ed il DB devono essere passati come argument.

dobbiamo scrivere i dati su una metric in influx che facciamo col solito | un stdout

La maggior parte dei mac address ritornera' un allarme (?)

argomenti:

`-w` int  `-c` int sono le soglie di warning e critical.

if warning exit 1, if critical exit 2, ok exit 0

eventualmente stampare i mac address "intrusi"

Potrebbe eservire estrarre l'ip presente dopo `ipNetToMediaPhysAddress.` (dovrebbero essere solo ipv4)

# args

-w warning threshold

-c critical threshold

-h ip I guess

-C community snmp

-D db name

-Q Query

# Stdout

Formato output:
"{nome_location_id} {inBandwidth} {outBandwidth} {} | 'inBandwidth'={inBandwidth}B;{warn};{critical};{min};{max}, 'outBandwidth'={outBandwidth}B"

# Esempio di dati:

```jsx
snmpwalk -v2c -c infra-mrtg 194.244.187.251 IP-MIB::ipNetToMediaPhysAddress
IP-MIB::ipNetToMediaPhysAddress.0.194.244.186.2 = STRING: 7c:e2:ca:f5:5a:a5
IP-MIB::ipNetToMediaPhysAddress.0.194.244.186.3 = STRING: 7c:e2:ca:f5:ed:eb
IP-MIB::ipNetToMediaPhysAddress.1.192.168.52.4 = STRING: 0:0:5e:0:1:14
IP-MIB::ipNetToMediaPhysAddress.1.192.168.52.6 = STRING: e4:c2:d1:e3:df:8f
IP-MIB::ipNetToMediaPhysAddress.2.192.168.54.3 = STRING: 0:18:71:76:a6:c8
IP-MIB::ipNetToMediaPhysAddress.2.192.168.54.5 = STRING: 0:d:65:d6:5a:c0
IP-MIB::ipNetToMediaPhysAddress.2.192.168.54.10 = STRING: c8:cb:b8:cc:ec:de
IP-MIB::ipNetToMediaPhysAddress.2.192.168.54.11 = STRING: ac:16:2d:7a:2d:94
IP-MIB::ipNetToMediaPhysAddress.2.192.168.54.20 = STRING: 0:19:99:a8:5c:a8
IP-MIB::ipNetToMediaPhysAddress.2.192.168.54.51 = STRING: 0:16:35:7f:5e:e4
IP-MIB::ipNetToMediaPhysAddress.2.192.168.54.52 = STRING: 0:c:29:8:11:1
IP-MIB::ipNetToMediaPhysAddress.2.192.168.54.53 = STRING: 0:c:29:8:11:1
IP-MIB::ipNetToMediaPhysAddress.2.192.168.54.58 = STRING: 0:c:29:8:11:1
IP-MIB::ipNetToMediaPhysAddress.2.192.168.54.60 = STRING: 0:c:29:c7:13:6b
IP-MIB::ipNetToMediaPhysAddress.2.192.168.54.69 = STRING: 0:17:a4:f6:fc:32
IP-MIB::ipNetToMediaPhysAddress.2.192.168.54.73 = STRING: 0:17:8:5c:69:ef
IP-MIB::ipNetToMediaPhysAddress.2.192.168.54.77 = STRING: 0:16:35:7f:19:e5
IP-MIB::ipNetToMediaPhysAddress.2.192.168.54.90 = STRING: 0:c:29:8:11:1
IP-MIB::ipNetToMediaPhysAddress.2.192.168.54.99 = STRING: 0:17:8:54:54:c4
IP-MIB::ipNetToMediaPhysAddress.2.192.168.54.101 = STRING: 0:c:29:81:ab:fe
IP-MIB::ipNetToMediaPhysAddress.2.192.168.54.104 = STRING: 0:c:29:5c:99:d2
IP-MIB::ipNetToMediaPhysAddress.2.192.168.54.109 = STRING: 0:1c:c4:c3:20:b8
IP-MIB::ipNetToMediaPhysAddress.2.192.168.54.113 = STRING: 0:16:76:73:ff:8b
IP-MIB::ipNetToMediaPhysAddress.2.192.168.54.114 = STRING: 0:1f:29:d0:6c:dd
IP-MIB::ipNetToMediaPhysAddress.2.192.168.54.117 = STRING: 0:9c:2:a4:1f:a0
IP-MIB::ipNetToMediaPhysAddress.2.192.168.54.120 = STRING: 0:1f:29:d0:6c:dd
IP-MIB::ipNetToMediaPhysAddress.2.192.168.54.124 = STRING: 0:c:29:60:e9:ab
IP-MIB::ipNetToMediaPhysAddress.2.192.168.54.125 = STRING: 0:c:29:60:e9:ab
IP-MIB::ipNetToMediaPhysAddress.2.192.168.54.132 = STRING: b4:b5:2f:51:30:a0
IP-MIB::ipNetToMediaPhysAddress.2.192.168.54.135 = STRING: 0:1:2:1b:11:b6
IP-MIB::ipNetToMediaPhysAddress.2.192.168.54.141 = STRING: 0:1c:c4:e2:cd:fc
IP-MIB::ipNetToMediaPhysAddress.2.192.168.54.143 = STRING: 0:17:8:54:54:c4
IP-MIB::ipNetToMediaPhysAddress.2.192.168.54.170 = STRING: b4:b5:2f:65:14:48
IP-MIB::ipNetToMediaPhysAddress.2.192.168.54.171 = STRING: b4:b5:2f:65:14:4a
IP-MIB::ipNetToMediaPhysAddress.2.192.168.54.172 = STRING: b4:b5:2f:65:c4:f4
IP-MIB::ipNetToMediaPhysAddress.3.194.244.187.1 = STRING: 0:0:c:7:ac:d4
IP-MIB::ipNetToMediaPhysAddress.3.194.244.187.2 = STRING: 0:12:7f:cd:ae:0
```

# UPDATES
ARP Table OID:
1. ipNetToMediaIfIndex:1.3.6.1.2.1.4.22.1.1
2. ipNetToMediaPhysAddress:1.3.6.1.2.1.4.22.1.2
3. ipNetToMediaNetAddress:1.3.6.1.2.1.4.22.1.3
4. ipNetToMediaType:1.3.6.1.2.1.4.22.1.4



# Lista Interfacce su cui è collegato un IP ADDRESS - L'interfaccia è espressa mediante INDEX (Integer). Successivamente la convertiamo in Descrizione Human Readable

[root@network01 ~]# snmpwalk -v2c -c ipngy2k 192.168.1.27 IP-MIB::ipNetToMediaIfIndex
IP-MIB::ipNetToMediaIfIndex.22.192.168.1.27 = INTEGER: 22
IP-MIB::ipNetToMediaIfIndex.28.212.90.1.2 = INTEGER: 28
IP-MIB::ipNetToMediaIfIndex.29.212.90.1.65 = INTEGER: 29
IP-MIB::ipNetToMediaIfIndex.29.212.90.1.67 = INTEGER: 29
IP-MIB::ipNetToMediaIfIndex.29.212.90.1.68 = INTEGER: 29
IP-MIB::ipNetToMediaIfIndex.29.212.90.1.69 = INTEGER: 29
IP-MIB::ipNetToMediaIfIndex.29.212.90.1.70 = INTEGER: 29
IP-MIB::ipNetToMediaIfIndex.29.212.90.1.71 = INTEGER: 29
IP-MIB::ipNetToMediaIfIndex.29.212.90.1.72 = INTEGER: 29
IP-MIB::ipNetToMediaIfIndex.29.212.90.1.76 = INTEGER: 29
IP-MIB::ipNetToMediaIfIndex.29.212.90.1.77 = INTEGER: 29
IP-MIB::ipNetToMediaIfIndex.29.212.90.1.78 = INTEGER: 29
IP-MIB::ipNetToMediaIfIndex.29.212.90.1.79 = INTEGER: 29
IP-MIB::ipNetToMediaIfIndex.29.212.90.1.80 = INTEGER: 29
IP-MIB::ipNetToMediaIfIndex.29.212.90.1.81 = INTEGER: 29
IP-MIB::ipNetToMediaIfIndex.29.212.90.1.82 = INTEGER: 29
IP-MIB::ipNetToMediaIfIndex.29.212.90.1.83 = INTEGER: 29
IP-MIB::ipNetToMediaIfIndex.29.212.90.1.84 = INTEGER: 29
IP-MIB::ipNetToMediaIfIndex.29.212.90.1.85 = INTEGER: 29
IP-MIB::ipNetToMediaIfIndex.30.212.90.1.34 = INTEGER: 30
IP-MIB::ipNetToMediaIfIndex.31.212.90.1.97 = INTEGER: 31
IP-MIB::ipNetToMediaIfIndex.31.212.90.1.99 = INTEGER: 31
IP-MIB::ipNetToMediaIfIndex.31.212.90.1.100 = INTEGER: 31
IP-MIB::ipNetToMediaIfIndex.31.212.90.1.101 = INTEGER: 31
IP-MIB::ipNetToMediaIfIndex.31.212.90.1.102 = INTEGER: 31
IP-MIB::ipNetToMediaIfIndex.31.212.90.1.103 = INTEGER: 31
IP-MIB::ipNetToMediaIfIndex.31.212.90.1.104 = INTEGER: 31
IP-MIB::ipNetToMediaIfIndex.31.212.90.1.108 = INTEGER: 31
IP-MIB::ipNetToMediaIfIndex.31.212.90.1.109 = INTEGER: 31
IP-MIB::ipNetToMediaIfIndex.31.212.90.1.110 = INTEGER: 31
IP-MIB::ipNetToMediaIfIndex.31.212.90.1.111 = INTEGER: 31
IP-MIB::ipNetToMediaIfIndex.31.212.90.1.112 = INTEGER: 31
IP-MIB::ipNetToMediaIfIndex.31.212.90.1.113 = INTEGER: 31
IP-MIB::ipNetToMediaIfIndex.31.212.90.1.114 = INTEGER: 31
IP-MIB::ipNetToMediaIfIndex.31.212.90.1.115 = INTEGER: 31
IP-MIB::ipNetToMediaIfIndex.31.212.90.1.116 = INTEGER: 31
IP-MIB::ipNetToMediaIfIndex.31.212.90.1.117 = INTEGER: 31
IP-MIB::ipNetToMediaIfIndex.932.62.94.30.245 = INTEGER: 932
IP-MIB::ipNetToMediaIfIndex.932.62.94.30.246 = INTEGER: 932
IP-MIB::ipNetToMediaIfIndex.933.62.94.5.25 = INTEGER: 933
IP-MIB::ipNetToMediaIfIndex.933.62.94.5.26 = INTEGER: 933
IP-MIB::ipNetToMediaIfIndex.934.62.94.5.61 = INTEGER: 934
IP-MIB::ipNetToMediaIfIndex.934.62.94.5.62 = INTEGER: 934
IP-MIB::ipNetToMediaIfIndex.1559.62.94.46.89 = INTEGER: 1559
IP-MIB::ipNetToMediaIfIndex.1559.62.94.46.90 = INTEGER: 1559
IP-MIB::ipNetToMediaIfIndex.1560.172.28.125.113 = INTEGER: 1560
IP-MIB::ipNetToMediaIfIndex.1560.172.28.125.114 = INTEGER: 1560
IP-MIB::ipNetToMediaIfIndex.1929.62.94.45.165 = INTEGER: 1929
IP-MIB::ipNetToMediaIfIndex.1929.62.94.45.166 = INTEGER: 1929
IP-MIB::ipNetToMediaIfIndex.1930.172.28.8.245 = INTEGER: 1930
IP-MIB::ipNetToMediaIfIndex.1930.172.28.8.246 = INTEGER: 1930
IP-MIB::ipNetToMediaIfIndex.1931.172.28.8.221 = INTEGER: 1931
IP-MIB::ipNetToMediaIfIndex.1931.172.28.8.222 = INTEGER: 1931
IP-MIB::ipNetToMediaIfIndex.3829.172.28.54.137 = INTEGER: 3829
IP-MIB::ipNetToMediaIfIndex.3829.172.28.54.138 = INTEGER: 3829
IP-MIB::ipNetToMediaIfIndex.3830.62.94.25.21 = INTEGER: 3830
IP-MIB::ipNetToMediaIfIndex.3830.62.94.25.22 = INTEGER: 3830
IP-MIB::ipNetToMediaIfIndex.3905.62.94.30.225 = INTEGER: 3905
IP-MIB::ipNetToMediaIfIndex.3905.62.94.30.226 = INTEGER: 3905
IP-MIB::ipNetToMediaIfIndex.4527.62.94.129.249 = INTEGER: 4527
IP-MIB::ipNetToMediaIfIndex.4538.62.94.30.37 = INTEGER: 4538
IP-MIB::ipNetToMediaIfIndex.4538.62.94.30.38 = INTEGER: 4538
IP-MIB::ipNetToMediaIfIndex.4540.62.94.46.145 = INTEGER: 4540
IP-MIB::ipNetToMediaIfIndex.4543.62.94.46.97 = INTEGER: 4543
IP-MIB::ipNetToMediaIfIndex.4543.62.94.46.98 = INTEGER: 4543
IP-MIB::ipNetToMediaIfIndex.4544.62.94.5.93 = INTEGER: 4544
IP-MIB::ipNetToMediaIfIndex.4544.62.94.5.94 = INTEGER: 4544
IP-MIB::ipNetToMediaIfIndex.4545.62.94.209.45 = INTEGER: 4545
IP-MIB::ipNetToMediaIfIndex.4545.62.94.209.46 = INTEGER: 4545
IP-MIB::ipNetToMediaIfIndex.4546.62.94.209.101 = INTEGER: 4546
IP-MIB::ipNetToMediaIfIndex.4546.62.94.209.102 = INTEGER: 4546
IP-MIB::ipNetToMediaIfIndex.4547.172.28.123.253 = INTEGER: 4547
IP-MIB::ipNetToMediaIfIndex.4547.172.28.123.254 = INTEGER: 4547
IP-MIB::ipNetToMediaIfIndex.4548.62.94.209.237 = INTEGER: 4548
IP-MIB::ipNetToMediaIfIndex.4548.62.94.209.238 = INTEGER: 4548
IP-MIB::ipNetToMediaIfIndex.4550.62.94.209.245 = INTEGER: 4550
IP-MIB::ipNetToMediaIfIndex.4550.62.94.209.246 = INTEGER: 4550
IP-MIB::ipNetToMediaIfIndex.4551.62.94.209.133 = INTEGER: 4551
IP-MIB::ipNetToMediaIfIndex.4557.62.94.25.193 = INTEGER: 4557
IP-MIB::ipNetToMediaIfIndex.4558.62.94.30.141 = INTEGER: 4558
IP-MIB::ipNetToMediaIfIndex.4558.62.94.30.142 = INTEGER: 4558
IP-MIB::ipNetToMediaIfIndex.4559.62.94.31.17 = INTEGER: 4559
IP-MIB::ipNetToMediaIfIndex.4559.62.94.31.18 = INTEGER: 4559
IP-MIB::ipNetToMediaIfIndex.4560.62.94.25.197 = INTEGER: 4560
IP-MIB::ipNetToMediaIfIndex.4560.62.94.25.198 = INTEGER: 4560
IP-MIB::ipNetToMediaIfIndex.4561.62.94.30.21 = INTEGER: 4561
IP-MIB::ipNetToMediaIfIndex.4561.62.94.30.22 = INTEGER: 4561
IP-MIB::ipNetToMediaIfIndex.4564.62.94.45.25 = INTEGER: 4564
IP-MIB::ipNetToMediaIfIndex.4564.62.94.45.26 = INTEGER: 4564
IP-MIB::ipNetToMediaIfIndex.4565.172.28.26.229 = INTEGER: 4565
IP-MIB::ipNetToMediaIfIndex.4565.172.28.26.230 = INTEGER: 4565
IP-MIB::ipNetToMediaIfIndex.4566.172.28.8.241 = INTEGER: 4566
IP-MIB::ipNetToMediaIfIndex.4566.172.28.8.242 = INTEGER: 4566
IP-MIB::ipNetToMediaIfIndex.4567.172.28.8.217 = INTEGER: 4567
IP-MIB::ipNetToMediaIfIndex.4567.172.28.8.218 = INTEGER: 4567
IP-MIB::ipNetToMediaIfIndex.4568.172.28.8.237 = INTEGER: 4568
IP-MIB::ipNetToMediaIfIndex.4568.172.28.8.238 = INTEGER: 4568
IP-MIB::ipNetToMediaIfIndex.4569.172.28.8.213 = INTEGER: 4569
IP-MIB::ipNetToMediaIfIndex.4569.172.28.8.214 = INTEGER: 4569
IP-MIB::ipNetToMediaIfIndex.4696.172.28.65.73 = INTEGER: 4696
IP-MIB::ipNetToMediaIfIndex.4696.172.28.65.74 = INTEGER: 4696
IP-MIB::ipNetToMediaIfIndex.4697.172.28.64.73 = INTEGER: 4697
IP-MIB::ipNetToMediaIfIndex.4697.172.28.64.74 = INTEGER: 4697
IP-MIB::ipNetToMediaIfIndex.4698.172.28.63.73 = INTEGER: 4698
IP-MIB::ipNetToMediaIfIndex.4698.172.28.63.74 = INTEGER: 4698
IP-MIB::ipNetToMediaIfIndex.4699.172.28.62.73 = INTEGER: 4699
IP-MIB::ipNetToMediaIfIndex.4699.172.28.62.74 = INTEGER: 4699
IP-MIB::ipNetToMediaIfIndex.4700.62.94.25.217 = INTEGER: 4700
IP-MIB::ipNetToMediaIfIndex.4700.62.94.25.218 = INTEGER: 4700
IP-MIB::ipNetToMediaIfIndex.4701.172.28.102.165 = INTEGER: 4701
IP-MIB::ipNetToMediaIfIndex.4701.172.28.102.166 = INTEGER: 4701
IP-MIB::ipNetToMediaIfIndex.4908.62.94.30.133 = INTEGER: 4908
IP-MIB::ipNetToMediaIfIndex.4909.62.94.113.117 = INTEGER: 4909
IP-MIB::ipNetToMediaIfIndex.4909.62.94.113.118 = INTEGER: 4909
IP-MIB::ipNetToMediaIfIndex.4910.62.94.31.145 = INTEGER: 4910
IP-MIB::ipNetToMediaIfIndex.4910.62.94.31.146 = INTEGER: 4910
IP-MIB::ipNetToMediaIfIndex.4913.62.94.31.253 = INTEGER: 4913
IP-MIB::ipNetToMediaIfIndex.4913.62.94.31.254 = INTEGER: 4913
IP-MIB::ipNetToMediaIfIndex.4914.172.28.15.101 = INTEGER: 4914
IP-MIB::ipNetToMediaIfIndex.4914.172.28.15.102 = INTEGER: 4914
IP-MIB::ipNetToMediaIfIndex.5014.172.28.112.137 = INTEGER: 5014 *
IP-MIB::ipNetToMediaIfIndex.5014.172.28.112.138 = INTEGER: 5014 *

###############################################################
# Trasformazione da IfIndex a IfDescr (esempio su interfaccia 5014

[root@network01 ~]# snmpbulkwalk -v2c -c ipngy2k 192.168.1.27 IF-MIB::ifDescr.5014
IF-MIB::ifDescr.5014 = STRING: TenGigabitEthernet0/1/2.13140002

###############################################################
# Cerco i mac address per ciascun IP trovato

[root@network01 ~]# snmpwalk -v2c -c ipngy2k 192.168.1.27 IP-MIB::ipNetToMediaPhysAddress
IP-MIB::ipNetToMediaPhysAddress.22.192.168.1.27 = STRING: 70:f:6a:9a:91:80
IP-MIB::ipNetToMediaPhysAddress.28.212.90.1.2 = STRING: 70:f:6a:9a:91:a0
IP-MIB::ipNetToMediaPhysAddress.29.212.90.1.65 = STRING: 70:f:6a:9a:2a:20
IP-MIB::ipNetToMediaPhysAddress.29.212.90.1.67 = STRING: 70:f:6a:9a:91:a0
IP-MIB::ipNetToMediaPhysAddress.29.212.90.1.68 = STRING: 30:f7:d:ee:a8:10
IP-MIB::ipNetToMediaPhysAddress.29.212.90.1.69 = STRING: b0:26:80:5b:7f:b0
IP-MIB::ipNetToMediaPhysAddress.29.212.90.1.70 = STRING: b0:26:80:5b:7f:ba
IP-MIB::ipNetToMediaPhysAddress.29.212.90.1.71 = STRING: b0:26:80:54:b9:34
IP-MIB::ipNetToMediaPhysAddress.29.212.90.1.72 = STRING: 70:e4:22:6c:1e:fc
IP-MIB::ipNetToMediaPhysAddress.29.212.90.1.76 = STRING: 0:2:7d:1c:c:1b
IP-MIB::ipNetToMediaPhysAddress.29.212.90.1.77 = STRING: 0:b:60:8:60:1b
IP-MIB::ipNetToMediaPhysAddress.29.212.90.1.78 = STRING: 30:f7:d:3c:9f:82
IP-MIB::ipNetToMediaPhysAddress.29.212.90.1.79 = STRING: ec:bd:1d:9e:90:bf
IP-MIB::ipNetToMediaPhysAddress.29.212.90.1.80 = STRING: 70:e4:22:eb:9:bf
IP-MIB::ipNetToMediaPhysAddress.29.212.90.1.81 = STRING: 0:ea:bd:5d:9a:3f
IP-MIB::ipNetToMediaPhysAddress.29.212.90.1.82 = STRING: 0:ea:bd:9:72:3f
IP-MIB::ipNetToMediaPhysAddress.29.212.90.1.83 = STRING: 0:ea:bd:2f:a4:bf
IP-MIB::ipNetToMediaPhysAddress.29.212.90.1.84 = STRING: 0:ea:bd:5d:a5:bf
IP-MIB::ipNetToMediaPhysAddress.29.212.90.1.85 = STRING: 6c:8b:d3:80:f:3f
IP-MIB::ipNetToMediaPhysAddress.30.212.90.1.34 = STRING: 70:f:6a:9a:91:a1
IP-MIB::ipNetToMediaPhysAddress.31.212.90.1.97 = STRING: 70:f:6a:9a:2a:21
IP-MIB::ipNetToMediaPhysAddress.31.212.90.1.99 = STRING: 70:f:6a:9a:91:a1
IP-MIB::ipNetToMediaPhysAddress.31.212.90.1.100 = STRING: 30:f7:d:ee:a8:20
IP-MIB::ipNetToMediaPhysAddress.31.212.90.1.101 = STRING: b0:26:80:37:7a:b6
IP-MIB::ipNetToMediaPhysAddress.31.212.90.1.102 = STRING: b0:26:80:5b:7f:b9
IP-MIB::ipNetToMediaPhysAddress.31.212.90.1.103 = STRING: b0:26:80:52:12:56
IP-MIB::ipNetToMediaPhysAddress.31.212.90.1.104 = STRING: 70:e4:22:6c:1e:fd
IP-MIB::ipNetToMediaPhysAddress.31.212.90.1.108 = STRING: 0:2:7d:1c:c:1a
IP-MIB::ipNetToMediaPhysAddress.31.212.90.1.109 = STRING: 0:b:60:8:60:1a
IP-MIB::ipNetToMediaPhysAddress.31.212.90.1.110 = STRING: 30:f7:d:3c:9f:83
IP-MIB::ipNetToMediaPhysAddress.31.212.90.1.111 = STRING: ec:bd:1d:9e:90:bf
IP-MIB::ipNetToMediaPhysAddress.31.212.90.1.112 = STRING: 70:e4:22:eb:9:bf
IP-MIB::ipNetToMediaPhysAddress.31.212.90.1.113 = STRING: 0:ea:bd:5d:9a:3f
IP-MIB::ipNetToMediaPhysAddress.31.212.90.1.114 = STRING: 0:ea:bd:9:72:3f
IP-MIB::ipNetToMediaPhysAddress.31.212.90.1.115 = STRING: 0:ea:bd:2f:a4:bf
IP-MIB::ipNetToMediaPhysAddress.31.212.90.1.116 = STRING: 0:ea:bd:5d:a5:bf
IP-MIB::ipNetToMediaPhysAddress.31.212.90.1.117 = STRING: 6c:8b:d3:80:f:3f
IP-MIB::ipNetToMediaPhysAddress.932.62.94.30.245 = STRING: 70:f:6a:9a:91:93
IP-MIB::ipNetToMediaPhysAddress.932.62.94.30.246 = STRING: 38:10:d5:4d:da:0
IP-MIB::ipNetToMediaPhysAddress.933.62.94.5.25 = STRING: 70:f:6a:9a:91:93
IP-MIB::ipNetToMediaPhysAddress.933.62.94.5.26 = STRING: 30:37:a6:cf:f9:c0
IP-MIB::ipNetToMediaPhysAddress.934.62.94.5.61 = STRING: 70:f:6a:9a:91:93
IP-MIB::ipNetToMediaPhysAddress.934.62.94.5.62 = STRING: bc:5:43:b6:3:90
IP-MIB::ipNetToMediaPhysAddress.1559.62.94.46.89 = STRING: 70:f:6a:9a:91:93
IP-MIB::ipNetToMediaPhysAddress.1559.62.94.46.90 = STRING: 0:fd:22:48:47:34
IP-MIB::ipNetToMediaPhysAddress.1560.172.28.125.113 = STRING: 70:f:6a:9a:91:93
IP-MIB::ipNetToMediaPhysAddress.1560.172.28.125.114 = STRING: 0:fd:22:48:47:34
IP-MIB::ipNetToMediaPhysAddress.1929.62.94.45.165 = STRING: 70:f:6a:9a:91:93
IP-MIB::ipNetToMediaPhysAddress.1929.62.94.45.166 = STRING: 68:ca:e4:8e:d4:6d
IP-MIB::ipNetToMediaPhysAddress.1930.172.28.8.245 = STRING: 70:f:6a:9a:91:93
IP-MIB::ipNetToMediaPhysAddress.1930.172.28.8.246 = STRING: ac:f2:c5:b0:bc:20
IP-MIB::ipNetToMediaPhysAddress.1931.172.28.8.221 = STRING: 70:f:6a:9a:91:93
IP-MIB::ipNetToMediaPhysAddress.1931.172.28.8.222 = STRING: ac:f2:c5:b0:bc:20
IP-MIB::ipNetToMediaPhysAddress.3829.172.28.54.137 = STRING: 70:f:6a:9a:91:91
IP-MIB::ipNetToMediaPhysAddress.3829.172.28.54.138 = STRING: 2c:f8:9b:64:1a:10
IP-MIB::ipNetToMediaPhysAddress.3830.62.94.25.21 = STRING: 70:f:6a:9a:91:91
IP-MIB::ipNetToMediaPhysAddress.3830.62.94.25.22 = STRING: 2c:f8:9b:64:1a:10
IP-MIB::ipNetToMediaPhysAddress.3905.62.94.30.225 = STRING: 70:f:6a:9a:91:92
IP-MIB::ipNetToMediaPhysAddress.3905.62.94.30.226 = STRING: f0:f7:55:2f:a3:a8
IP-MIB::ipNetToMediaPhysAddress.4527.62.94.129.249 = STRING: 70:f:6a:9a:91:91
IP-MIB::ipNetToMediaPhysAddress.4538.62.94.30.37 = STRING: 70:f:6a:9a:91:92
IP-MIB::ipNetToMediaPhysAddress.4538.62.94.30.38 = STRING: 0:1b:d5:8f:56:10
IP-MIB::ipNetToMediaPhysAddress.4540.62.94.46.145 = STRING: 70:f:6a:9a:91:92
IP-MIB::ipNetToMediaPhysAddress.4543.62.94.46.97 = STRING: 70:f:6a:9a:91:91
IP-MIB::ipNetToMediaPhysAddress.4543.62.94.46.98 = STRING: e4:c7:22:a8:41:6c
IP-MIB::ipNetToMediaPhysAddress.4544.62.94.5.93 = STRING: 70:f:6a:9a:91:91
IP-MIB::ipNetToMediaPhysAddress.4544.62.94.5.94 = STRING: 0:1d:aa:d6:17:89
IP-MIB::ipNetToMediaPhysAddress.4545.62.94.209.45 = STRING: 70:f:6a:9a:91:91
IP-MIB::ipNetToMediaPhysAddress.4545.62.94.209.46 = STRING: 4c:0:82:54:fa:28
IP-MIB::ipNetToMediaPhysAddress.4546.62.94.209.101 = STRING: 70:f:6a:9a:91:91
IP-MIB::ipNetToMediaPhysAddress.4546.62.94.209.102 = STRING: 4c:0:82:54:fa:28
IP-MIB::ipNetToMediaPhysAddress.4547.172.28.123.253 = STRING: 70:f:6a:9a:91:91
IP-MIB::ipNetToMediaPhysAddress.4547.172.28.123.254 = STRING: 4c:0:82:54:fa:28
IP-MIB::ipNetToMediaPhysAddress.4548.62.94.209.237 = STRING: 70:f:6a:9a:91:91
IP-MIB::ipNetToMediaPhysAddress.4548.62.94.209.238 = STRING: 9c:af:ca:71:a6:bf
IP-MIB::ipNetToMediaPhysAddress.4550.62.94.209.245 = STRING: 70:f:6a:9a:91:91
IP-MIB::ipNetToMediaPhysAddress.4550.62.94.209.246 = STRING: 28:93:fe:6c:18:93
IP-MIB::ipNetToMediaPhysAddress.4551.62.94.209.133 = STRING: 70:f:6a:9a:91:91
IP-MIB::ipNetToMediaPhysAddress.4557.62.94.25.193 = STRING: 70:f:6a:9a:91:91
IP-MIB::ipNetToMediaPhysAddress.4558.62.94.30.141 = STRING: 70:f:6a:9a:91:91
IP-MIB::ipNetToMediaPhysAddress.4558.62.94.30.142 = STRING: 2c:5a:f:2d:12:71
IP-MIB::ipNetToMediaPhysAddress.4559.62.94.31.17 = STRING: 70:f:6a:9a:91:91
IP-MIB::ipNetToMediaPhysAddress.4559.62.94.31.18 = STRING: 0:21:d8:7c:99:2c
IP-MIB::ipNetToMediaPhysAddress.4560.62.94.25.197 = STRING: 70:f:6a:9a:91:91
IP-MIB::ipNetToMediaPhysAddress.4560.62.94.25.198 = STRING: ac:f2:c5:66:ed:40
IP-MIB::ipNetToMediaPhysAddress.4561.62.94.30.21 = STRING: 70:f:6a:9a:91:91
IP-MIB::ipNetToMediaPhysAddress.4561.62.94.30.22 = STRING: 0:1d:aa:ed:c:32
IP-MIB::ipNetToMediaPhysAddress.4564.62.94.45.25 = STRING: 70:f:6a:9a:91:91
IP-MIB::ipNetToMediaPhysAddress.4564.62.94.45.26 = STRING: 0:22:55:c1:59:ac
IP-MIB::ipNetToMediaPhysAddress.4565.172.28.26.229 = STRING: 70:f:6a:9a:91:91
IP-MIB::ipNetToMediaPhysAddress.4565.172.28.26.230 = STRING: 0:22:55:c1:59:ac
IP-MIB::ipNetToMediaPhysAddress.4566.172.28.8.241 = STRING: 70:f:6a:9a:91:91
IP-MIB::ipNetToMediaPhysAddress.4566.172.28.8.242 = STRING: 70:81:5:9d:e9:60
IP-MIB::ipNetToMediaPhysAddress.4567.172.28.8.217 = STRING: 70:f:6a:9a:91:91
IP-MIB::ipNetToMediaPhysAddress.4567.172.28.8.218 = STRING: 70:81:5:9d:e9:60
IP-MIB::ipNetToMediaPhysAddress.4568.172.28.8.237 = STRING: 70:f:6a:9a:91:91
IP-MIB::ipNetToMediaPhysAddress.4568.172.28.8.238 = STRING: 50:57:a8:ff:f5:0
IP-MIB::ipNetToMediaPhysAddress.4569.172.28.8.213 = STRING: 70:f:6a:9a:91:91
IP-MIB::ipNetToMediaPhysAddress.4569.172.28.8.214 = STRING: 50:57:a8:ff:f5:0
IP-MIB::ipNetToMediaPhysAddress.4696.172.28.65.73 = STRING: 70:f:6a:9a:91:92
IP-MIB::ipNetToMediaPhysAddress.4696.172.28.65.74 = STRING: 64:0:f1:fa:71:80
IP-MIB::ipNetToMediaPhysAddress.4697.172.28.64.73 = STRING: 70:f:6a:9a:91:92
IP-MIB::ipNetToMediaPhysAddress.4697.172.28.64.74 = STRING: 64:0:f1:fa:71:80
IP-MIB::ipNetToMediaPhysAddress.4698.172.28.63.73 = STRING: 70:f:6a:9a:91:92
IP-MIB::ipNetToMediaPhysAddress.4698.172.28.63.74 = STRING: 64:0:f1:fa:71:81
IP-MIB::ipNetToMediaPhysAddress.4699.172.28.62.73 = STRING: 70:f:6a:9a:91:92
IP-MIB::ipNetToMediaPhysAddress.4699.172.28.62.74 = STRING: 64:0:f1:fa:71:81
IP-MIB::ipNetToMediaPhysAddress.4700.62.94.25.217 = STRING: 70:f:6a:9a:91:92
IP-MIB::ipNetToMediaPhysAddress.4700.62.94.25.218 = STRING: 0:fd:22:af:a8:0
IP-MIB::ipNetToMediaPhysAddress.4701.172.28.102.165 = STRING: 70:f:6a:9a:91:92
IP-MIB::ipNetToMediaPhysAddress.4701.172.28.102.166 = STRING: 0:fd:22:af:a8:0
IP-MIB::ipNetToMediaPhysAddress.4908.62.94.30.133 = STRING: 70:f:6a:9a:91:92
IP-MIB::ipNetToMediaPhysAddress.4909.62.94.113.117 = STRING: 70:f:6a:9a:91:92
IP-MIB::ipNetToMediaPhysAddress.4909.62.94.113.118 = STRING: 0:a:b8:39:c9:22
IP-MIB::ipNetToMediaPhysAddress.4910.62.94.31.145 = STRING: 70:f:6a:9a:91:92
IP-MIB::ipNetToMediaPhysAddress.4910.62.94.31.146 = STRING: 1c:df:f:29:25:58
IP-MIB::ipNetToMediaPhysAddress.4913.62.94.31.253 = STRING: 70:f:6a:9a:91:92
IP-MIB::ipNetToMediaPhysAddress.4913.62.94.31.254 = STRING: 0:15:2b:97:b2:31
IP-MIB::ipNetToMediaPhysAddress.4914.172.28.15.101 = STRING: 70:f:6a:9a:91:92
IP-MIB::ipNetToMediaPhysAddress.4914.172.28.15.102 = STRING: 0:15:2b:97:b2:31
IP-MIB::ipNetToMediaPhysAddress.5014.172.28.112.137 = STRING: 70:f:6a:9a:91:92
IP-MIB::ipNetToMediaPhysAddress.5014.172.28.112.138 = STRING: 0:1a:6c:6d:c5:ec

#############################################################################
# Mediante questa chiamata mi posso estrarmi Ip Address come ultimo campo (Se serve, almeno mi evito il parsing o le regex)

[root@network01 ~]# snmpwalk -v2c -c ipngy2k 192.168.1.27 IP-MIB::ipNetToMediaNetAddress
IP-MIB::ipNetToMediaNetAddress.22.192.168.1.27 = IpAddress: 192.168.1.27
IP-MIB::ipNetToMediaNetAddress.28.212.90.1.2 = IpAddress: 212.90.1.2
IP-MIB::ipNetToMediaNetAddress.29.212.90.1.65 = IpAddress: 212.90.1.65
IP-MIB::ipNetToMediaNetAddress.29.212.90.1.67 = IpAddress: 212.90.1.67
IP-MIB::ipNetToMediaNetAddress.29.212.90.1.68 = IpAddress: 212.90.1.68
IP-MIB::ipNetToMediaNetAddress.29.212.90.1.69 = IpAddress: 212.90.1.69
IP-MIB::ipNetToMediaNetAddress.29.212.90.1.70 = IpAddress: 212.90.1.70
IP-MIB::ipNetToMediaNetAddress.29.212.90.1.71 = IpAddress: 212.90.1.71
IP-MIB::ipNetToMediaNetAddress.29.212.90.1.72 = IpAddress: 212.90.1.72
IP-MIB::ipNetToMediaNetAddress.29.212.90.1.76 = IpAddress: 212.90.1.76
IP-MIB::ipNetToMediaNetAddress.29.212.90.1.77 = IpAddress: 212.90.1.77
IP-MIB::ipNetToMediaNetAddress.29.212.90.1.78 = IpAddress: 212.90.1.78
IP-MIB::ipNetToMediaNetAddress.29.212.90.1.79 = IpAddress: 212.90.1.79
IP-MIB::ipNetToMediaNetAddress.29.212.90.1.80 = IpAddress: 212.90.1.80
IP-MIB::ipNetToMediaNetAddress.29.212.90.1.81 = IpAddress: 212.90.1.81
IP-MIB::ipNetToMediaNetAddress.29.212.90.1.82 = IpAddress: 212.90.1.82
IP-MIB::ipNetToMediaNetAddress.29.212.90.1.83 = IpAddress: 212.90.1.83
IP-MIB::ipNetToMediaNetAddress.29.212.90.1.84 = IpAddress: 212.90.1.84
IP-MIB::ipNetToMediaNetAddress.29.212.90.1.85 = IpAddress: 212.90.1.85
IP-MIB::ipNetToMediaNetAddress.30.212.90.1.34 = IpAddress: 212.90.1.34
IP-MIB::ipNetToMediaNetAddress.31.212.90.1.97 = IpAddress: 212.90.1.97
IP-MIB::ipNetToMediaNetAddress.31.212.90.1.99 = IpAddress: 212.90.1.99
IP-MIB::ipNetToMediaNetAddress.31.212.90.1.100 = IpAddress: 212.90.1.100
IP-MIB::ipNetToMediaNetAddress.31.212.90.1.101 = IpAddress: 212.90.1.101
IP-MIB::ipNetToMediaNetAddress.31.212.90.1.102 = IpAddress: 212.90.1.102
IP-MIB::ipNetToMediaNetAddress.31.212.90.1.103 = IpAddress: 212.90.1.103
IP-MIB::ipNetToMediaNetAddress.31.212.90.1.104 = IpAddress: 212.90.1.104
IP-MIB::ipNetToMediaNetAddress.31.212.90.1.108 = IpAddress: 212.90.1.108
IP-MIB::ipNetToMediaNetAddress.31.212.90.1.109 = IpAddress: 212.90.1.109
IP-MIB::ipNetToMediaNetAddress.31.212.90.1.110 = IpAddress: 212.90.1.110
IP-MIB::ipNetToMediaNetAddress.31.212.90.1.111 = IpAddress: 212.90.1.111
IP-MIB::ipNetToMediaNetAddress.31.212.90.1.112 = IpAddress: 212.90.1.112
IP-MIB::ipNetToMediaNetAddress.31.212.90.1.113 = IpAddress: 212.90.1.113
IP-MIB::ipNetToMediaNetAddress.31.212.90.1.114 = IpAddress: 212.90.1.114
IP-MIB::ipNetToMediaNetAddress.31.212.90.1.115 = IpAddress: 212.90.1.115
IP-MIB::ipNetToMediaNetAddress.31.212.90.1.116 = IpAddress: 212.90.1.116
IP-MIB::ipNetToMediaNetAddress.31.212.90.1.117 = IpAddress: 212.90.1.117
IP-MIB::ipNetToMediaNetAddress.932.62.94.30.245 = IpAddress: 62.94.30.245
IP-MIB::ipNetToMediaNetAddress.932.62.94.30.246 = IpAddress: 62.94.30.246
IP-MIB::ipNetToMediaNetAddress.933.62.94.5.25 = IpAddress: 62.94.5.25
IP-MIB::ipNetToMediaNetAddress.933.62.94.5.26 = IpAddress: 62.94.5.26
IP-MIB::ipNetToMediaNetAddress.934.62.94.5.61 = IpAddress: 62.94.5.61
IP-MIB::ipNetToMediaNetAddress.934.62.94.5.62 = IpAddress: 62.94.5.62
IP-MIB::ipNetToMediaNetAddress.1559.62.94.46.89 = IpAddress: 62.94.46.89
IP-MIB::ipNetToMediaNetAddress.1559.62.94.46.90 = IpAddress: 62.94.46.90
IP-MIB::ipNetToMediaNetAddress.1560.172.28.125.113 = IpAddress: 172.28.125.113
IP-MIB::ipNetToMediaNetAddress.1560.172.28.125.114 = IpAddress: 172.28.125.114
IP-MIB::ipNetToMediaNetAddress.1929.62.94.45.165 = IpAddress: 62.94.45.165
IP-MIB::ipNetToMediaNetAddress.1929.62.94.45.166 = IpAddress: 62.94.45.166
IP-MIB::ipNetToMediaNetAddress.1930.172.28.8.245 = IpAddress: 172.28.8.245
IP-MIB::ipNetToMediaNetAddress.1930.172.28.8.246 = IpAddress: 172.28.8.246
IP-MIB::ipNetToMediaNetAddress.1931.172.28.8.221 = IpAddress: 172.28.8.221
IP-MIB::ipNetToMediaNetAddress.1931.172.28.8.222 = IpAddress: 172.28.8.222
IP-MIB::ipNetToMediaNetAddress.3829.172.28.54.137 = IpAddress: 172.28.54.137
IP-MIB::ipNetToMediaNetAddress.3829.172.28.54.138 = IpAddress: 172.28.54.138
IP-MIB::ipNetToMediaNetAddress.3830.62.94.25.21 = IpAddress: 62.94.25.21
IP-MIB::ipNetToMediaNetAddress.3830.62.94.25.22 = IpAddress: 62.94.25.22
IP-MIB::ipNetToMediaNetAddress.3905.62.94.30.225 = IpAddress: 62.94.30.225
IP-MIB::ipNetToMediaNetAddress.3905.62.94.30.226 = IpAddress: 62.94.30.226
IP-MIB::ipNetToMediaNetAddress.4527.62.94.129.249 = IpAddress: 62.94.129.249
IP-MIB::ipNetToMediaNetAddress.4538.62.94.30.37 = IpAddress: 62.94.30.37
IP-MIB::ipNetToMediaNetAddress.4538.62.94.30.38 = IpAddress: 62.94.30.38
IP-MIB::ipNetToMediaNetAddress.4540.62.94.46.145 = IpAddress: 62.94.46.145
IP-MIB::ipNetToMediaNetAddress.4543.62.94.46.97 = IpAddress: 62.94.46.97
IP-MIB::ipNetToMediaNetAddress.4543.62.94.46.98 = IpAddress: 62.94.46.98
IP-MIB::ipNetToMediaNetAddress.4544.62.94.5.93 = IpAddress: 62.94.5.93
IP-MIB::ipNetToMediaNetAddress.4544.62.94.5.94 = IpAddress: 62.94.5.94
IP-MIB::ipNetToMediaNetAddress.4545.62.94.209.45 = IpAddress: 62.94.209.45
IP-MIB::ipNetToMediaNetAddress.4545.62.94.209.46 = IpAddress: 62.94.209.46
IP-MIB::ipNetToMediaNetAddress.4546.62.94.209.101 = IpAddress: 62.94.209.101
IP-MIB::ipNetToMediaNetAddress.4546.62.94.209.102 = IpAddress: 62.94.209.102
IP-MIB::ipNetToMediaNetAddress.4547.172.28.123.253 = IpAddress: 172.28.123.253
IP-MIB::ipNetToMediaNetAddress.4547.172.28.123.254 = IpAddress: 172.28.123.254
IP-MIB::ipNetToMediaNetAddress.4548.62.94.209.237 = IpAddress: 62.94.209.237
IP-MIB::ipNetToMediaNetAddress.4548.62.94.209.238 = IpAddress: 62.94.209.238
IP-MIB::ipNetToMediaNetAddress.4550.62.94.209.245 = IpAddress: 62.94.209.245
IP-MIB::ipNetToMediaNetAddress.4550.62.94.209.246 = IpAddress: 62.94.209.246
IP-MIB::ipNetToMediaNetAddress.4551.62.94.209.133 = IpAddress: 62.94.209.133
IP-MIB::ipNetToMediaNetAddress.4557.62.94.25.193 = IpAddress: 62.94.25.193
IP-MIB::ipNetToMediaNetAddress.4558.62.94.30.141 = IpAddress: 62.94.30.141
IP-MIB::ipNetToMediaNetAddress.4558.62.94.30.142 = IpAddress: 62.94.30.142
IP-MIB::ipNetToMediaNetAddress.4559.62.94.31.17 = IpAddress: 62.94.31.17
IP-MIB::ipNetToMediaNetAddress.4559.62.94.31.18 = IpAddress: 62.94.31.18
IP-MIB::ipNetToMediaNetAddress.4560.62.94.25.197 = IpAddress: 62.94.25.197
IP-MIB::ipNetToMediaNetAddress.4560.62.94.25.198 = IpAddress: 62.94.25.198
IP-MIB::ipNetToMediaNetAddress.4561.62.94.30.21 = IpAddress: 62.94.30.21
IP-MIB::ipNetToMediaNetAddress.4561.62.94.30.22 = IpAddress: 62.94.30.22
IP-MIB::ipNetToMediaNetAddress.4564.62.94.45.25 = IpAddress: 62.94.45.25
IP-MIB::ipNetToMediaNetAddress.4564.62.94.45.26 = IpAddress: 62.94.45.26
IP-MIB::ipNetToMediaNetAddress.4565.172.28.26.229 = IpAddress: 172.28.26.229
IP-MIB::ipNetToMediaNetAddress.4565.172.28.26.230 = IpAddress: 172.28.26.230
IP-MIB::ipNetToMediaNetAddress.4566.172.28.8.241 = IpAddress: 172.28.8.241
IP-MIB::ipNetToMediaNetAddress.4566.172.28.8.242 = IpAddress: 172.28.8.242
IP-MIB::ipNetToMediaNetAddress.4567.172.28.8.217 = IpAddress: 172.28.8.217
IP-MIB::ipNetToMediaNetAddress.4567.172.28.8.218 = IpAddress: 172.28.8.218
IP-MIB::ipNetToMediaNetAddress.4568.172.28.8.237 = IpAddress: 172.28.8.237
IP-MIB::ipNetToMediaNetAddress.4568.172.28.8.238 = IpAddress: 172.28.8.238
IP-MIB::ipNetToMediaNetAddress.4569.172.28.8.213 = IpAddress: 172.28.8.213
IP-MIB::ipNetToMediaNetAddress.4569.172.28.8.214 = IpAddress: 172.28.8.214
IP-MIB::ipNetToMediaNetAddress.4696.172.28.65.73 = IpAddress: 172.28.65.73
IP-MIB::ipNetToMediaNetAddress.4696.172.28.65.74 = IpAddress: 172.28.65.74
IP-MIB::ipNetToMediaNetAddress.4697.172.28.64.73 = IpAddress: 172.28.64.73
IP-MIB::ipNetToMediaNetAddress.4697.172.28.64.74 = IpAddress: 172.28.64.74
IP-MIB::ipNetToMediaNetAddress.4698.172.28.63.73 = IpAddress: 172.28.63.73
IP-MIB::ipNetToMediaNetAddress.4698.172.28.63.74 = IpAddress: 172.28.63.74
IP-MIB::ipNetToMediaNetAddress.4699.172.28.62.73 = IpAddress: 172.28.62.73
IP-MIB::ipNetToMediaNetAddress.4699.172.28.62.74 = IpAddress: 172.28.62.74
IP-MIB::ipNetToMediaNetAddress.4700.62.94.25.217 = IpAddress: 62.94.25.217
IP-MIB::ipNetToMediaNetAddress.4700.62.94.25.218 = IpAddress: 62.94.25.218
IP-MIB::ipNetToMediaNetAddress.4701.172.28.102.165 = IpAddress: 172.28.102.165
IP-MIB::ipNetToMediaNetAddress.4701.172.28.102.166 = IpAddress: 172.28.102.166
IP-MIB::ipNetToMediaNetAddress.4908.62.94.30.133 = IpAddress: 62.94.30.133
IP-MIB::ipNetToMediaNetAddress.4909.62.94.113.117 = IpAddress: 62.94.113.117
IP-MIB::ipNetToMediaNetAddress.4909.62.94.113.118 = IpAddress: 62.94.113.118
IP-MIB::ipNetToMediaNetAddress.4910.62.94.31.145 = IpAddress: 62.94.31.145
IP-MIB::ipNetToMediaNetAddress.4910.62.94.31.146 = IpAddress: 62.94.31.146
IP-MIB::ipNetToMediaNetAddress.4913.62.94.31.253 = IpAddress: 62.94.31.253
IP-MIB::ipNetToMediaNetAddress.4913.62.94.31.254 = IpAddress: 62.94.31.254
IP-MIB::ipNetToMediaNetAddress.4914.172.28.15.101 = IpAddress: 172.28.15.101
IP-MIB::ipNetToMediaNetAddress.4914.172.28.15.102 = IpAddress: 172.28.15.102
IP-MIB::ipNetToMediaNetAddress.5014.172.28.112.137 = IpAddress: 172.28.112.137
IP-MIB::ipNetToMediaNetAddress.5014.172.28.112.138 = IpAddress: 172.28.112.138

##############################################################################
# Per ciascun IP, ho l'info relativa alla tipologia (static/dynamic)

[root@network01 ~]# snmpwalk -v2c -c ipngy2k 192.168.1.27 IP-MIB::ipNetToMediaType
IP-MIB::ipNetToMediaType.22.192.168.1.27 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.28.212.90.1.2 = INTEGER: static(4)
IP-MIB::ipNetToMediaType.29.212.90.1.65 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.29.212.90.1.67 = INTEGER: static(4)
IP-MIB::ipNetToMediaType.29.212.90.1.68 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.29.212.90.1.69 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.29.212.90.1.70 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.29.212.90.1.71 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.29.212.90.1.72 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.29.212.90.1.76 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.29.212.90.1.77 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.29.212.90.1.78 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.29.212.90.1.79 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.29.212.90.1.80 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.29.212.90.1.81 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.29.212.90.1.82 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.29.212.90.1.83 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.29.212.90.1.84 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.29.212.90.1.85 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.30.212.90.1.34 = INTEGER: static(4)
IP-MIB::ipNetToMediaType.31.212.90.1.97 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.31.212.90.1.99 = INTEGER: static(4)
IP-MIB::ipNetToMediaType.31.212.90.1.100 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.31.212.90.1.101 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.31.212.90.1.102 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.31.212.90.1.103 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.31.212.90.1.104 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.31.212.90.1.108 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.31.212.90.1.109 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.31.212.90.1.110 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.31.212.90.1.111 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.31.212.90.1.112 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.31.212.90.1.113 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.31.212.90.1.114 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.31.212.90.1.115 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.31.212.90.1.116 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.31.212.90.1.117 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.932.62.94.30.245 = INTEGER: static(4)
IP-MIB::ipNetToMediaType.932.62.94.30.246 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.933.62.94.5.25 = INTEGER: static(4)
IP-MIB::ipNetToMediaType.933.62.94.5.26 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.934.62.94.5.61 = INTEGER: static(4)
IP-MIB::ipNetToMediaType.934.62.94.5.62 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.1559.62.94.46.89 = INTEGER: static(4)
IP-MIB::ipNetToMediaType.1559.62.94.46.90 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.1560.172.28.125.113 = INTEGER: static(4)
IP-MIB::ipNetToMediaType.1560.172.28.125.114 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.1929.62.94.45.165 = INTEGER: static(4)
IP-MIB::ipNetToMediaType.1929.62.94.45.166 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.1930.172.28.8.245 = INTEGER: static(4)
IP-MIB::ipNetToMediaType.1930.172.28.8.246 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.1931.172.28.8.221 = INTEGER: static(4)
IP-MIB::ipNetToMediaType.1931.172.28.8.222 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.3829.172.28.54.137 = INTEGER: static(4)
IP-MIB::ipNetToMediaType.3829.172.28.54.138 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.3830.62.94.25.21 = INTEGER: static(4)
IP-MIB::ipNetToMediaType.3830.62.94.25.22 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.3905.62.94.30.225 = INTEGER: static(4)
IP-MIB::ipNetToMediaType.3905.62.94.30.226 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.4527.62.94.129.249 = INTEGER: static(4)
IP-MIB::ipNetToMediaType.4538.62.94.30.37 = INTEGER: static(4)
IP-MIB::ipNetToMediaType.4538.62.94.30.38 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.4540.62.94.46.145 = INTEGER: static(4)
IP-MIB::ipNetToMediaType.4543.62.94.46.97 = INTEGER: static(4)
IP-MIB::ipNetToMediaType.4543.62.94.46.98 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.4544.62.94.5.93 = INTEGER: static(4)
IP-MIB::ipNetToMediaType.4544.62.94.5.94 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.4545.62.94.209.45 = INTEGER: static(4)
IP-MIB::ipNetToMediaType.4545.62.94.209.46 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.4546.62.94.209.101 = INTEGER: static(4)
IP-MIB::ipNetToMediaType.4546.62.94.209.102 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.4547.172.28.123.253 = INTEGER: static(4)
IP-MIB::ipNetToMediaType.4547.172.28.123.254 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.4548.62.94.209.237 = INTEGER: static(4)
IP-MIB::ipNetToMediaType.4548.62.94.209.238 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.4550.62.94.209.245 = INTEGER: static(4)
IP-MIB::ipNetToMediaType.4550.62.94.209.246 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.4551.62.94.209.133 = INTEGER: static(4)
IP-MIB::ipNetToMediaType.4557.62.94.25.193 = INTEGER: static(4)
IP-MIB::ipNetToMediaType.4558.62.94.30.141 = INTEGER: static(4)
IP-MIB::ipNetToMediaType.4558.62.94.30.142 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.4559.62.94.31.17 = INTEGER: static(4)
IP-MIB::ipNetToMediaType.4559.62.94.31.18 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.4560.62.94.25.197 = INTEGER: static(4)
IP-MIB::ipNetToMediaType.4560.62.94.25.198 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.4561.62.94.30.21 = INTEGER: static(4)
IP-MIB::ipNetToMediaType.4561.62.94.30.22 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.4564.62.94.45.25 = INTEGER: static(4)
IP-MIB::ipNetToMediaType.4564.62.94.45.26 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.4565.172.28.26.229 = INTEGER: static(4)
IP-MIB::ipNetToMediaType.4565.172.28.26.230 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.4566.172.28.8.241 = INTEGER: static(4)
IP-MIB::ipNetToMediaType.4566.172.28.8.242 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.4567.172.28.8.217 = INTEGER: static(4)
IP-MIB::ipNetToMediaType.4567.172.28.8.218 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.4568.172.28.8.237 = INTEGER: static(4)
IP-MIB::ipNetToMediaType.4568.172.28.8.238 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.4569.172.28.8.213 = INTEGER: static(4)
IP-MIB::ipNetToMediaType.4569.172.28.8.214 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.4696.172.28.65.73 = INTEGER: static(4)
IP-MIB::ipNetToMediaType.4696.172.28.65.74 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.4697.172.28.64.73 = INTEGER: static(4)
IP-MIB::ipNetToMediaType.4697.172.28.64.74 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.4698.172.28.63.73 = INTEGER: static(4)
IP-MIB::ipNetToMediaType.4698.172.28.63.74 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.4699.172.28.62.73 = INTEGER: static(4)
IP-MIB::ipNetToMediaType.4699.172.28.62.74 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.4700.62.94.25.217 = INTEGER: static(4)
IP-MIB::ipNetToMediaType.4700.62.94.25.218 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.4701.172.28.102.165 = INTEGER: static(4)
IP-MIB::ipNetToMediaType.4701.172.28.102.166 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.4908.62.94.30.133 = INTEGER: static(4)
IP-MIB::ipNetToMediaType.4909.62.94.113.117 = INTEGER: static(4)
IP-MIB::ipNetToMediaType.4909.62.94.113.118 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.4910.62.94.31.145 = INTEGER: static(4)
IP-MIB::ipNetToMediaType.4910.62.94.31.146 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.4913.62.94.31.253 = INTEGER: static(4)
IP-MIB::ipNetToMediaType.4913.62.94.31.254 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.4914.172.28.15.101 = INTEGER: static(4)
IP-MIB::ipNetToMediaType.4914.172.28.15.102 = INTEGER: dynamic(3)
IP-MIB::ipNetToMediaType.5014.172.28.112.137 = INTEGER: static(4)
IP-MIB::ipNetToMediaType.5014.172.28.112.138 = INTEGER: dynamic(3)

###################################################################

DESIDERATA FINALE:
Ip address 172.28.112.138 di tipo dynamic, con mac-address 0:1a:6c:6d:c5:ec attivo su porta TenGigabitEthernet0/1/2.13140002