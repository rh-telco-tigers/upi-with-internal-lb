export INFRA_ID=$(jq -r .infraID install-dir/metadata.json)

for index in $(seq 0 2); do
    MASTER_HOSTNAME="$INFRA_ID-master-$index\n"
    python -c "import base64, json, sys;
ignition = json.load(sys.stdin);
storage = ignition.get('storage', {});
files = storage.get('files', []);
files.append({'path': '/etc/hostname', 'mode': 420, 'contents': {'source': 'data:text/plain;charset=utf-8;base64,' + base64.standard_b64encode(b'$MASTER_HOSTNAME').decode().strip(), 'verification': {}}, 'filesystem': 'root'});
files.append({'path': '/etc/mdns/hostname', 'mode': 420, 'contents': {'source': 'data:text/plain;charset=utf-8;base64,' + base64.standard_b64encode(b'$MASTER_HOSTNAME').decode().strip(), 'verification': {}}, 'filesystem': 'root'});
storage['files'] = files;
ignition['storage'] = storage
json.dump(ignition, sys.stdout)" <install-dir/master.ign > "install-dir/$INFRA_ID-master-$index-ignition.json"

done

docker run --rm -ti --volume `pwd`:/srv:z filetranspile:latest -i install-dir/$INFRA_ID-master-0-ignition.json -f master0/fakeroot  -o install-dir/$INFRA_ID-master-0-ignition.json
docker run --rm -ti --volume `pwd`:/srv:z filetranspile:latest -i install-dir/$INFRA_ID-master-1-ignition.json -f master1/fakeroot  -o install-dir/$INFRA_ID-master-1-ignition.json
docker run --rm -ti --volume `pwd`:/srv:z filetranspile:latest -i install-dir/$INFRA_ID-master-2-ignition.json -f master2/fakeroot  -o install-dir/$INFRA_ID-master-2-ignition.json
