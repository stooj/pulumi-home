import getpass

import pulumi
import pulumi_azure_native as azure_native

# Retrieve current user details
username = getpass.getuser()

management_group_user = azure_native.management.ManagementGroup(
    f"managementGroup{username.title()}",
    details=azure_native.management.CreateManagementGroupDetailsArgs(
        parent=azure_native.management.CreateParentGroupInfoArgs(
            id="/providers/Microsoft.Management/managementGroups/RootGroup",
        ),
    ),
    display_name=f"ManagementGroup{username.title()}",
    group_id=f"ManagementGroup{username.title()}",
)
