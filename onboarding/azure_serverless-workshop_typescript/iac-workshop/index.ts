import * as pulumi from "@pulumi/pulumi";
import * as resources from "@pulumi/azure-native/resources";
import * as storage from "@pulumi/azure-native/storage";

const resourceGroup = new resources.ResourceGroup("my-group", {
    resourceGroupName: "my-group",
    location: "westus",
});

const storageAccount = new storage.StorageAccount("mystorage", {
    resourceGroupName: resourceGroup.name,
    accountName: "c01ab8082e05",
    location: resourceGroup.location,
    sku: {
        name: "Standard_LRS",
    },
    kind: "StorageV2",
});

const container = new storage.BlobContainer("mycontainer", {
    resourceGroupName: resourceGroup.name,
    accountName: storageAccount.name,
    containerName: "files",
});

export const accountName = storageAccount.name;
