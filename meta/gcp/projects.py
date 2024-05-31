import pulumi
import pulumi_gcp as gcp

config = pulumi.Config()
org_id = config.get("gcp_organization")

stoo_project = gcp.organizations.Project(
    "stoo_project",
    name="Stoo's playground project",
    project_id="pulumi-ce-stoo",
    org_id=org_id,
)
