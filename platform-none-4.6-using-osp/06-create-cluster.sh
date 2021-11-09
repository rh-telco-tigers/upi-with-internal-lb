export INFRA_ID=$(jq -r .infraID install-dir/metadata.json)

cd install-dir
ansible-playbook -i inventory.yaml security-groups.yaml
ansible-playbook -i inventory.yaml network.yaml

openstack subnet set --dns-nameserver 8.8.8.8 ${INFRA_ID}-nodes
openstack subnet set --dns-nameserver 10.0.0.5 ${INFRA_ID}-nodes

ansible-playbook -i inventory.yaml bootstrap.yaml
ansible-playbook -i inventory.yaml control-plane.yaml