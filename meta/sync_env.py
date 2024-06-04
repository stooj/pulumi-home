"""Syncronize """

import json
import subprocess
import sys

import yaml

if len(sys.argv) != 2:
    print("No environment name given", file=sys.stderr)
    sys.exit(1)

envname = sys.argv[-1]

with open("generated.yaml") as f:
    wanted_env = yaml.load(f, Loader=yaml.Loader).get("values")

current_env = subprocess.run(
    ["pulumi", "env", "open", envname],
    capture_output=True,
)

if current_env.returncode != 0:
    print("Couldn't get environnment", file=sys.stderr)
    sys.exit(1)

current_env_parsed = json.loads(current_env.stdout)


# def merge(a: dict, b: dict, path=[]):
#     for key in b:
#         if key in a:
#             if isinstance(a[key], dict) and isinstance(b[key], dict):
#                 merge(a[key], b[key], path + [str(key)])
#             elif a[key] != b[key]:
#                 raise Exception("Conflict at " + ".".join(path + [str(key)]))
#         else:
#             a[key] = b[key]
#     return a


# def pulumi_config(current, wanted, path=[]):
#     for key in wanted:
#         if key in current:
#             if isinstance(current[key], dict) and isinstance(wanted[key], dict):
#                 pulumi_config(current[key], wanted[key], path + [str(key)])
#             elif current[key] != wanted[key]:
#                 breadcrumbs = ".".join(path + [str(key)])
#                 print(f"{key} at {breadcrumbs} does not match")
#                 print(f"current = {current[key]}, wanted = {wanted[key]}")
#         else:
#             breadcrumbs = ".".join(path + [str(key)])
#             print(f"{key} at {breadcrumbs} matches")
#             if not isinstance(wanted[key], dict):
#                 print("TIME TO UPDATE CONFIG HERE")
#             else:
#                 pulumi_config_tree(wanted[key], path + [str(key)])
#
#
# def pulumi_config_tree(wanted, path=[]):
#     for key in wanted:
#         if isinstance(wanted[key], dict):
#             print(f"Digging into {key}")
#             pulumi_config_tree(wanted[key], path + [str(key)])
#         else:
#             breadcrumbs = ".".join(path + [str(key)])
#             print(f"Reached bottom {key} at {breadcrumbs}")


def safeget(dct, keys):
    for key in keys:
        try:
            dct = dct[key]
        except KeyError:
            return None
    return dct


def pulumi_config(current, wanted, path=[]):
    for key, value in wanted.items():
        breadcrumbs = ".".join(path + [str(key)])
        if not isinstance(value, dict):
            # We've reached the bottom here
            print(f"{key}: {value} is at the bottom in {breadcrumbs}")
            # Does this exist in the current?
            current_value = safeget(current, path + [str(key)])
            if current_value is not None:
                # current exists. Does it match?
                print("Current value exists")
                if current_value == value:
                    print("Current value matches wanted value")
                else:
                    pulumi_config_set(breadcrumbs, value)
            else:
                print("Current value does not exist")
                pulumi_config_set(breadcrumbs, value)
        else:
            pulumi_config(current, value, path + [str(key)])


def pulumi_config_set(key, value):
    print("Going to run:")
    print(f"pulumi env set {envname} {key} {value}")
    # result = subprocess.run(
    #         ["pulumi", "env", "set", envname, key, value]
    #         )
    # if result.returncode != 0:
    #     print("Couldn't set the env value", file=sys.stderr;
    #     sys.exit(1)


print()
print()
print("####  CURRENT ENVIRONMENT ####")
print()
print()
print(json.dumps(current_env_parsed, sort_keys=True, indent=2))
print()
print()
print("####  WANTED ENVIRONMENT ####")
print()
print()
print(json.dumps(wanted_env, sort_keys=True, indent=2))
print()
print()
print("####  Config Set run ####")
print()
print()
pulumi_config(current_env_parsed, wanted_env)
