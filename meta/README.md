# Pulumi-home meta

Configures a working environment for pulumi support tasks

- [gcp/auth](###Auth)
- [gcp/projects](###Projects)
- [gcp/services](###Services)

## GCP

#### Auth

Creates OIDC configuration for authenticating with GCP using pulumi as an
identity provider. Creates a Pulumi ESC environment to integrate the OIDC into
other pulumi projects.

#### Projects

Creates an gcp project within the pulumi-ce organization to avoid breaking other
ppeople's stuff.

#### Services

Enables the gdrive_api_service on the project created in [Projects](#projects).

Currently you need to make the OAuth credentials by hand on the
[Credentials](https://console.cloud.google.com/apis/credentials?project=pulumi-ce-stoo)
page on Google Cloud. This is a limitation of Google's API, not Pulumi or
Terraform.
