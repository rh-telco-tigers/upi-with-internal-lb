cd install-dir
ansible-playbook -i inventory.yaml down-bootstrap.yaml
ansible-playbook -i inventory.yaml down-control-plane.yaml
ansible-playbook -i inventory.yaml security-groups.yaml
