# Introduction
This post demonstrates how to install an OpenShift cluster using the UPI technique without the need for an external loadbalancer in OpenStack. We will deploy both Keepalived and Haproxy components in the same cluster, eliminating the requirement for an external loadbalancer.

> Note: We built the infrastructure with an Openstack Tripleo cluster, but it should be possible to reproduce it with any Openstack cluster.

## Pre-requisites
- Access to Openstack Environment
- Access to cloud.redhat.com
- ansible-playbook cli

## Download and install openshift-install, oc and kubectl
- For linux execute script `scripts/0x-linux-install-tools.sh`
- For Mac execute script `scripts/0x-mac-install-tools.sh`

## Download RCHOS image and create openstack image
Execute script `scripts/0x-openstack-create-image.sh`

## Create Openstack floating ips
We need these ip addresses to access the k8s API, the boostrap machine, and the ingress API; see the inventory.yaml section for additional information.

```
openstack network list

NETWORK_ID=<YOUR-NETWORK-ID>
openstack floating ip create --description "demotel API" ${NETWORK_ID}
openstack floating ip create --description "demotel Ingress" ${NETWORK_ID}
openstack floating ip create --description "demotel Bootstrap" ${NETWORK_ID}
```

## Execute scripts in sequence

1. Get ansible playbooks using script `01-get-ansible-playbook.sh`
Once you get the playbook, make sure to change `inventory.yaml` as per your environment. For example
```
all:
  hosts:
    localhost:
      ansible_connection: local
      ansible_python_interpreter: "{{ansible_playbook_python}}"

      # User-provided values
      os_subnet_range: '10.0.0.0/16'
      os_flavor_master: 'm1.xlarge'
      os_flavor_worker: 'm1.xlarge'
      os_image_rhcos: 'rhcos-openstack.4.6.47.x86_64.qcow2'
      # Service subnet cidr
      svc_subnet_range: '172.30.0.0/16'
      os_svc_network_range: '172.30.0.0/15'
      # Subnet pool prefixes
      cluster_network_cidrs: '10.128.0.0/14'
      # Subnet pool prefix length
      host_prefix: '23'
      # Name of the SDN.
      # Possible values are OpenshiftSDN or Kuryr.
      os_networking_type: 'OpenshiftSDN'

      # Number of provisioned Control Plane nodes
      # 3 is the minimum number for a fully-functional cluster.
      os_cp_nodes_number: 3

      # Number of provisioned Compute nodes.
      # 3 is the minimum number for a fully-functional cluster.
      os_compute_nodes_number: 3

      # The public network providing connectivity to the cluster. If not
      # provided, the cluster external connectivity must be provided in another
      # way.
      #
      # Required for os_api_fip, os_ingress_fip, os_bootstrap_fip.
      os_external_network: 'public'

      # OpenShift API floating IP address. If this value is non-empty, the
      # corresponding floating IP will be attached to the Control Plane to
      # serve the OpenShift API.
      os_api_fip: '192.168.5.126'

      # OpenShift Ingress floating IP address. If this value is non-empty, the
      # corresponding floating IP will be attached to the worker nodes to serve
      # the applications.
      os_ingress_fip: '192.168.5.179'

      # If this value is non-empty, the corresponding floating IP will be
      # attached to the bootstrap machine. This is needed for collecting logs
      # in case of install failure.
      os_bootstrap_fip: '192.168.5.200'
```

2. Add your image pull secrets to `install-dir/install-config.yaml` and use `02-initial-ignition-config.sh` to construct initial ignition configs.
3. Modify bootstrap ignition configs using `03-modify-bootstrap-ignition.sh`, we are using python script to generate this ignition config.
4. Modify master ignition configs using `04-modify-master-ignition.sh` scripts.
5. Upload bootstrap ignition config to Openstack Glance using `05-upload-bootstrap-ignition.sh`. Technically, you can host this ignition configuration on any webserver.
6. Finally create the cluster using `06-create-cluster.sh`