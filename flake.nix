{
  inputs.nixpkgs.url = "github:nixos/nixpkgs";

  outputs = { self, ... } @ inputs:
    let
      system = "x86_64-linux";
      pkgs = (import inputs.nixpkgs { system = "x86_64-linux"; });
    in
    {
      formatter.${system} = pkgs.nixpkgs-fmt;
      devShells.${system}.default = pkgs.mkShell {
        buildInputs = [
          (pkgs.symlinkJoin {
            name = "shelly";
            paths = [
              (pkgs.python3.withPackages (ps: with ps; [
                # Python dependencies goes here
                plumbum
              ]))
              # Other dependencies goes here
              pkgs.ulauncher
              pkgs.zsh
            ];
          })
        ];
        shellHook = ''
          exec zsh
        '';
      };
    };
}
