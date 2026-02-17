{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    devshell.url = "github:numtide/devshell";
    flake-parts.url = "github:hercules-ci/flake-parts";
    systems.url = "github:nix-systems/default";
  };

  outputs =
    inputs@{ flake-parts, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      imports = [
        inputs.devshell.flakeModule
      ];
      systems = import inputs.systems;
      perSystem =
        { pkgs, ... }:
        {
          devshells.default = {
            packages = [ pkgs.markdown-link-check ];
            commands = [
              {
                name = "check-links";
                command = "${pkgs.lib.getExe pkgs.markdown-link-check} -i node_modules -i .git .";
                help = "Check all markdown links";
              }
            ];
          };
        };
    };
}
