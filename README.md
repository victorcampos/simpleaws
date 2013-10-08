Simple AWS
==========
Simple AWS is a little collection of tools to easily:

 * list OpsWorks instances in a layer and start an ssh session
 * search and list EC2 instances by name and start an ssh session

I've started this project to minimize time spent searching for problematic
instances on AWS Console, grabbing the public DNS and ssh'ing.

Usage
-----
Configure your AWS settings as of config.yml instructions

Run "python main.py" with the following arguments:

 * -c path to config.yml
 * -l OpsWorks Layer ID (optional if set on config.yml)
 * --offline show offline instances (optional, default=False)
 * *ec2* for EC2 search functions or *opsworks* for... OpsWorks

> usage: main.py [-h] -c CONFIG_PATH [-l LAYER_ID] [--offline OFFLINE]  
>               {ec2,opsworks}  
>
> Connect to OpsWorks instances.  
>
> positional arguments:  
>  {ec2,opsworks}        service to connect  
>
> optional arguments:  
>  -h, --help            show this help message and exit  
>  -c CONFIG_PATH, --config CONFIG_PATH  
>                        path to configuration file  
>  -l LAYER_ID, --layer LAYER_ID  
>                        layer id to search for instances if different from  
>                        specified in config.yml  
>  --offline OFFLINE     return offline instances?