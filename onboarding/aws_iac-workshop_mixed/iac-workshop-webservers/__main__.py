"""An AWS Python Pulumi program"""

import pulumi
import pulumi_aws as aws


ami = aws.ec2.get_ami(
    most_recent="true",
    owners=["amazon"],
    filters=[{"name": "name", "values": ["amzn2-ami-hvm-*-x86_64-gp2"]}],
)

vpc = aws.ec2.get_vpc(default=True)
vpc_subnets = aws.ec2.get_subnets(
    filters=[
        aws.ec2.GetSubnetsFilterArgs(
            name="vpc-id",
            values=[vpc.id],
        )
    ]
)

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
    egress=[
        {
            "protocol": "tcp",
            "from_port": 80,
            "to_port": 80,
            "cidr_blocks": ["0.0.0.0/0"],
        }
    ],
)

lb = aws.lb.LoadBalancer(
    "loadbalancer",
    internal=False,
    security_groups=[group.id],
    subnets=vpc_subnets.ids,
    load_balancer_type="application",
)

target_group = aws.lb.TargetGroup(
    "target-group", port=80, protocol="HTTP", target_type="ip", vpc_id=vpc.id
)

listener = aws.lb.Listener(
    "listener",
    load_balancer_arn=lb.arn,
    port=80,
    default_actions=[{"type": "forward", "target_group_arn": target_group.arn}],
)

USER_DATA = """
#!/bin/bash
echo \"Hello, World -- from {}!\" > index.html
nohup python -m SimpleHTTPServer 80 &
"""

ips = []
hostnames = []

for az in aws.get_availability_zones().names:
    server = aws.ec2.Instance(
        f"web-server-{az}",
        instance_type="t2.micro",
        vpc_security_group_ids=[group.id],
        ami=ami.id,
        user_data=USER_DATA.format(az),
        availability_zone=az,
        tags={
            "Name": "web-server",
        },
    )
    ips.append(server.public_ip)
    hostnames.append(server.public_dns)

    attachment = aws.lb.TargetGroupAttachment(
        f"web-server-{az}",
        target_group_arn=target_group.arn,
        target_id=server.private_ip,
        port=80,
    )

pulumi.export("ips", ips)
pulumi.export("hostnames", hostnames)
pulumi.export("url", lb.dns_name)
