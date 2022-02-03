cd install-dir
export CONTAINER_NAME=$(yq -r .all.hosts.localhost.swift_container_name install-dir/inventory.yaml)
export INFRA_ID=$(yq -r .all.hosts.localhost.cluster_name install-dir/inventory.yaml)
ansible-playbook -i inventory.yaml down-bootstrap.yaml
ansible-playbook -i inventory.yaml down-control-plane.yaml
ansible-playbook -i inventory.yaml down-security-groups.yaml
ansible-playbook -i inventory.yaml down-ports.yaml
openstack object delete ${CONTAINER_NAME} ${INFRA_ID}-bootstrap.ign