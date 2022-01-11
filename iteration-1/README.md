### Route
```
[core@ocp300-4qxqq-master-0 ~]$ route -n
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         172.21.104.1    0.0.0.0         UG    800    0        0 br-ex
10.128.0.0      10.130.0.1      255.252.0.0     UG    0      0        0 ovn-k8s-mp0
10.130.0.0      0.0.0.0         255.255.254.0   U     0      0        0 ovn-k8s-mp0
169.254.0.0     0.0.0.0         255.255.240.0   U     0      0        0 ovn-k8s-gw0
172.21.104.0    0.0.0.0         255.255.255.192 U     800    0        0 br-ex
172.30.0.0      10.130.0.1      255.255.0.0     UG    0      0        0 ovn-k8s-mp0
```

### Ip addr
```
[core@ocp300-4qxqq-master-0 ~]$ ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: ens3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 2150 qdisc fq_codel master ovs-system state UP group default qlen 1000
    link/ether 02:69:16:48:a3:83 brd ff:ff:ff:ff:ff:ff
3: ovs-system: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000
    link/ether ca:1e:8a:35:fc:c2 brd ff:ff:ff:ff:ff:ff
4: br-ex: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 2150 qdisc noqueue state UNKNOWN group default qlen 1000
    link/ether 02:69:16:48:a3:83 brd ff:ff:ff:ff:ff:ff
    inet 172.21.104.21/26 brd 172.21.104.63 scope global noprefixroute br-ex
       valid_lft forever preferred_lft forever
    inet6 fe80::a457:16ff:fe47:9ade/64 scope link 
       valid_lft forever preferred_lft forever
5: br-int: <BROADCAST,MULTICAST> mtu 2050 qdisc noop state DOWN group default qlen 1000
    link/ether be:e7:b2:f4:1c:00 brd ff:ff:ff:ff:ff:ff
6: genev_sys_6081: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 65000 qdisc noqueue master ovs-system state UNKNOWN group default qlen 1000
    link/ether b6:0e:c0:11:15:b5 brd ff:ff:ff:ff:ff:ff
    inet6 fe80::b40e:c0ff:fe11:15b5/64 scope link 
       valid_lft forever preferred_lft forever
7: br-local: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 2050 qdisc noqueue state UNKNOWN group default qlen 1000
    link/ether 3a:1b:52:f8:a4:40 brd ff:ff:ff:ff:ff:ff
    inet6 fe80::381b:52ff:fef8:a440/64 scope link 
       valid_lft forever preferred_lft forever
```


### curl test
```
[core@ocp300-4qxqq-master-0 ~]$ curl https://oauth-openshift.apps.ocp300.nfvdev.tlabs.ca/oauth/token -k
{"error":"unsupported_grant_type","error_description":"The authorization grant type is not supported by the authorization server."}
```

```
[v0268030@TLABS.ca@osptenantjp ~]$ oc exec console-74cf9d7676-gdxzw -n  openshift-console -- /bin/curl https://oauth-openshift.apps.ocp300.nfvdev.tlabs.ca/oauth/token  -k
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   132  100   132    0     0   5280      0 --:--:-- --:--:-- --:--:--  5280
{"error":"unsupported_grant_type","error_description":"The authorization grant type is not supported by the authorization server."}
```

### Console 
```
[v0268030@TLABS.ca@osptenantjp ~]$ oc get pods -n openshift-console -w
NAME                         READY   STATUS    RESTARTS   AGE
console-74cf9d7676-gdxzw     1/1     Running   0          5m39s
console-74cf9d7676-mfrfq     1/1     Running   0          8m14s
downloads-59cc69bd8d-dzg52   1/1     Running   0          12m
downloads-59cc69bd8d-rvxnx   1/1     Running   0          12m
```