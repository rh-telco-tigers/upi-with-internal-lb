# Install: User Provided Infrastructure (UPI) with Internal Load Balancer
In this POC we are going to install Openshift with UPI (User Provided Infrastructure). The overall goal is to deploy HAProxy, Keepalived and Coredns inside the same cluster to avoid creating outside DNS entries and load balancers for control plane components. This will allow us to lessen our dependence on external load balancers while also minimizing the resource usage.
 
There are 3 separate way we are creating cluster to show the different use cases in this POC,

1. Create OpenShift on Openstack using Openstack as a targe platform: This approach automatically deploy these components (HAProxy, Keepalived, Coredns, and Mdns publisher) and manage those as a part of cluster's life cycle management. This is the only officially supported method when you create OCP on OSP. For this all you need to do is select openstack as your target platform when you create install config for the cluster. For example
```
platform:
  openstack:
    apiVIP: 10.0.0.5
    cloud: standalone
    computeFlavor: m1.large
    externalDNS: null
    externalNetwork: public
    ingressVIP: 10.0.0.7
    lbFloatingIP: 192.168.5.126
```

2. In the second method also we are using openstack but we set platform to none and manually install all of the components, including HAProxy, Keepalived, Coredns, and Mdns publisher. We create a custom ignition config file for the bootstrap and master node using this method. We're going to use the `filetranspiler` utility tool to produce the custom ignition config. 
```
platform:
  none: {}
```

3. The third option is very identical to the second, with the exception that we use VMware instead of OpenStack for infrastructure.

For installation instructions, go to the readme file in the corresponding platform folder.

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
