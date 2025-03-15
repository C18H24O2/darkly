#!/usr/bin/env bash

set -euo pipefail

ISO="Darkly.iso"

if [ ! -f "$ISO" ]; then
    echo "Downloading $ISO"
    curl -L -o "$ISO" https://cdn.intra.42.fr/isos/Darkly_i386.iso
fi

echo "Running VM"
VM_NAME="DARKLY_VM"
VBoxManage unregistervm "$VM_NAME" --delete || true
VBoxManage createvm --name "$VM_NAME" --register
VBoxManage modifyvm "$VM_NAME" --memory 2048 --cpus 2 --ostype Debian --nic1 nat --vram 64 --graphicscontroller vmsvga
VBoxManage storagectl "$VM_NAME" --name "IDE Controller" --add ide
VBoxManage storageattach "$VM_NAME" --storagectl "IDE Controller" --port 0 --device 0 --type dvddrive --medium "$ISO"
VBoxManage modifyvm "$VM_NAME" --nic1 bridged --bridgeadapter1 "${1:-eno2}"
VBoxManage startvm "$VM_NAME"
 
