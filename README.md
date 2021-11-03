# upi-with-internal-lb
Process to install using UPI with internal Load balancer


# Export
export OS_CLOUD="standalone"
export INFRA_ID=$(jq -r .infraID metadata.json)

# Download openshift-install
```
curl -LO https://mirror.openshift.com/pub/openshift-v4/clients/ocp/4.6.49/openshift-install-linux-4.6.49.tar.gz
tar -zxvf openshift-install-linux-4.6.49.tar.gz 


curl -LO https://mirror.openshift.com/pub/openshift-v4/clients/ocp/4.6.47/openshift-client-mac-4.6.47.tar.gz
tar -zxvf openshift-client-mac-4.6.47.tar.gz

curl -LO https://mirror.openshift.com/pub/openshift-v4/clients/ocp/4.6.47/openshift-install-mac-4.6.47.tar.gz

tar -zxvf openshift-install-mac-4.6.47.tar.gz


curl -LO curl -LO https://mirror.openshift.com/pub/openshift-v4/clients/ocp/4.6.47/openshift-install-linux-4.6.47.tar.gz
tar -zxvf openshift-install-linux-4.6.47.tar.gz
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
openstack floating ip create --description "demotel API" ${NETWORK_ID}
openstack floating ip create --description "demotel Ingress" ${NETWORK_ID}
openstack floating ip create --description "demotel Bootstrap" ${NETWORK_ID}


# demotelbm
NETWORK_ID="58439661-2a6f-4698-8364-0a4910830c58"
openstack floating ip create --description "demotelbm API" ${NETWORK_ID}
- 192.168.5.155
openstack floating ip create --description "demotelbm Ingress" ${NETWORK_ID}
- 192.168.5.93
openstack floating ip create --description "demotelbm Bootstrap" ${NETWORK_ID}
- 192.168.5.184
```


## Prepare ignition config
```
./openshift-install create install-config --dir=install-dir
./openshift-install create manifests --dir=install-dir
rm -f openshift/99_openshift-cluster-api_master-machines-*.yaml openshift/99_openshift-cluster-api_worker-machineset-*.yaml
./openshift-install create ignition-configs --dir=install-dir 
```

## Preparing the bootstrap Ignition files

```
import base64
import json
import os

with open('bootstrap.ign', 'r') as f:
    ignition = json.load(f)

files = ignition['storage'].get('files', [])

infra_id = os.environ.get('INFRA_ID', 'openshift').encode()
hostname_b64 = base64.standard_b64encode(infra_id + b'-bootstrap\n').decode().strip()
files.append(
{
    'path': '/etc/hostname',
    'mode': 420,
    'contents': {
        'source': 'data:text/plain;charset=utf-8;base64,' + hostname_b64
    }
})

ca_cert_path = os.environ.get('OS_CACERT', '')
if ca_cert_path:
    with open(ca_cert_path, 'r') as f:
        ca_cert = f.read().encode()
        ca_cert_b64 = base64.standard_b64encode(ca_cert).decode().strip()

    files.append(
    {
        'path': '/opt/openshift/tls/cloud-ca-cert.pem',
        'mode': 420,
        'contents': {
            'source': 'data:text/plain;charset=utf-8;base64,' + ca_cert_b64
        }
    })

ignition['storage']['files'] = files;

with open('bootstrap.ign', 'w') as f:
    json.dump(ignition, f)
```

```

xargs -n 1 curl -O <<< '
        https://raw.githubusercontent.com/openshift/installer/release-4.6/upi/openstack/bootstrap.yaml
        https://raw.githubusercontent.com/openshift/installer/release-4.6/upi/openstack/common.yaml
        https://raw.githubusercontent.com/openshift/installer/release-4.6/upi/openstack/compute-nodes.yaml
        https://raw.githubusercontent.com/openshift/installer/release-4.6/upi/openstack/control-plane.yaml
        https://raw.githubusercontent.com/openshift/installer/release-4.6/upi/openstack/inventory.yaml
        https://raw.githubusercontent.com/openshift/installer/release-4.6/upi/openstack/network.yaml
        https://raw.githubusercontent.com/openshift/installer/release-4.6/upi/openstack/security-groups.yaml
        https://raw.githubusercontent.com/openshift/installer/release-4.6/upi/openstack/down-bootstrap.yaml
        https://raw.githubusercontent.com/openshift/installer/release-4.6/upi/openstack/down-compute-nodes.yaml
        https://raw.githubusercontent.com/openshift/installer/release-4.6/upi/openstack/down-control-plane.yaml
        https://raw.githubusercontent.com/openshift/installer/release-4.6/upi/openstack/down-load-balancers.yaml
        https://raw.githubusercontent.com/openshift/installer/release-4.6/upi/openstack/down-network.yaml
        https://raw.githubusercontent.com/openshift/installer/release-4.6/upi/openstack/down-security-groups.yaml
        https://raw.githubusercontent.com/openshift/installer/release-4.6/upi/openstack/down-containers.yaml'


ansible-playbook -i inventory.yaml security-groups.yaml
ansible-playbook -i inventory.yaml network.yaml
openstack quota set --secgroups 300 --secgroup-rules 1000 admin
```

```
export INFRA_ID=$(jq -r .infraID metadata.json)
openstack console log show "$INFRA_ID-bootstrap"
openshift-install wait-for bootstrap-complete
```

## Bootstrap Image
```
openstack image create --disk-format=raw --container-format=bare --file bootstrap.ign ocp-$INFRA_ID-bootstrap.ign
openstack image show ocp-4.9-bootstrap.ign
openstack catalog show image
```

```
openstack token issue -c id -f value
vim $INFRA_ID-bootstrap-ignition.json
```

```
{
  "ignition": {
    "config": {
      "merge": [{
        "source": "http://192.168.7.213:9292/v2/images/1999ea1e-0f3d-4d93-be17-72c346c87783/file", 
        "httpHeaders": [{
          "name": "X-Auth-Token", 
          "value": "gAAAAABhgpwNCRt9pgq6AKCh6MUXsBAWfKMsC-N36OlVgRPII29bvIpoCwLZuuTn-sZZehPU9l-e9spuBxQxpLI7wsu3P3W_UgDrUC4iJ3xQb9WQgRPlJYB3nOiZYA8PWV0WmAUlPFiwN2neft2Lllz2hH7KGE7sbvMAcVOX9s3jDtxqrxvpxBg" 
        }]
      }]
    },
    "version": "3.1.0"
  }
}
```

## Control plane ignition config
```
for index in $(seq 0 2); do
    MASTER_HOSTNAME="$INFRA_ID-master-$index\n"
    python -c "import base64, json, sys;
ignition = json.load(sys.stdin);
storage = ignition.get('storage', {});
files = storage.get('files', []);
files.append({'path': '/etc/hostname', 'mode': 420, 'contents': {'source': 'data:text/plain;charset=utf-8;base64,' + base64.standard_b64encode(b'$MASTER_HOSTNAME').decode().strip(), 'verification': {}}, 'filesystem': 'root'});
storage['files'] = files;
ignition['storage'] = storage
json.dump(ignition, sys.stdout)" <master.ign >"$INFRA_ID-master-$index-ignition.json"
done
```

```
for index in $(seq 0 2); do MASTER_IGNITION_FILE=$INFRA_ID-master-$index-ignition.json  python master-ignition-custom.py ; done
```