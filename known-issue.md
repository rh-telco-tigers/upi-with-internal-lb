
There are some know issue with this POC,

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
