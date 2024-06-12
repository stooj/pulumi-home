import getpass

import pulumi
import pulumi_pulumiservice as pulumiservice
from pulumi_gcp import iam, organizations, projects, serviceaccount

from . import utils

issuer = "https://api.pulumi.com/oidc"

# Retrieve local Pulumi configuration
pulumi_config = pulumi.Config()
audience = pulumi.get_organization()

# Retrieve project details
project_config = organizations.get_project()
project_id = project_config.number

# Retrieve current user details
username = getpass.getuser()

# Create a Workload Identity Pool
identity_pool = iam.WorkloadIdentityPool(
    "pulumiOidcWorkloadIdentityPool",
    workload_identity_pool_id=f"pulumi-oidc-identity-pool-{username}",
    description="Pulumi OIDC Workload Identity Pool",
    display_name="Pulumi OIDC Identity Pool",
)


# Create a Workload Identity Provider
identity_provider = iam.WorkloadIdentityPoolProvider(
    "pulumiOidcIdentityProvider",
    workload_identity_pool_id=identity_pool.workload_identity_pool_id,
    workload_identity_pool_provider_id=f"pulumi-oidc-provider-{username}",
    attribute_mapping={
        "google.subject": "assertion.sub",
    },
    oidc=iam.WorkloadIdentityPoolProviderOidcArgs(
        issuer_uri=issuer, allowed_audiences=[audience]
    ),
)

# Create a service account
service_account = serviceaccount.Account(
    "serviceAccount",
    account_id=f"pulumi-oidc-service-acct-{username}",
    display_name="Pulumi OIDC Service Account",
)

# Grant the service account 'roles/editor' on the project
editor_policy_binding = projects.IAMMember(
    "editorIamBinding",
    member=service_account.email.apply(lambda email: f"serviceAccount:{email}"),
    role="roles/editor",
    project=project_id,
)

# Allow the workload identity pool to impersonate the service account
iam_policy_binding = serviceaccount.IAMBinding(
    "iamPolicyBinding",
    service_account_id=service_account.name,
    role="roles/iam.workloadIdentityUser",
    members=identity_pool.name.apply(
        lambda name: [f"principalSet://iam.googleapis.com/{name}/*"]
    ),
)

# Create an environment for oidc authentication
gcp_oidc_env = pulumiservice.Environment(
    "pulumi-support-oidc-gcp",
    name="pulumi-support-oidc-gcp",
    organization=audience,
    opts=pulumi.ResourceOptions(
        parent=identity_provider, depends_on=[identity_provider]
    ),
    yaml=(
        pulumi.Output.all(
            project_id,
            identity_provider.workload_identity_pool_id,
            identity_provider.workload_identity_pool_provider_id,
            service_account.email,
        )
        .apply(utils.generate_yaml)
        .apply(pulumi.StringAsset)
    ),
)

prompt = """
    To use oidc with gcp, add the environment to your pulumi configuration with:
        `pulumi config env add {}`
    """
gcp_oidc_env.name.apply(lambda name: print(prompt.format(name)))
