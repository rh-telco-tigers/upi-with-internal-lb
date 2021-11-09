export INFRA_ID=$(jq -r .infraID install-dir/metadata.json)
python _bootstrap-ignition.py
filetranspile -i install-dir/bootstrap.ign -f bootstrap/fakeroot -o install-dir/custom-bootstrap.ign