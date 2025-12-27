{
  description = "Aga icin dev-shell";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
  let
    system = "x86_64-linux";
    pkgs = import nixpkgs { inherit system; };
  in {
    devShells.${system}.default = pkgs.mkShell {
      name = "aga-shell";

      packages = with pkgs; [
        nodejs
        python3
        python3Packages.textual
        git
        gcc
      ];

      shellHook = ''
        echo "🔥 DEV SHELL AKTIF AGA 🔥"
      '';
    };
  };
}
