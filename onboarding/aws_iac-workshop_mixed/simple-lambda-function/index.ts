import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

const role = new aws.iam.Role('my-function-role', {
    assumeRolePolicy: aws.iam.assumeRolePolicyForPrincipal({
        Service: "lambda.amazonaws.com"
    })
})

const lambdaFunction = new aws.lambda.Function('my-function', {
    role: role.arn,
    handler: "index.handler",
    // runtime: aws.lambda.NodeJS12dXRuntime,
    runtime: aws.lambda.Runtime.NodeJS18dX,
    code: new pulumi.asset.AssetArchive({
        "index.js": new pulumi.asset.StringAsset(
            "exports.handler = (e, c, cb) => cb(null, {statusCode: 200, body: 'Hello, world!'});",
        ),
    }),
})

export const functionName = lambdaFunction.name
