import { Config } from "@pulumi/pulumi";

const config = new Config();
export const containerName = config.require("container");
export const account = config.require("account");
export const resourceGroupName = config.require("resourceGroup");
