cd install-dir
export CONTAINER_NAME="ocp30-ignition"
export INFRA_ID=$(jq -r .infraID metadata.json)
ansible-playbook -i inventory.yaml down-bootstrap.yaml
ansible-playbook -i inventory.yaml down-control-plane.yaml
ansible-playbook -i inventory.yaml down-security-groups.yaml
ansible-playbook -i inventory.yaml down-ports.yaml
openstack object delete ${CONTAINER_NAME} ${INFRA_ID}-bootstrap.ign