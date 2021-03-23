load("@io_bazel_rules_go//go:def.bzl", "go_library")
load("@rules_proto//proto:defs.bzl", "proto_library")
load("@io_bazel_rules_go//proto:def.bzl", "go_proto_library")
load("@rules_proto_grpc//nodejs:defs.bzl", "nodejs_grpc_compile")

nodejs_grpc_compile(
    name = "semanticservice_nodejs_proto",
    deps = [":semanticservice_proto"],
)

proto_library(
    name = "semanticservice_proto",
    srcs = ["semanticservice.proto"],
    visibility = ["//visibility:public"],
)

filegroup(
    name = "semanticservice_file",
    srcs = ["semanticservice.proto"],
    visibility = ["//visibility:public"],
)

go_proto_library(
    name = "semanticservice_go_proto",
    compilers = ["@io_bazel_rules_go//proto:go_grpc"],
    importpath = "coe-sops/proto/semanticservice",
    proto = ":semanticservice_proto",
    visibility = ["//visibility:public"],
)

go_library(
    name = "go_default_library",
    embed = [":semanticservice_go_proto"],
    importpath = "coe-sops/proto/semanticservice",
    visibility = ["//visibility:public"],
)
