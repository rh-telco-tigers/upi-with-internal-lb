export INFRA_ID=$(jq -r .infraID install-dir/metadata.json)
python _bootstrap-ignition.py
