from yaml import dump


# Generate Pulumi ESC YAML template
def create_yaml_structure(args):
    gcp_project, workload_pool_id, provider_id, service_account_email = args
    return {
        "values": {
            "login": {
                "fn::open::gcp-login": {
                    "project": int(gcp_project),
                    "oidc": {
                        "workloadPoolId": workload_pool_id,
                        "providerId": provider_id,
                        "serviceAccount": service_account_email,
                    },
                }
            }
        },
        "environmentVariables": {
            "GOOGLE_PROJECT": "${gcp.login.project}",
            "CLOUDSDK_AUTH_ACCESS_TOKEN": "${gcp.login.accessToken}",
        },
    }


def generate_yaml(args):
    yaml_structure = create_yaml_structure(args)
    yaml_string = dump(yaml_structure, sort_keys=False)
    return yaml_string.rstrip()
