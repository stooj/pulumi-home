import getpass

import pulumi
import pulumi_pulumiservice as pulumiservice
from pulumi_azure_native import authorization

from . import utils

# Retrieve current user details
username = getpass.getuser()

issuer = "https://api.pulumi.com/oidc"

# Retrieve local Pulumi configuration
pulumi_config = pulumi.Config()
audience = pulumi.get_organization()
# env_name = pulumi_config.require("environmentName")

# Retrieve local Azure configuration
azure_config = authorization.get_client_config()
az_subscription = azure_config.subscription_id
tenant_id = azure_config.tenant_id

# Create a Microsoft Entra Application
# application = azuread.Application(
#     f"pulumi-oidc-app-reg-{username}",
#     owners=[azure_config.object_id],
#     display_name=f"pulumi-oidc-app-reg-{username}",
#     sign_in_audience="AzureADMyOrg",
# )

# Create Federated Credentials
# subject = f"pulumi:environments:org:{audience}:env:{env_name}"
"""
Defining a subject identifier using a specific environment
name is not currently supported at this time.
There is a known issue with the value of the subject
identifier that is sent to Azure from Pulumi. The subject 
identifier used below is what you need to provide
to configure OIDC for Pulumi ESC.

See: https://github.com/pulumi/pulumi/issues/14509
"""
# subject = f"pulumi:environments:org:{audience}:env:<yaml>"

# federated_identity_credential = azuread.ApplicationFederatedIdentityCredential(
#     f"oidcFederatedIdentityCredential{username.title()}",
#     application_id=application.object_id.apply(
#         lambda object_id: f"/applications/{object_id}"
#     ),
#     display_name=f"pulumi-env-oidc-fic-{username}",
#     description="Federated credentials for Pulumi ESC",
#     audiences=[audience],
#     issuer=issuer,
#     subject=subject,
# )

# Create a Service Principal
# service_principal = azuread.ServicePrincipal(
#     f"oidc-service-principal-{username}", client_id=application.client_id
# )

# Assign the 'Contributor' role to the Service principal at the scope specified
# CONTRIBUTOR = f"/subscriptions/{az_subscription}/providers/Microsoft.Authorization/roleDefinitions/b24988ac-6180-42a0-ab88-20f7382dd24c"

# role_assignment = authorization.RoleAssignment(
#     f"oidc-role-assignment-{username}",
#     role_definition_id=CONTRIBUTOR,
#     principal_id=service_principal.id,
#     principal_type="ServicePrincipal",
#     scope=f"/subscriptions/{az_subscription}",
# )

#
# pulumi.Output.all(application.client_id, tenant_id, az_subscription).apply(print_yaml)


"""
Pulumi already has OIDC set up for the org, and you need admin permissions to
make a parallel configuration, so I'm skipping the actual OIDC creation step and
just configuring the environment.
"""

# yaml = utils.generate_yaml(client_id, tenant_id, az_subscription)
# # Create an environment for oidc authentication
# azure_oidc_env = pulumiservice.Environment(
#     "pulumi-support-oidc-azure",
#     name="pulumi-support-oidc-gcp",
#     organization=audience,
#     yaml=pulumi.StringAsset(yaml),
# )
