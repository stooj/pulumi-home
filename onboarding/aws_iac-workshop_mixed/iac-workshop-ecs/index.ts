import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";
import * as awsx from "@pulumi/awsx";

const vpc = new awsx.ec2.Vpc(
    "vpc", {
    natGateways: {
        strategy: awsx.ec2.NatGatewayStrategy.Single,
    }
});

const cluster = new aws.ecs.Cluster("cluster");

const group = new aws.ec2.SecurityGroup(
    "web-secgrp", {
    vpcId: vpc.vpcId,
    description: "Enable HTTP access",
    ingress: [{
        protocol: "tcp",
        fromPort: 80,
        toPort: 80,
        cidrBlocks: ["0.0.0.0/0"],
    }],
    egress: [{
        protocol: "-1",
        fromPort: 0,
        toPort: 0,
        cidrBlocks: ["0.0.0.0/0"],
    }]
});

const alb = new aws.lb.LoadBalancer(
    "app-lb", {
    securityGroups: [group.id],
    subnets: vpc.publicSubnetIds,
});

const targetGroup = new aws.lb.TargetGroup(
    "app-tg", {
    port: 80,
    protocol: "HTTP",
    targetType: "ip",
    vpcId: vpc.vpcId,
});

const listener = new aws.lb.Listener(
    "web", {
    loadBalancerArn: alb.arn,
    port: 80,
    defaultActions: [{
        type: "forward",
        targetGroupArn: targetGroup.arn,
    }],
});
