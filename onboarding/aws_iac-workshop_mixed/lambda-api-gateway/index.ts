import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";
import * as awsx from "@pulumi/awsx";

const api = new awsx.classic.apigateway.API("hello-world", {
    routes: [{
        path: "/",
        method: "GET",
        eventHandler: async (event) => {
            return {
                statusCode: 200,
                body: "Hello, world!",
            };
        },
    },
        {
            path: "encode",
            method: "POST",
            eventHandler: async (event) => {
                console.log("request: " + JSON.stringify(event));
                let body: string
                let responseCode: number

                if (event.body != null) {
                    if (event.isBase64Encoded) {
                        body = event.body // API gateway will base64 encode for us
                        responseCode = 200
                    } else {
                        body = Buffer.from(event.body).toString('base64')
                        responseCode = 200
                    }
                } else {
                    body = "No data submitted"
                    responseCode = 400
                }

                return {
                    statusCode: responseCode,
                    body: body,
                }
            },
        }],
})

export const url = api.url;
