"""An AWS Python Pulumi program"""

import pulumi
import pulumi_aws as aws

ami = aws.ec2.get_ami(
    most_recent="true",
    owners=["amazon"],
    filters=[{"name": "name", "values": ["amzn2-ami-hvm-*-x86_64-gp2"]}],
)

vpc = aws.ec2.get_vpc(default=True)

group = aws.ec2.SecurityGroup(
    "web-secgrp",
    description="Enable HTTP access",
    vpc_id=vpc.id,
    ingress=[
        {
            "protocol": "icmp",
            "from_port": 8,
            "to_port": 0,
            "cidr_blocks": ["0.0.0.0/0"],
        },
        {
            "protocol": "tcp",
            "from_port": 80,
            "to_port": 80,
            "cidr_blocks": ["0.0.0.0/0"],
        },
    ],
)

USER_DATA = """
#!/bin/bash
echo "Hello, World!" > index.html
nohup python -m SimpleHTTPServer 80 &
"""

ips = []
hostnames = []

for az in aws.get_availability_zones().names:
    server = aws.ec2.Instance(
            
            f'web-server-{az}',
            instance_type="t2.micro",
            vpc_security_group_ids=[group.id],
            ami=ami.id,
            availability_zone=az,
            user_data=USER_DATA,
            tags={
                "Name": "web-server",
            },
    )
    ips.append(server.public_ip)
    hostnames.append(server.public_dns)

pulumi.export("ips", ips)
pulumi.export("hostnames", hostnames)
