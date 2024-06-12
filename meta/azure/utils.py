from yaml import dump


# Generate Pulumi ESC YAML template
def create_yaml_structure(args):
    client_id, tenant_id, subscription_id = args
    return {
        "values": {
            "azure": {
                "login": {
                    "fn::open::azure-login": {
                        "clientId": client_id,
                        "tenantId": tenant_id,
                        "subscriptionId": subscription_id,
                        "oidc": True,
                    }
                }
            },
            "environmentVariables": {
                "ARM_USE_OIDC": "true",
                "ARM_CLIENT_ID": "${azure.login.clientId}",
                "ARM_TENANT_ID": "${azure.login.tenantId}",
                "ARM_OIDC_TOKEN": "${azure.login.oidc.token}",
                "ARM_SUBSCRIPTION_ID": "${azure.login.subscriptionId}",
            },
        }
    }


def generate_yaml(args):
    yaml_structure = create_yaml_structure(args)
    yaml_string = dump(yaml_structure, sort_keys=False)
    return yaml_string.rstrip()
