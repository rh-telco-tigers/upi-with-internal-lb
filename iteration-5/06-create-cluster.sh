export INFRA_ID=$(yq -r .all.hosts.localhost.cluster_name install-dir/inventory.yaml)

cd install-dir
ansible-playbook -i inventory.yaml security-groups.yaml
ansible-playbook -i inventory.yaml ports.yaml
ansible-playbook -i inventory.yaml bootstrap.yaml
ansible-playbook -i inventory.yaml control-plane.yaml