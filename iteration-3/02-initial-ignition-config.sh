OPENSHIFT_INSTALL_CMD="./scripts/openshift-install"
${OPENSHIFT_INSTALL_CMD} create manifests --dir=install-dir
${OPENSHIFT_INSTALL_CMD} create ignition-configs --dir=install-dir 
