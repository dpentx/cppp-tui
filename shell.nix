{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
	buildInputs = with pkgs; [
		gcc
		openssl.dev
		python3
                python3Packages.textual
	];
}
