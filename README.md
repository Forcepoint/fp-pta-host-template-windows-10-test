# template-windows-10-test

This is a Packer process which creates a Windows 10 VM on a vSphere host.

## Notes

This process is inherently different than the template-centos-7-test packer process.
For the CentOS 7 template, the packer process creates the VM directly on the host running packer
using the 'vmware-iso' builder.
That works well, especially if you intend to keep the VM on the host running packer.
Contrary to that idea though, I wrote a post processor that then uploads the VM to vSphere.

The Windows 10 template here though does it differently with the 'vsphere-iso' builder.
Instead of building the VM locally, it builds it directly on the vsphere instance using API calls to
vSphere itself. The documentation says there's various options for getting the ISO, but since
this is Windows, and those ISOs aren't just floating around for anyone to download, I obtained one
with my MSDN account and uploaded it directly into the datastore for use with Packer, skipping
any download times. Believe me, the setup of Windows is long enough. No need to add more time to it
downloading the ISO from elsewhere.

On a related note, if you can have your vsphere admin mount an NFS fileshare as a datastore in vsphere,
you'll have a really easy way to dump new ISOs on your datastore via the fileshare. This is really helpful.

Personally, I like using the 'vsphere-iso' builder over the 'vmware-iso' builder for a number of reasons...

1. You don't need a beefy VM with hardware virtualization enabled to run Packer on. You can use a skimpy
system because all of the heavy lifting is done by vSphere.
1. You don't need a VMware Workstation license because you're not building the VM locally in VMware Workstation.
1. The overall packer process is shorter because you don't have to upload a VM to vSphere.
1. If your ISOs are on a datastore, you can run multiple packer processes against the same ISO without issue.
I think I've run about 6 Packer builds simultaneously against the same ISO and had no problems whatsoever.

The one caveat that I found to use 'vsphere-iso' is that it would only run properly for me against 
vSphere 6.7. I had to instead use 'vmware-iso' with vSphere 6.0 and 6.5.

Crafting the install process was a trial in frustration for a novice to Windows Unattended Installs.
The goal is always to get the system setup enough that it will Terraform properly (i.e. has VMware Tools installed)
and allow connections with Ansible for further configuration. Anything else that I found in examples for
running packer against Windows 10 I ripped out. It was too error prone and difficult and time consuming
to debug, including Windows Updates.

You may notice that I don't update the system with Windows Updates as part of this Packer process. This
goes contrary to many examples I saw online for Packer-izing Windows, but I found it wasted a ton of time.
Also, I could get around the need to run Windows Updates during Packer-izing if I just made sure I always 
updated the base ISO every 3 to 6 months with the latest one from Microsoft, 
which would have all the new updates baked in. The first thing I do with Ansible is run Windows Updates
anyways, so I'm not skipping out on Updates, just being choosy when I want them run. ~shrug~ I found
doing the updates with Ansible simpler too because of the well written ansible module to run them.

You may also notice that there's no place to specify your own Windows Key. That's because the Terraform
process is where the real key is applied. The one in the Autounattend.xml file is bogus and provided
by Microsoft for just this sort of scenario.

## Jenkins

You can run this packer process on your own machine if you want, but I don't see that as necessary.
I suggest waiting till you have your PTA Controller, Gitlab, and Artifactory instances setup to then 
run this through a job on the PTA Controller. 

## Useful Links

* https://packages.vmware.com/tools/releases/11.0.1/windows/

* https://www.vmware.com/pdf/vmware-tools-101-standalone-user-guide.pdf

* https://pubs.vmware.com/vsphere-50/index.jsp?topic=%2Fcom.vmware.vmtools.install.doc%2FGUID-CD6ED7DD-E2E2-48BC-A6B0-E0BB81E05FA3.html

* https://pubs.vmware.com/vsphere-50/index.jsp?topic=%2Fcom.vmware.vmtools.install.doc%2FGUID-E45C572D-6448-410F-BFA2-F729F2CDA8AC.html

* https://github.com/jetbrains-infra/packer-builder-vsphere

* https://docs.ansible.com/ansible/latest/user_guide/windows_setup.html#winrm-setup

* This is a fantastic guide to creating and validating your own windows answer file.
https://www.windowscentral.com/how-create-unattended-media-do-automated-installation-windows-10

* https://www.ivobeerens.nl/2019/09/09/vmware-tools-installation-and-upgrade-tips-and-tricks/

* https://packages.vmware.com/tools/versions
Helpful for figuring out which vmware tools version is compatible with your esxi version.