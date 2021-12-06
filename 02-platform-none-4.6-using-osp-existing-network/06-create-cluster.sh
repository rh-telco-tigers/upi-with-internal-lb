export INFRA_ID=$(jq -r .infraID install-dir/metadata.json)

cd install-dir
ansible-playbook -i inventory.yaml bootstrap.yaml
ansible-playbook -i inventory.yaml control-plane.yaml