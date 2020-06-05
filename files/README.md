# files

I tried mucking around with the Autounattend.xml file to install certificates, but found it wasn't
a trivial affair. Instead, I found it easier to install certificates with a Packer provisioner.
If you add said files to this folder, you can easily add provisioners to apply them to your VM.
Packer hasn't figured out how to add comments easily to the packer json files, 
so here's some example code for you...

    "provisioners": [
      {
        "type": "file",
        "source": "./files/internal_ca.cer",
        "destination": "C:\\Windows\\internal_ca.cer"
      },
      {
        "type": "powershell",
        "inline": ["Import-Certificate -CertStoreLocation cert:\\LocalMachine\\Root -FilePath 'C:\\Windows\\internal_ca.cer'"]
      }
    ]
