### Route
```
[core@ocp300-snz4c-master-0 ~]$ route -n
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         172.21.104.1    0.0.0.0         UG    800    0        0 br-ex
10.128.0.0      10.130.0.1      255.252.0.0     UG    0      0        0 ovn-k8s-mp0
10.130.0.0      0.0.0.0         255.255.254.0   U     0      0        0 ovn-k8s-mp0
169.254.0.0     0.0.0.0         255.255.240.0   U     0      0        0 ovn-k8s-gw0
172.21.104.0    0.0.0.0         255.255.255.192 U     800    0        0 br-ex
172.21.112.0    0.0.0.0         255.255.255.224 U     101    0        0 ens4
172.30.0.0      10.130.0.1      255.255.0.0     UG    0      0        0 ovn-k8s-mp0
```

### ip addr
```
[core@ocp300-snz4c-master-0 ~]$ ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: ens3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 2150 qdisc fq_codel master ovs-system state UP group default qlen 1000
    link/ether 02:eb:45:8f:d6:af brd ff:ff:ff:ff:ff:ff
3: ens4: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 02:f3:bb:e7:e7:61 brd ff:ff:ff:ff:ff:ff
    inet 172.21.112.21/27 brd 172.21.112.31 scope global noprefixroute ens4
       valid_lft forever preferred_lft forever
    inet6 fe80::f3:bbff:fee7:e761/64 scope link 
       valid_lft forever preferred_lft forever
4: ovs-system: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000
    link/ether 82:60:1d:08:77:df brd ff:ff:ff:ff:ff:ff
5: br-ex: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 2150 qdisc noqueue state UNKNOWN group default qlen 1000
    link/ether 02:eb:45:8f:d6:af brd ff:ff:ff:ff:ff:ff
    inet 172.21.104.21/26 brd 172.21.104.63 scope global noprefixroute br-ex
       valid_lft forever preferred_lft forever
    inet 172.21.112.25/32 scope global br-ex
       valid_lft forever preferred_lft forever
    inet6 fe80::20df:27ff:fed7:e03e/64 scope link 
       valid_lft forever preferred_lft forever
6: br-int: <BROADCAST,MULTICAST> mtu 2050 qdisc noop state DOWN group default qlen 1000
    link/ether 56:cd:83:a8:a3:fd brd ff:ff:ff:ff:ff:ff
7: genev_sys_6081: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 65000 qdisc noqueue master ovs-system state UNKNOWN group default qlen 1000
    link/ether fe:7e:5a:69:0f:e7 brd ff:ff:ff:ff:ff:ff
    inet6 fe80::fc7e:5aff:fe69:fe7/64 scope link 
       valid_lft forever preferred_lft forever
8: br-local: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 2050 qdisc noqueue state UNKNOWN group default qlen 1000
    link/ether fa:b7:de:c0:a6:43 brd ff:ff:ff:ff:ff:ff
    inet6 fe80::f8b7:deff:fec0:a643/64 scope link 
       valid_lft forever preferred_lft forever
```

### curl test
- from node
```
[core@ocp300-snz4c-master-0 ~]$ curl https://oauth-openshift.apps.ocp300.nfvdev.tlabs.ca/oauth/token -k
{"error":"unsupported_grant_type","error_description":"The authorization grant type is not supported by the authorization server."}
[core@ocp300-snz4c-master-0 ~]$ nslookup oauth-openshift.apps.ocp300.nfvdev.tlabs.ca
;; Got recursion not available from 172.21.104.21, trying next server
Server:		205.206.214.249
Address:	205.206.214.249#53

Name:	oauth-openshift.apps.ocp300.nfvdev.tlabs.ca
Address: 172.21.112.26
;; Got recursion not available from 172.21.104.21, trying next server
```

- from pod

```
[core@ocp300-snz4c-master-0 ~]$  oc exec console-66486998fb-2mxwm -n  openshift-console -- /bin/curl https://oauth-openshift.apps.ocp300.nfvdev.tlabs.ca/oauth/token  -k
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0{"error":"unsupported_grant_type","error_description":"The authorization grant type is not supported by the authorization server."}
100   132  100   132    0     0   6000      0 --:--:-- --:--:-- --:--:--  6000

[core@ocp300-snz4c-master-0 ~]$ oc exec console-66486998fb-2mxwm -n  openshift-console -- nslookup oauth-openshift.apps.ocp300.nfvdev.tlabs.ca
Server:		172.30.0.10
Address:	172.30.0.10#53

Name:	oauth-openshift.apps.ocp300.nfvdev.tlabs.ca
Address: 172.21.104.26
```

### console pod
```
[core@ocp300-snz4c-master-0 ~]$ oc get pods -n openshift-console
NAME                         READY   STATUS    RESTARTS   AGE
console-66486998fb-2mxwm     1/1     Running   0          20m
console-66486998fb-z45q8     1/1     Running   4          20m
downloads-59cc69bd8d-4dzjt   1/1     Running   0          21m
downloads-59cc69bd8d-9k595   1/1     Running   0          21m
```