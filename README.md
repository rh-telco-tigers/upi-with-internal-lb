# upi-with-internal-lb
Installing Openshift with UPI and an internal load balancer. For installation instructions, go to the readme file in the corresponding platform folder.

# Some Handy-commands for reference
```
export OS_CLOUD="standalone"
export INFRA_ID=$(jq -r .infraID metadata.json)
openstack quota set --secgroups 300 --secgroup-rules 1000 admin
openstack console log show "$INFRA_ID-bootstrap"
openshift-install wait-for bootstrap-complete
openstack token issue -c id -f value
openstack catalog show image
openstack image show ocp-4.9-bootstrap.ign
```


## Creating Ignition file with filetranspiler tool
We can also use the filetranspiler tool for creating custom ignition files. This tool creates an Ignition file from a fake root. To install this tool please follow [this URL](https://github.com/ashcrow/filetranspiler).

You can also get ROM version from [here](https://download.copr.fedorainfracloud.org/results/eminguez/eminguez-RPMs/fedora-33-x86_64/01784152-filetranspiler/filetranspiler-1.1.0-1.fc33.x86_64.rpm)

Once you have installed this tool create a fakeroot directory. See example below
```
#tree fakeroot
fakeroot
└── etc
    └── kubernetes
        ├── manifests
        │   ├── coredns.yaml
        │   ├── haproxy.yaml
        │   ├── keepalived.yaml
        │   └── mdns-publisher.yaml
        └── static-pod-resources
            ├── coredns
            │   └── Corefile.tmpl
            ├── haproxy
            │   └── haproxy.cfg.tmpl
            ├── keepalived
            │   ├── keepalived.conf.tmpl
            │   └── scripts
            │       ├── chk_ocp_script_both.sh.tmpl
            │       └── chk_ocp_script.sh.tmpl
            └── mdns
                └── config.hcl.tmpl
```
Once your directory structure in place then use filetranspiler binary to create your custom ignition.
```
#filetranspile --help
usage: filetranspile [-h] [-i IGNITION] -f FAKE_ROOT [-o OUTPUT] [-p]
                     [--dereference-symlinks] [--format {json,yaml}]
                     [--version]

optional arguments:
  -h, --help            show this help message and exit
  -i IGNITION, --ignition IGNITION
                        Path to ignition file to use as the base
  -f FAKE_ROOT, --fake-root FAKE_ROOT
                        Path to the fake root
  -o OUTPUT, --output OUTPUT
                        Where to output the file. If empty, will print to
                        stdout
  -p, --pretty          Make the output pretty
  --dereference-symlinks
                        Write out file contents instead of making symlinks
                        NOTE: Target files must exist in the fakeroot
  --format {json,yaml}  What format of file to write out. `yaml` or `json`
                        (default)
  --version             show program's version number and exit
 
 #filetranspile -i ignition.json -f fakeroot -o custom-ignition.ign
 ```
 If you want to see a pretty output on screen use following command
 ```
 #filetranspile -i ignition.json -f fakeroot -p
 ```
