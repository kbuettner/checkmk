load("@aspect_rules_py//py:defs.bzl", "py_binary")
load("@bazel_skylib//rules:write_file.bzl", "write_file")
load("@cmk_requirements//:requirements.bzl", "requirement")
load("@rules_pkg//pkg:mappings.bzl", "filter_directory", "pkg_attributes", "pkg_filegroup", "pkg_files", "pkg_mkdirs", "pkg_mklink", "strip_prefix")
load("@rules_pkg//pkg:tar.bzl", "pkg_tar")
load("//bazel/rules:binreplace_version_from_flag.bzl", "binreplace_version_from_flag")

bin_paths = [
    "bin/c_rehash",
    "bin/openssl",
]

lib_symlinks = [
    ("libcrypto.so", "libcrypto.so.3"),
    ("libssl.so", "libssl.so.3"),
]

# skel/etc/ssl/misc/
skel_symlinks = [
    ("tsget", "tsget.pl"),
]

symlinks = lib_symlinks + skel_symlinks

executable_paths = [
    "skel/etc/ssl/misc/CA.pl",
    "skel/etc/ssl/misc/tsget.pl",
]

lib_with_rpath_paths = [
    "lib/libssl.so.3",
    "lib/libcrypto.so.3",
]

genrule(
    name = "openssl_bin_deployable",
    srcs = ["@openssl//:gen_dir"],
    outs = bin_paths + lib_with_rpath_paths,
    cmd = """
        for F in $(OUTS); do
            cp -L $(location @openssl//:gen_dir)/$${F#$(RULEDIR)/} $$F
        done

        chmod u+w $(OUTS)

        # set RPATH for all ELF binaries we find
        file -L $(OUTS) \\
            | grep ELF | cut -d ':' -f1 \\
            | xargs patchelf --force-rpath --set-rpath "\\$$ORIGIN/../lib"
    """,
)

genrule(
    name = "openssl_executables_deployable",
    srcs = ["@openssl//:gen_dir"],
    outs = executable_paths,
    cmd = """
        for F in $(OUTS); do
            cp -L $(location @openssl//:gen_dir)/$${F#$(RULEDIR)/} $$F
        done
    """,
)

pkg_files(
    name = "openssl_bin_pkg",
    srcs = bin_paths,
    attributes = pkg_attributes(
        mode = "0755",
    ),
    prefix = "bin",
)

write_file(
    name = "binreplace",
    out = "binreplace.py",
    content = [
        "import runpy",
        "runpy.run_module('cmk_dev.binreplace', run_name=('__main__'))",
    ],
)

py_binary(
    name = "binreplace_binary",
    srcs = [":binreplace.py"],
    deps = [
        requirement("checkmk-dev-tools"),
    ],
)

[binreplace_version_from_flag(
    name = "run_binreplace_" + edition,
    src =
        ":lib/libcrypto.so.3",
    out = "lib/libcrypto.so.3." + edition,
    intermediate_out = "lib/libcrypto.so.3.replaced",
    new_value = "/omd/versions/{version}.%s/" % edition,
    reg_ex = r"/(?:home|root)/.*?/openssl\.build_tmpdir/openssl/",
    tool = ":binreplace_binary",
    value = "//bazel/cmk/version",
) for edition in [
    "cre",
    "cce",
    "cee",
    "cme",
    "cse",
]]

[pkg_files(
    name = "openssl_lib_with_rpath_pkg_" + edition,
    srcs = [
        "run_binreplace_" + edition,
        "lib/libssl.so.3",
    ],
    prefix = "lib",
    renames = {"lib/libcrypto.so.3." + edition: "libcrypto.so.3"},
) for edition in [
    "cre",
    "cce",
    "cee",
    "cme",
    "cse",
]]

[pkg_mklink(
    name = link_name,
    link_name = link_name,
    target = target,
) for link_name, target in symlinks]

pkg_filegroup(
    name = "openssl_lib_symlinks_pkg",
    srcs = [
        ":%s" % link_name
        for link_name, target in lib_symlinks
    ],
    prefix = "lib",
)

pkg_filegroup(
    name = "openssl_skel_symlinks_pkg",
    srcs = [
        ":%s" % link_name
        for link_name, target in skel_symlinks
    ],
    prefix = "skel/etc/ssl/misc",
)

# empty dir:
pkg_mkdirs(
    name = "openssl_empty_dirs",
    dirs = [
        "lib/engines-3",
        "lib/ossl-modules",
        "skel/etc/ssl/certs",
        "skel/etc/ssl/private",
    ],
)

pkg_files(
    name = "openssl_executables_pkg",
    srcs = [
        ":openssl_executables_deployable",
    ],
    attributes = pkg_attributes(
        mode = "0755",
    ),
    strip_prefix = strip_prefix.from_pkg(""),
)

filter_directory(
    name = "openssl_filtered",
    src = "@openssl//:gen_dir",
    excludes = bin_paths + lib_with_rpath_paths +
               ["lib/%s" % i[0] for i in lib_symlinks] +
               ["skel/etc/ssl/misc/%s" % i[0] for i in skel_symlinks] +
               executable_paths,
)

# This target should contain all files that are not referenced
# explicitly somewhere else (see filter).
pkg_files(
    name = "openssl_rest_pkg",
    srcs = [
        ":openssl_filtered",
    ],
    strip_prefix = "openssl_filtered",
)

[pkg_filegroup(
    name = "openssl_files_pkg_" + edition,
    srcs = [
        ":openssl_bin_pkg",
        ":openssl_empty_dirs",
        ":openssl_executables_pkg",
        ":openssl_lib_symlinks_pkg",
        ":openssl_rest_pkg",
        ":openssl_skel_symlinks_pkg",
        ":openssl_lib_with_rpath_pkg_" + edition,
    ],
    visibility = ["//visibility:public"],
) for edition in [
    "cre",
    "cce",
    "cee",
    "cme",
    "cse",
]]

[pkg_tar(
    name = "openssl_tar_" + edition,
    srcs = [":openssl_files_pkg_" + edition],
    package_file_name = "openssl.tar",
    visibility = ["//visibility:public"],
) for edition in [
    "cre",
    "cce",
    "cee",
    "cme",
    "cse",
]]
