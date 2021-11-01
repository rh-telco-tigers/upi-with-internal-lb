# upi-with-internal-lb
Process to install using UPI with internal Load balancer


# Download openshift-install
```
curl -LO https://mirror.openshift.com/pub/openshift-v4/clients/ocp/4.6.49/openshift-install-linux-4.6.49.tar.gz
tar -zxvf openshift-install-linux-4.6.49.tar.gz 
```

# Download oc, kubectl client
```
curl -LO https://mirror.openshift.com/pub/openshift-v4/clients/ocp/4.6.49/openshift-client-linux-4.6.49.tar.gz
tar -zxvf openshift-client-linux-4.6.49.tar.gz
```

# Download RCHOS image and create openstack image
```
curl -LO https://mirror.openshift.com/pub/openshift-v4/dependencies/rhcos/4.6/4.6.47/rhcos-openstack.x86_64.qcow2.gz

gzip -d rhcos-openstack.x86_64.qcow2.gz 

openstack image create --container-format=bare --disk-format=qcow2 --file rhcos-openstack.x86_64.qcow2 rhcos-openstack.4.6.47.x86_64.qcow2
```

## Create openstack floating ips

```
openstack network list

NETWORK_ID="58439661-2a6f-4698-8364-0a4910830c58"
openstack floating ip create --description "API ocpinternallb.zerotodevops.com" ${NETWORK_ID}
openstack floating ip create --description "Ingress ocpinternallb.zerotodevops.com" ${NETWORK_ID}
openstack floating ip create --description "bootstrap machine for ocpinternallb" ${NETWORK_ID}
```
