# Enter this shell `nix-shell shell.nix` to fix missing libraries
{ pkgs ? import <nixpkgs> {} }:
(pkgs.buildFHSUserEnv {
  name = "pipzone";
  targetPkgs = pkgs: (with pkgs; [
    python3
    python3Packages.pip
    python3Packages.virtualenv
  ]);
  runScript = "bash";
}).env
