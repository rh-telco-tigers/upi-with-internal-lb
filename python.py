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

keepalived_path = "../static-pod-resources/keepalived/keepalived.conf.tmpl"
if keepalived_path:
    with open(keepalived_path, 'r') as f:
        keepalived_conf = f.read().encode()
        keepalived_conf_b64 = base64.standard_b64encode(keepalived_conf).decode().strip()

    files.append(
    {
        'path': '/etc/kubernetes/static-pod-resources/keepalived/keepalived.conf.tmpl',
        'mode': 644,
        'user': {
            'name': 'root'
        },
        'contents': {
            'source': 'data:text/plain;charset=utf-8;base64,' + keepalived_conf_b64
        }
    })

haproxy_path = "../static-pod-resources/haproxy/haproxy.cfg.tmpl"
if haproxy_path:
    with open(haproxy_path, 'r') as f:
        haproxy_conf = f.read().encode()
        haproxy_conf_b64 = base64.standard_b64encode(haproxy_conf).decode().strip()

    files.append(
    {
        'path': '/etc/kubernetes/static-pod-resources/haproxy/haproxy.cfg.tmpl',
        'mode': 644,
        'user': {
            'name': 'root'
        },
        'contents': {
            'source': 'data:text/plain;charset=utf-8;base64,' + haproxy_conf_b64
        }
    })

mdns_path = "../static-pod-resources/mdns/config.hcl.tmpl"
if mdns_path:
    with open(mdns_path, 'r') as f:
        mdns_conf = f.read().encode()
        mdns_conf_b64 = base64.standard_b64encode(mdns_conf).decode().strip()

    files.append(
    {
        'path': '/etc/kubernetes/static-pod-resources/mdns/config.hcl.tmpl',
        'mode': 644,
        'user': {
            'name': 'root'
        },
        'contents': {
            'source': 'data:text/plain;charset=utf-8;base64,' + mdns_conf_b64
        }
    })


ignition['storage']['files'] = files;

with open('bootstrap.ign', 'w') as f:
    json.dump(ignition, f)