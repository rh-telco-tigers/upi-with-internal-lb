export INFRA_ID=$(jq -r .infraID install-dir/metadata.json)
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