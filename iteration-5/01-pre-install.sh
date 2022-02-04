cd install-dir
ansible-playbook -i inventory.yaml openshift-install-prep.yaml
ansible-playbook -i inventory.yaml generate-ignition-files.yaml
