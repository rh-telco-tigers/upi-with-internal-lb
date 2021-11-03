import base64
import json
import os
import sys

master_ignition_file = os.environ.get('MASTER_IGNITION_FILE', '')
with open(master_ignition_file, 'r') as f:
    ignition = json.load(f)

files = ignition['storage'].get('files', [])

keepalived_path = "/home/stack/ocp/4.6/upi-with-internal-lb/master2/manifests/keepalived.yaml"
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

keepalived_conf_path = "/home/stack/ocp/4.6/upi-with-internal-lb/master2/static-pod-resources/keepalived/keepalived.conf.tmpl"
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

keepalived_script1_path = "/home/stack/ocp/4.6/upi-with-internal-lb/master2/static-pod-resources/keepalived/scripts/chk_ocp_script.sh.tmpl"
if keepalived_script1_path:
    with open(keepalived_script1_path, 'r') as f:
        keepalived_script1 = f.read().encode()
        keepalived_script1_b64 = base64.standard_b64encode(keepalived_script1).decode().strip()

    files.append(
    {
        'path': '/etc/kubernetes/static-pod-resources/keepalived/scripts/chk_ocp_script.sh.tmpl',
        'mode': 644,
        'contents': {
            'source': 'data:text/plain;charset=utf-8;base64,' + keepalived_script1_b64
        }
    })

keepalived_script2_path = "/home/stack/ocp/4.6/upi-with-internal-lb/master2/static-pod-resources/keepalived/scripts/chk_ocp_script_both.sh.tmpl"
if keepalived_script2_path:
    with open(keepalived_script2_path, 'r') as f:
        keepalived_script2 = f.read().encode()
        keepalived_script2_b64 = base64.standard_b64encode(keepalived_script2).decode().strip()

    files.append(
    {
        'path': '/etc/kubernetes/static-pod-resources/keepalived/scripts/chk_ocp_script.sh.tmpl',
        'mode': 644,
        'contents': {
            'source': 'data:text/plain;charset=utf-8;base64,' + keepalived_script2_b64
        }
    })

haproxy_path = "/home/stack/ocp/4.6/upi-with-internal-lb/master2/manifests/haproxy.yaml"
if haproxy_path:
    with open(haproxy_path, 'r') as f:
        haproxy_kubelet = f.read().encode()
        haproxy_kubelet_b64 = base64.standard_b64encode(haproxy_kubelet).decode().strip()

    files.append(
    {
        'path': '/etc/kubernetes/manifests/haproxy.yaml',
        'mode': 644,
        'contents': {
            'source': 'data:text/plain;charset=utf-8;base64,' + haproxy_kubelet_b64
        }
    })

haproxy_conf_path = "/home/stack/ocp/4.6/upi-with-internal-lb/master2/static-pod-resources/haproxy/haproxy.cfg.tmpl"
if haproxy_conf_path:
    with open(haproxy_conf_path, 'r') as f:
        haproxy_conf = f.read().encode()
        haproxy_conf_b64 = base64.standard_b64encode(haproxy_conf).decode().strip()

    files.append(
    {
        'path': '/etc/kubernetes/static-pod-resources/haproxy/haproxy.cfg.tmpl',
        'mode': 644,
        'contents': {
            'source': 'data:text/plain;charset=utf-8;base64,' + haproxy_conf_b64
        }
    })

mdns_path = "/home/stack/ocp/4.6/upi-with-internal-lb/master2/manifests/mdns-publisher.yaml"
if mdns_path:
    with open(mdns_path, 'r') as f:
        mdns_kubelet = f.read().encode()
        mdns_kubelet_b64 = base64.standard_b64encode(mdns_kubelet).decode().strip()

    files.append(
    {
        'path': '/etc/kubernetes/manifests/mdns-publisher.yaml',
        'mode': 644,
        'contents': {
            'source': 'data:text/plain;charset=utf-8;base64,' + mdns_kubelet_b64
        }
    })

mdns_conf_path = "/home/stack/ocp/4.6/upi-with-internal-lb/master2/static-pod-resources/mdns/config.hcl.tmpl"
if mdns_conf_path:
    with open(mdns_conf_path, 'r') as f:
        mdns_conf = f.read().encode()
        mdns_conf_b64 = base64.standard_b64encode(mdns_conf).decode().strip()

    files.append(
    {
        'path': '/etc/kubernetes/static-pod-resources/mdns/config.hcl.tmpl',
        'mode': 644,
        'contents': {
            'source': 'data:text/plain;charset=utf-8;base64,' + mdns_conf_b64
        }
    })


coredns_path = "/home/stack/ocp/4.6/upi-with-internal-lb/master2/manifests/coredns.yaml"
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

coredns_conf_path = "/home/stack/ocp/4.6/upi-with-internal-lb/master2/static-pod-resources/coredns/Corefile.tmpl"
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

with open(master_ignition_file, 'w') as f:
    json.dump(ignition, f)
