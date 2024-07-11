import getpass

import pulumi
import pulumi_azure_native as azure_native
import pulumi_command as command

# Retrieve current user details
username = getpass.getuser()

# elevate = command.local.Command(
#     "elevate-admin-permissions",
#     create='az rest --method post --url "/providers/Microsoft.Authorization/elevateAccess?api-version=2016-07-01"',
# )

# Permissions required for adding subscription to a management group, assigned to the service principal, in the remote subscription
# perm: "Microsoft.Authorization/roleAssignments/write" # required to add subscription to management group
# perm: "Microsoft.Authorization/roleAssignments/delete" # required to add subscription to management group
# perm: "Microsoft.Authorization/roleAssignments/read" # required to add subscription to management group
# perm: "Microsoft.Management/managementGroups/*" # required to add subscription to management group - trial and error, could be more granular

management_group_user = azure_native.management.ManagementGroup(
    f"managementGroup{username.title()}",
    display_name=f"ManagementGroup{username.title()}",
    group_id=f"ManagementGroup{username.title()}",
    # opts=pulumi.ResourceOptions(depends_on=[elevate]),
)

subscription = azure_native.management.ManagementGroupSubscription(
    f"managementGroupSubscription{username.title()}",
    group_id=management_group_user.id,
)
# deelevate = command.local.Command(
#     "remove-admin-permissions",
#     create='az role assignment delete --role "User Access Administrator" --scope "/"',
#     opts=pulumi.ResourceOptions(depends_on=[management_group_user]),
# )
# pulumi.export("Root group: ", root_management_group)
