export INFRA_ID=$(jq -r .infraID install-dir/metadata.json)
IGNITION_FILE=$(openstack image create --disk-format=raw --container-format=bare --file install-dir/bootstrap.ign ocp-$INFRA_ID-bootstrap.ign -f json | jq -r .file)
GLANCE_URL=$(openstack catalog show image -f json | jq -r .endpoints[0].url)
TOKEN=$(openstack token issue -c id -f value)

cat <<EOF > install-dir/$INFRA_ID-bootstrap-ignition.json
{
  "ignition": {
    "config": {
      "merge": [{
        "source": "${GLANCE_URL}${IGNITION_FILE}", 
        "httpHeaders": [{
          "name": "X-Auth-Token", 
          "value": "${TOKEN}" 
        }]
      }]
    },
    "version": "3.1.0"
  }
}
EOF