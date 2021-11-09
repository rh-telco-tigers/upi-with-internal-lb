
There are some know issue with this POC,

- The upgrade from 4.6.47 to 4.6.48 is complete, however the following components are not updated. These are the components we added manually.
  - coredns
  - haproxy
  - keepalived
  - mdns-publisher

- Because /etc/resolv.conf was not changed and pointed to the local dns server, i used an external dns provider as a workaround and established the following 2 record sets, both of which pointed to the internal vip api address.

```
api-int.demotelbm.zerotodevops.com	A	10.0.0.5
api.demotelbm.zerotodevops.com	A   10.0.0.5
```
