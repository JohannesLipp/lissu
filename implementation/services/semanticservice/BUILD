load("@rules_proto_grpc//python:defs.bzl", "python_grpc_library")
load("@pips//:requirements.bzl", "requirement")

py_binary(
    name = "main",
    srcs = ["main.py"],
    data = ["serverSemantic.json","scannerSemantic.json","qudtscannerSemantic.json"],
    deps = [
        ":semantic_grpc",
        requirement("futures"),
        requirement("absl-py"),
        requirement("numpy"),
        requirement("grpcio-reflection"),
        requirement("rdflib"),
    ],
    visibility = ["//visibility:public"],
)


python_grpc_library(
    name = "semantic_grpc",
    deps = ["//implementation/proto/semanticservice:semanticservice_proto"]
)
