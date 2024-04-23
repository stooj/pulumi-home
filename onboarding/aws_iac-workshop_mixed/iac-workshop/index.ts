import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";
import { Resource } from "@pulumi/aws/apigateway";

const bucket = new aws.s3.Bucket("my-website-bucket", {
    website: {
        indexDocument: "index.html",
    },
});

const publicAccessBlock = new aws.s3.BucketPublicAccessBlock(
    "public-access-block", {
        bucket: bucket.bucket,
        blockPublicPolicy: false,
    }
);

new aws.s3.BucketPolicy(
    "bucket-policy", {
        bucket: bucket.bucket,
        policy: pulumi.jsonStringify({
            Version: "2012-10-17",
            Statement: [{
                Effect: "Allow",
                Principal: "*",
                Action: ["s3:GetObject"],
                Resource: [
                    pulumi.interpolate`${bucket.arn}/*`,
                ],
            }]
        })
    }, {
        dependsOn: [publicAccessBlock],
});

new aws.s3.BucketObject(
    "index.html", {
        bucket: bucket,
        source: new pulumi.asset.FileAsset("www/index.html"),
        contentType: "text/html",
});

export const url = pulumi.interpolate`http://${bucket.websiteEndpoint}`;
