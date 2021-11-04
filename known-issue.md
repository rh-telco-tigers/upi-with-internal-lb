
There are some know issue with this POC,

- The file `haproxy.cfg` was not created with the appropriate permissions,
```
ls -la /etc/haproxy/
total 16
drwxr-xr-x.  2 root root   25 Nov  4 18:27 .
drwxr-xr-x. 94 root root 8192 Nov  4 18:28 ..
--w----r--.  1 root root 1068 Nov  4 18:28 haproxy.cfg
```

So  I was seeing following issue,

```
$ oc logs -n openshift-openstack-infra                          haproxy-demotelbm-9b9bp-master-2    haproxy -p
+ declare -r haproxy_sock=/var/run/haproxy/haproxy-master.sock
+ declare -r haproxy_log_sock=/var/run/haproxy/haproxy-log.sock
+ export -f msg_handler
+ export -f reload_haproxy
+ export -f verify_old_haproxy_ps_being_deleted
+ rm -f /var/run/haproxy/haproxy-master.sock /var/run/haproxy/haproxy-log.sock
+ '[' -s /etc/haproxy/haproxy.cfg ']'
+ socat UNIX-RECV:/var/run/haproxy/haproxy-log.sock STDOUT
+ socat UNIX-LISTEN:/var/run/haproxy/haproxy-master.sock,fork 'system:bash -c msg_handler'
+ /usr/sbin/haproxy -W -db -f /etc/haproxy/haproxy.cfg -p /var/lib/haproxy/run/haproxy.pid
[ALERT] 307/184250 (10) : Could not open configuration file /etc/haproxy/haproxy.cfg : Permission denied
```

I'm using the following command as a workaround to address the problem:

```
sudo chmod 644 /etc/haproxy/haproxy.cfg 
```

- The upgrade from 4.6.47 to 4.6.48 is complete, however the following components are not updated. These are the components we added manually.
  - coredns
  - haproxy
  - keepalived
  - mdns-publisher

- I had an intermittent issue with the bootstrap process, which got stuck in a loop and never recovered.
```
Nov 04 16:32:23 demotel-4hbnz-bootstrap bootkube.sh[2361]: "99_openshift-machineconfig_99-master-ssh.yaml": unable to get REST mapping for "99_openshift-machineconfig_99-master-ssh.yaml": no matches for kind "MachineConfig" in version "machineconfiguration.openshift.io/v1"
Nov 04 16:32:23 demotel-4hbnz-bootstrap bootkube.sh[2361]: "99_openshift-machineconfig_99-worker-ssh.yaml": unable to get REST mapping for "99_openshift-machineconfig_99-worker-ssh.yaml": no matches for kind "MachineConfig" in version "machineconfiguration.openshift.io/v1"
```
Found a previously closed similar issue, https://access.redhat.com/solutions/5207731

- Because /etc/resolve.conf was not changed and pointed to the local dns server, i used an external dns provider as a workaround and established the following 2 record sets, both of which pointed to the internal vip api address.

```
api-int.demotelbm.zerotodevops.com	A	10.0.0.5
api.demotelbm.zerotodevops.com	A   10.0.0.5
```