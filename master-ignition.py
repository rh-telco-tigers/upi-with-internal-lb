for index in $(seq 0 2); do
    MASTER_HOSTNAME="$INFRA_ID-master-$index\n"
    python -c "import base64, json, sys;
ignition = json.load(sys.stdin);
storage = ignition.get('storage', {});
files = storage.get('files', []);

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

files.append({'path': '/etc/hostname', 'mode': 420, 'contents': {'source': 'data:text/plain;charset=utf-8;base64,' + base64.standard_b64encode(b'$MASTER_HOSTNAME').decode().strip(), 'verification': {}}, 'filesystem': 'root'});
storage['files'] = files;
ignition['storage'] = storage
json.dump(ignition, sys.stdout)" <master.ign >"$INFRA_ID-master-$index-ignition.json"
done