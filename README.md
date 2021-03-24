# LISSU: Integrating SemanticWeb Concepts Into SOA Frameworks
Resource repository accompanying the research paper "LISSU: Integrating Semantic Web Concepts Into SOA Frameworks" from the [International Conference on Enterprise Information Systems (ICEIS)](http://www.iceis.org/), covering code snippets and an example.

## Implementation

Prerequisites:
- `bazel`

Find out how to install it here: https://docs.bazel.build/versions/master/install-ubuntu.html

Run `bazel run //implementation/services/semanticservice:main` from inside this folder.



## Usage of the Semantic Services 

### Related file locations
Under `/implementation/services/semanticservice` you can find the "main.py" file containing the two new semantic service implementations and the semantic configurations for the servers as well. The server configurations should be named after the server. 

The services are defined under `proto/semanticservice/semanticservice.proto`  

So far only tested with the scanner service. Under `services/scannerservice/hardwarecontroller/semanticDemos` the "withSem.py" file can be used as a test for both semantic modules in an error free environment and the "failedSem.py" file for a case with semantical errors. 

The "clientSemantic.json" is a configuration file with the OM URIs while "qudtSemantic.json" has the QUDT identifiers. 

### Runing applications with semantics enabled 
All the following commands assume, that you are within the folder of the file you want to run. 

1) Run the semantic server in this folder via `bazel run main`.  

2) Run a desired server, for example the scanner mockup under `services/scannerservice/hardwarecontroller/mockup` via `bazel run mockup`

3) Start your desired client, for example the demo client under `services/scannerservice/hardwarecontroller/semanticDemos` via `bazel run withSem`or `bazel run failedSem`

Authors: Siyabend Sakik, Moritz Kröger, Johannes Lipp
