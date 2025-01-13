{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    # stooj-nur.url = "github:stooj/nur-packages";
  };
  outputs = {
    self,
    nixpkgs,
    flake-utils,
    # stooj-nur,
  }:
    flake-utils.lib.eachDefaultSystem (
      system: let
        pkgs = nixpkgs.legacyPackages.${system};
        # stooj = stooj-nur.legacyPackages.${system};
        gdk = pkgs.google-cloud-sdk.withExtraComponents (
          with pkgs.google-cloud-sdk.components; [
            gke-gcloud-auth-plugin
            config-connector # Export existing gcloud config to yaml
          ]
        );
      in {
        devShells.default = pkgs.mkShell {
          packages = [
            # Virtualization
            pkgs.docker
            # Cloud tools
            pkgs.awscli2
            (pkgs.azure-cli.withExtensions
              [
                pkgs.azure-cli.extensions.automation
                pkgs.azure-cli.extensions.portal
              ])
            pkgs.doctl
            gdk
            pkgs.hcloud
            pkgs.kubectl
            # Languages
            pkgs.dotnet-sdk
            pkgs.nodejs
            pkgs.go
            pkgs.openjdk17 # currently-supported LTS version
            # Pulumi packages
            # (pkgs.pulumi.withPackages(ps: with ps; [
            #     pulumi-language-go
            #     pulumi-language-python
            #     pulumi-language-nodejs
            #     pulumi-azure-native
            #     pulumi-aws-native
            #     stooj.pulumi-language-dotnet
            #     stooj.pulumi-language-java
            #     stooj.pulumi-language-yaml
            # ]))
            # # Langauge dependencies
            pkgs.python3
            pkgs.poetry
            # (pkgs.python3.withPackages(ps: with ps; [
            #   pulumi
            #   pulumi-azure-native
            #   # pulumi-aws
            #   pulumi-aws-native
            # ]))
            pkgs.maven
            # Other things
            pkgs.aws-sso-creds
            pkgs.black # Python code formatter
            pkgs.grpc
            pkgs.k9s
          ];
          shellHook = ''
            export LD_LIBRARY_PATH=${pkgs.lib.makeLibraryPath [pkgs.stdenv.cc.cc]}
            export PATH="$PATH:$HOME/.local/pulumi-binaries/latest"
            export AWS_PROFILE="pulumi-ce"
            export PULUMI_HOME=$(pwd)/.pulumi
            eval $(aws-sso-creds export)
          '';
        };
      }
    );
}
