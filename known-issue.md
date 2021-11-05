
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



```
[core@demotelbm-9b9bp-bootstrap ~]$ sudo crictl logs 277fcc2cb3557
I1104 16:39:27.135474       1 bootstrap.go:37] Version: v4.6.0-202109221828.p0.git.cb3a981.assembly.stream-dirty (cb3a98105211586a299d25a373cf752df6b5341e)
I1104 16:39:27.135786       1 api.go:72] Launching server on :22624
I1104 16:39:27.135918       1 api.go:72] Launching server on :22623
I1104 16:39:29.536108       1 api.go:117] Pool master requested by address:"10.0.2.113:40148" User-Agent:"Ignition/2.6.0" Accept-Header: "application/vnd.coreos.ignition+json;version=3.1.0, */*;q=0.1"
I1104 16:39:29.536230       1 bootstrap_server.go:66] reading file "/etc/mcs/bootstrap/machine-pools/master.yaml"
I1104 16:39:29.543396       1 bootstrap_server.go:86] reading file "/etc/mcs/bootstrap/machine-configs/rendered-master-7b3cdb28e6f501e7615cd141785b0ce0.yaml"
I1104 16:39:31.235932       1 api.go:117] Pool master requested by address:"10.0.2.196:47332" User-Agent:"Ignition/2.6.0" Accept-Header: "application/vnd.coreos.ignition+json;version=3.1.0, */*;q=0.1"
I1104 16:39:31.236005       1 bootstrap_server.go:66] reading file "/etc/mcs/bootstrap/machine-pools/master.yaml"
I1104 16:39:31.237855       1 bootstrap_server.go:86] reading file "/etc/mcs/bootstrap/machine-configs/rendered-master-7b3cdb28e6f501e7615cd141785b0ce0.yaml"
I1104 16:39:34.124873       1 api.go:117] Pool master requested by address:"10.0.1.28:49746" User-Agent:"Ignition/2.6.0" Accept-Header: "application/vnd.coreos.ignition+json;version=3.1.0, */*;q=0.1"
I1104 16:39:34.124955       1 bootstrap_server.go:66] reading file "/etc/mcs/bootstrap/machine-pools/master.yaml"
I1104 16:39:34.128452       1 bootstrap_server.go:86] reading file "/etc/mcs/bootstrap/machine-configs/rendered-master-7b3cdb28e6f501e7615cd141785b0ce0.yaml"
```