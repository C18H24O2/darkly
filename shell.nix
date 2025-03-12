{
  pkgs ? import <nixpkgs> {},
}:

pkgs.mkShell {
  nativeBuildInputs = with pkgs; [
    feroxbuster
    hashcat
    virtualboxKvm
  ];
}
