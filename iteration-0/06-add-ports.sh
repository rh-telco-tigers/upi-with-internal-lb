export INFRA_ID=$(jq -r .infraID metadata.json)
openstack server add port $INFRA_ID-master-0 public-$INFRA_ID-master-port-0
openstack server add port $INFRA_ID-master-0 management-$INFRA_ID-master-port-0 
openstack server add port $INFRA_ID-master-0 outbound-$INFRA_ID-master-port-0 

openstack server add port $INFRA_ID-master-1 public-$INFRA_ID-master-port-1
openstack server add port $INFRA_ID-master-1 management-$INFRA_ID-master-port-1
openstack server add port $INFRA_ID-master-1 outbound-$INFRA_ID-master-port-1

openstack server add port $INFRA_ID-master-2 public-$INFRA_ID-master-port-2
openstack server add port $INFRA_ID-master-2 management-$INFRA_ID-master-port-2
openstack server add port $INFRA_ID-master-2 outbound-$INFRA_ID-master-port-2
