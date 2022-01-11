cd install-dir
xargs -n 1 curl -O <<< '
        https://raw.githubusercontent.com/openshift/installer/release-4.6/upi/openstack/bootstrap.yaml
        https://raw.githubusercontent.com/openshift/installer/release-4.6/upi/openstack/common.yaml
        https://raw.githubusercontent.com/openshift/installer/release-4.6/upi/openstack/compute-nodes.yaml
        https://raw.githubusercontent.com/openshift/installer/release-4.6/upi/openstack/control-plane.yaml
        https://raw.githubusercontent.com/openshift/installer/release-4.6/upi/openstack/inventory.yaml
        https://raw.githubusercontent.com/openshift/installer/release-4.6/upi/openstack/network.yaml
        https://raw.githubusercontent.com/openshift/installer/release-4.6/upi/openstack/security-groups.yaml
        https://raw.githubusercontent.com/openshift/installer/release-4.6/upi/openstack/down-bootstrap.yaml
        https://raw.githubusercontent.com/openshift/installer/release-4.6/upi/openstack/down-compute-nodes.yaml
        https://raw.githubusercontent.com/openshift/installer/release-4.6/upi/openstack/down-control-plane.yaml
        https://raw.githubusercontent.com/openshift/installer/release-4.6/upi/openstack/down-load-balancers.yaml
        https://raw.githubusercontent.com/openshift/installer/release-4.6/upi/openstack/down-network.yaml
        https://raw.githubusercontent.com/openshift/installer/release-4.6/upi/openstack/down-security-groups.yaml
        https://raw.githubusercontent.com/openshift/installer/release-4.6/upi/openstack/down-containers.yaml'