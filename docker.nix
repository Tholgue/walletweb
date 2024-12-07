buildImage {
  name = "walletweb";
  tag = "latest";

  copyToRoot = pkgs.buildEnv {
    name = "walletweb";
    paths = [ pkgs.walletweb ];
    pathsToLink = [ "/bin" ];
  };

  runAsRoot = ''
    #!${pkgs.runtimeShell}
    mkdir -p /data
  '';

  config = {
    Cmd = [ "/bin/walletweb" ];
    WorkingDir = "/data";
    Volumes = { "/data" = { }; };
  };

  diskSize = 1024;
  buildVMMemorySize = 512;
}