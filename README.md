Simple AWS
==========
Simple AWS is intended as a collection of scripts to easily show and do SSH
connections to OpsWorks and EC2 machines under OS X.

Usage
-----
Configure your AWS settings as of config.yml instructions

Run "python main.py" with the following arguments:
 -c path to config.yml
 -l OpsWorks Layer ID (optional if set on config.yml)
 --offline show offline instances (optional, default=False)