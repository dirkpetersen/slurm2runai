# CLI Commands Reference

Run:ai Command-line Interface

## Synopsis

runai - The Run:ai Researcher Command Line Interface

Description:\
A tool for managing Run:ai workloads and monitoring available resources.\
It provides researchers with comprehensive control over their AI development environment.

```
runai [flags]
```

## Options

```
      --config-file string   config file name; can be set by environment variable RUNAI_CLI_CONFIG_FILE (default "config.json")
      --config-path string   config path; can be set by environment variable RUNAI_CLI_CONFIG_PATH
  -d, --debug                enable debug mode
  -h, --help                 help for runai
  -q, --quiet                enable quiet mode, suppress all output except error messages
      --verbose              enable verbose mode
```

## SEE ALSO

* [runai auth](/self-hosted/reference/cli/runai/runai_auth.md) - Authentication related commands
* [runai cluster](/self-hosted/reference/cli/runai/runai_cluster.md) - cluster management
* [runai config](/self-hosted/reference/cli/runai/runai_config.md) - configuration management
* [runai compute](/self-hosted/reference/cli/runai/runai-compute.md) - Compute resource asset management
* [runai datasource](/self-hosted/reference/cli/runai/runai-datasource.md) - Data Source asset management
* [runai department](/self-hosted/reference/cli/runai/runai-department.md) - department management
* [runai diagnostics](/self-hosted/reference/cli/runai/runai-diagnostics.md) - system diagnostics and troubleshooting tools
* [runai environment](/self-hosted/reference/cli/runai/runai-environment.md) - Environment asset management
* [runai inference](/self-hosted/reference/cli/runai/runai_inference.md) - inference management
* [runai jax](/self-hosted/reference/cli/runai/runai_jax.md) - alias for jax management
* [runai kubeconfig](/self-hosted/reference/cli/runai/runai_kubeconfig.md) - kubeconfig management
* [runai login](/self-hosted/reference/cli/runai/runai_login.md) - login to the control plane
* [runai logout](/self-hosted/reference/cli/runai/runai_logout.md) - logout of the system
* [runai mpi](/self-hosted/reference/cli/runai/runai_mpi.md) - alias for mpi management
* [runai my-credential](/self-hosted/reference/cli/runai/runai-my-credential.md) - manage personal credentials associated with the current user
* [runai node](/self-hosted/reference/cli/runai/runai_node.md) - node management
* [runai nodepool](/self-hosted/reference/cli/runai/runai_nodepool.md) - node pool management
* [runai project](/self-hosted/reference/cli/runai/runai_project.md) - project management
* [runai pvc](/self-hosted/reference/cli/runai/runai_pvc.md) - PVC management
* [runai pytorch](/self-hosted/reference/cli/runai/runai_pytorch.md) - alias for pytorch management
* [runai report](/self-hosted/reference/cli/runai/runai_report.md) - \[Experimental] report management
* [runai template](/self-hosted/reference/cli/runai/runai-template.md) - workload template management
* [runai tensorflow](/self-hosted/reference/cli/runai/runai_tensorflow.md) - alias for tensorflow management
* [runai training](/self-hosted/reference/cli/runai/runai_training.md) - training management
* [runai upgrade](/self-hosted/reference/cli/runai/runai_upgrade.md) - upgrades the CLI to the latest version
* [runai version](/self-hosted/reference/cli/runai/runai_version.md) - show the current version of the CLI
* [runai whoami](/self-hosted/reference/cli/runai/runai_whoami.md) - show the current logged in user
* [runai workload](/self-hosted/reference/cli/runai/runai_workload.md) - workload management
* [runai workload-type](/self-hosted/reference/cli/runai/runai-workload-type.md) - workload type management
* [runai workspace](/self-hosted/reference/cli/runai/runai_workspace.md) - workspace management
* [runai xgboost](/self-hosted/reference/cli/runai/runai_xgboost.md) - alias for xgboost management


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://run-ai-docs.nvidia.com/self-hosted/reference/cli/runai.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
