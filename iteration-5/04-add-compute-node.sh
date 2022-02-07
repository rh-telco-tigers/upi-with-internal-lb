export INFRA_ID=$(yq -r .all.hosts.localhost.cluster_name install-dir/inventory.yaml)

cd install-dir
ansible-playbook -i inventory.yaml compute-nodes.yaml 
oc get csr -o name | xargs oc adm certificate approve