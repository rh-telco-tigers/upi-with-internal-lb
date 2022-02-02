Hyperconverged Openshift cluster:

- 3 nodes (Master and work same)
- Networking profile
	- Outbound: All egress traffic from nodes
	- Cluster: All cluster to cluster communication
	- Management: Other utlities network
	- Public:  Tenant network, Ingress, External API Access
- Remove dependencies on external loadbalancer

 

## Ansible Inventory
- Setup OSP ports for all 4 networks
- Setup security groups
- Upload ignition config to swift
- Setup bootstrap machine
- Setup control plane
- Tear down control plane
- Tear down boostrap
- Tear down Security Groups
- Tear OSP ports
- Delete ignition config

## Ignition config generator
- filetranspile  (https://github.com/ashcrow/filetranspiler)
- Creates an Ignition JSON file from a fake root.

```
fakeroot
└── etc
    ├── kubernetes
    │   ├── manifests
    │   │   ├── coredns.yaml
    │   │   ├── haproxy.yaml
    │   │   ├── keepalived.yaml
    │   │   └── mdns-publisher.yaml
    │   └── static-pod-resources
    │       ├── coredns
    │       │   └── Corefile.tmpl
    │       ├── haproxy
    │       │   ├── Readme.md
    │       │   └── haproxy.cfg.tmpl
    │       ├── keepalived
    │       │   ├── Readme.md
    │       │   ├── keepalived.conf.tmpl
    │       │   └── scripts
    │       │       ├── Readme.md
    │       │       ├── chk_ocp_script.sh.tmpl
    │       │       └── chk_ocp_script_both.sh.tmpl
    │       └── mdns
    │           ├── Readme.md
    │           └── config.hcl.tmpl
    ├── sysconfig
    │   └── network-scripts
    │       ├── ifcfg-ens3
    │       ├── ifcfg-ens4
    │       ├── ifcfg-ens5
    │       ├── ifcfg-ens6
    │       ├── route-ens4
    │       └── route-ens5
    └── systemd
        └── system
            └── kubelet.service.d
                └── 80-nodeip.conf

14 directories, 21 files
```


## Bootstrap Ignition Config
### Static manifest files
- coredns 
- keepalived

## Master Ignition Config
### Static manifest files
- coredns 
- keepalived
- haproxy
- mdns-publisher

### Network config
- outbound default route
- public, policy based routing
- cluster/ interconnect 
- management (static routes)

### kubelet config 
- to force interconnect network for nodes

## Openstack Swift: Ignition config storage


## Known issue
- keepalived master entering into BACKUP STATE immediately when reloading service 
- version 2.0.10
- Keepalived v2.1.5 (issue fixed)
- 
- resulting packet loss (public access only) 
- https://github.com/acassen/keepalived/issues/1425


