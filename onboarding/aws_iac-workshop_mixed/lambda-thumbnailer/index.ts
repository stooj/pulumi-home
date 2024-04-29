import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";
import * as awsx from "@pulumi/awsx";

const image = awsx.classic.ecr.buildAndPushImage("thumbnailer", {
    context: "./app",
});
