{ lib, stdenv, python3, python3Packages, fetchPypi, sqlite }:
let
  fs = lib.fileset;
  sourceFiles = fs.unions [
    ./walletweb
  ];
in

with python3Packages;
buildPythonApplication {
  pname = "walletweb";
  version = "1.0";

  src = fs.toSource {
    root = ./walletweb;
    fileset = sourceFiles;
  };

  build-system = [
    setuptools
  ];

  doCheck = false;

  buildInputs = [ python3 build flask schedule pytz gunicorn];

  meta = with lib; {
    description = "A simple Python app using Flask, Schedule, and SQLite";
    license = licenses.mit;
    maintainers = with maintainers; [ "Thomas LE GUEN" ]; # Replace with your name
  };
}