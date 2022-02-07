
## Upload ignition 
cd install-dir

export INFRA_ID=$(yq -r .all.hosts.localhost.cluster_name inventory.yaml)
export CONTAINER_NAME=$(yq -r .all.hosts.localhost.swift_container_name inventory.yaml)
export DOMAIN_NAME=$(yq -r .all.hosts.localhost.dns_nameservers.domain inventory.yaml)
export CERTIFICATE=$(cat ~/.openstack/nfvi.crt | base64 )
export CONTAINER_TENANT_ID=$(openstack container show $CONTAINER_NAME -f json | jq -r .account)
export SWIFT_URL_TEMP=$(openstack endpoint list -f json | jq -r '.[] | select((."Service Name"=="swift") and (."Interface"=="public")) | .URL')
export SWIFT_URL=$(echo $SWIFT_URL_TEMP | sed -r "s/AUTH_\%\(tenant_id\)s/$CONTAINER_TENANT_ID/g")
export TOKEN=$(openstack token issue -c id -f value)

ansible-playbook -i inventory.yaml openshift-install-prep.yaml
ansible-playbook -i inventory.yaml generate-ignition-files.yaml


openstack object create --name $INFRA_ID-bootstrap.ign $CONTAINER_NAME ../scripts/${INFRA_ID}.${DOMAIN_NAME}/final-bootstrap.ign

cat <<EOF > ../scripts/${INFRA_ID}.${DOMAIN_NAME}/$INFRA_ID-bootstrap-ignition.json
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
ansible-playbook -i inventory.yaml security-groups.yaml
ansible-playbook -i inventory.yaml ports-static.yaml
ansible-playbook -i inventory.yaml bootstrap.yaml
ansible-playbook -i inventory.yaml control-plane.yaml