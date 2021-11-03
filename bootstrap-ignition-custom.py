import base64
import json
import os

with open('bootstrap.ign', 'r') as f:
    ignition = json.load(f)

files = ignition['storage'].get('files', [])

infra_id = os.environ.get('INFRA_ID', 'openshift').encode()
hostname_b64 = base64.standard_b64encode(infra_id + b'-bootstrap\n').decode().strip()
files.append(
{
    'path': '/etc/hostname',
    'mode': 420,
    'contents': {
        'source': 'data:text/plain;charset=utf-8;base64,' + hostname_b64
    }
})

ca_cert_path = os.environ.get('OS_CACERT', '')
if ca_cert_path:
    with open(ca_cert_path, 'r') as f:
        ca_cert = f.read().encode()
        ca_cert_b64 = base64.standard_b64encode(ca_cert).decode().strip()

    files.append(
    {
        'path': '/opt/openshift/tls/cloud-ca-cert.pem',
        'mode': 420,
        'contents': {
            'source': 'data:text/plain;charset=utf-8;base64,' + ca_cert_b64
        }
    })

keepalived_path = "/home/stack/ocp/4.6/upi-with-internal-lb/bootstrap/manifests/keepalived.yaml"
if keepalived_path:
    with open(keepalived_path, 'r') as f:
        keepalived_kubelet = f.read().encode()
        keepalived_kubelet_b64 = base64.standard_b64encode(keepalived_kubelet).decode().strip()

    files.append(
    {
        'path': '/etc/kubernetes/manifests/keepalived.yaml',
        'mode': 644,
        'contents': {
            'source': 'data:text/plain;charset=utf-8;base64,' + keepalived_kubelet_b64
        }
    })


coredns_path = "/home/stack/ocp/4.6/upi-with-internal-lb/bootstrap/manifests/coredns.yaml"
if coredns_path:
    with open(coredns_path, 'r') as f:
        coredns_kubelet = f.read().encode()
        coredns_kubelet_b64 = base64.standard_b64encode(coredns_kubelet).decode().strip()

    files.append(
    {
        'path': '/etc/kubernetes/manifests/coredns.yaml',
        'mode': 644,
        'contents': {
            'source': 'data:text/plain;charset=utf-8;base64,' + coredns_kubelet_b64
        }
    })

keepalived_conf_path = "/home/stack/ocp/4.6/upi-with-internal-lb/bootstrap/static-pod-resources/keepalived/keepalived.conf.tmpl"
if keepalived_conf_path:
    with open(keepalived_conf_path, 'r') as f:
        keepalived_conf = f.read().encode()
        keepalived_conf_b64 = base64.standard_b64encode(keepalived_conf).decode().strip()

    files.append(
    {
        'path': '/etc/kubernetes/static-pod-resources/keepalived/keepalived.conf.tmpl',
        'mode': 644,
        'contents': {
            'source': 'data:text/plain;charset=utf-8;base64,' + keepalived_conf_b64
        }
    })

coredns_conf_path = "/home/stack/ocp/4.6/upi-with-internal-lb/bootstrap/static-pod-resources/Corefile.tmpl"
if coredns_conf_path:
    with open(coredns_conf_path, 'r') as f:
        coredns_conf = f.read().encode()
        coredns_conf_b64 = base64.standard_b64encode(coredns_conf).decode().strip()

    files.append(
    {
        'path': '/etc/kubernetes/static-pod-resources/coredns/Corefile.tmpl',
        'mode': 644,
        'contents': {
            'source': 'data:text/plain;charset=utf-8;base64,' + coredns_conf_b64
        }
    })


ignition['storage']['files'] = files;

with open('bootstrap.ign', 'w') as f:
    json.dump(ignition, f)