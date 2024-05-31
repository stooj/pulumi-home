import pulumi_gcp as gcp

gdrive_service = gcp.projects.Service(
    "gdrive_api_service",
    project="pulumi-ce-stoo",
    service="drive.googleapis.com",
    disable_dependent_services=True,
)

# Create a new Service Account
# service_account = gcp.serviceaccount.Account("gdrive_service_account",
#     account_id="stooj-gdrive-rsync-account",
#     display_name="GDrive rsync for stooj")

# Create a new key for the Service Account, which can be used as OAuth credentials
# service_account_key = gcp.serviceaccount.Key(
#     "gdrive_service_account_key",
#     project=stoo_project.name,
#     service_account_id=service_account.name,
#     public_key_type="TYPE_X509_PEM_FILE",
#     private_key_type="TYPE_GOOGLE_CREDENTIALS_FILE")

# Export the email and the private key of the service account
# pulumi.export("service_account_email", service_account.email)
# pulumi.export("service_account_private_key", service_account_key.private_key)
