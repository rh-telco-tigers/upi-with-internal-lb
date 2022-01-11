## Ignition Config
OPENSHIFT_INSTALL_CMD="./scripts/openshift-install"
${OPENSHIFT_INSTALL_CMD} create manifests --dir=install-dir
${OPENSHIFT_INSTALL_CMD} create ignition-configs --dir=install-dir 

## Modify Bootstrap Ignition
export INFRA_ID=$(jq -r .infraID install-dir/metadata.json)
python _bootstrap-ignition.py
docker run --rm -ti --volume `pwd`:/srv:z filetranspile:latest -i install-dir/bootstrap.ign -f bootstrap/fakeroot  -o install-dir/custom-bootstrap.ign

## Modify Master Ignition
for index in $(seq 0 2); do
    MASTER_HOSTNAME="$INFRA_ID-master-$index\n"
    python -c "import base64, json, sys;
ignition = json.load(sys.stdin);
storage = ignition.get('storage', {});
files = storage.get('files', []);
files.append({'path': '/etc/hostname', 'mode': 420, 'contents': {'source': 'data:text/plain;charset=utf-8;base64,' + base64.standard_b64encode(b'$MASTER_HOSTNAME').decode().strip(), 'verification': {}}, 'filesystem': 'root'});
files.append({'path': '/etc/mdns/hostname', 'mode': 420, 'contents': {'source': 'data:text/plain;charset=utf-8;base64,' + base64.standard_b64encode(b'$MASTER_HOSTNAME').decode().strip(), 'verification': {}}, 'filesystem': 'root'});
storage['files'] = files;
ignition['storage'] = storage
json.dump(ignition, sys.stdout)" <install-dir/master.ign > "install-dir/$INFRA_ID-master-$index-ignition.json"

done

docker run --rm -ti --volume `pwd`:/srv:z filetranspile:latest -i install-dir/$INFRA_ID-master-0-ignition.json -f master0/fakeroot  -o install-dir/$INFRA_ID-master-0-ignition.json
docker run --rm -ti --volume `pwd`:/srv:z filetranspile:latest -i install-dir/$INFRA_ID-master-1-ignition.json -f master1/fakeroot  -o install-dir/$INFRA_ID-master-1-ignition.json
docker run --rm -ti --volume `pwd`:/srv:z filetranspile:latest -i install-dir/$INFRA_ID-master-2-ignition.json -f master2/fakeroot  -o install-dir/$INFRA_ID-master-2-ignition.json

## Upload ignition 

export CONTAINER_NAME="ocp30-ignition"
export CERTIFICATE=$(cat ~/.openstack/nfvi.crt | base64 )
export CONTAINER_TENANT_ID=$(openstack container show $CONTAINER_NAME -f json | jq -r .account)
export SWIFT_URL_TEMP=$(openstack endpoint list -f json | jq -r '.[] | select((."Service Name"=="swift") and (."Interface"=="public")) | .URL')
export SWIFT_URL=$(echo $SWIFT_URL_TEMP | sed -r "s/AUTH_\%\(tenant_id\)s/$CONTAINER_TENANT_ID/g")
export TOKEN=$(openstack token issue -c id -f value)

openstack object create --name $INFRA_ID-bootstrap.ign $CONTAINER_NAME install-dir/custom-bootstrap.ign

cat <<EOF > install-dir/$INFRA_ID-bootstrap-ignition.json
{
  "ignition": {
    "config": {
      "merge": [{
        "source": "${SWIFT_URL}/${CONTAINER_NAME}/${INFRA_ID}-bootstrap.ign", 
        "httpHeaders": [{
          "name": "X-Auth-Token", 
          "value": "${TOKEN}" 
        }]
      }]
    },
    "security": {
      "tls": {
        "certificateAuthorities": [{
          "source": "data:text/plain;charset=utf-8;base64,${CERTIFICATE}" 
        }]
      }
    },
    "version": "3.1.0"
  }
}
EOF

## Create cluster
cd install-dir
ansible-playbook -i inventory.yaml security-groups.yaml
ansible-playbook -i inventory.yaml ports.yaml
ansible-playbook -i inventory.yaml bootstrap.yaml
ansible-playbook -i inventory.yaml control-plane.yaml