# runai workload submit

submit a workload from a yaml file

#### Synopsis

Submit a workload using a Kubernetes manifest file.

This command submits workloads directly from YAML manifests to the control plane. It provides flexibility in managing workloads through declarative configuration.

```
runai workload submit [NAME] [flags]
```

## Examples

```
# Submit a workload from a manifest file (uses manifest metadata.name or defaults to "workload")
runai workload submit --file workload.yaml --project my-project

# Submit with a specific name
runai workload submit <name> --file workload.yaml --project my-project

# Submit with name as prefix (generates random suffix)
runai workload submit --name-prefix my-workload --file workload.yaml --project my-project

# Submit with priority override
runai workload submit --file workload.yaml --project my-project --priority high

# Submit with category
runai workload submit --file workload.yaml --project my-project --category production

# Submit with MNNVL mode enabled
runai workload submit --file workload.yaml --project my-project --mnnvl Required
```

## Options

```
      --category string                 Set workload category
  -f, --file string                     Path to the workload manifest YAML file (required)
  -h, --help                            help for submit
      --mnnvl mnnvl                     Enable MNNVL (Multi-Node NVLink) mode. Valid values: Required|None
      --name-prefix string              Use the provided name as a prefix (generates random suffix). Mutually exclusive with [NAME] argument
      --preemptibility preemptibility   Specify whether the workload can be preempted by higher-priority workloads. Valid values: preemptible, non-preemptible. Overrides the default preemptibility for the workload type.
      --priority string                 Sets the workload’s scheduling priority. Valid values: very-low, low, medium-low, medium, medium-high, high, very-high. 
                                        Overrides the default priority for the workload type. Changing priority does not update preemptibility automatically.
  -p, --project string                  Specify the project for the command to use. Defaults to the project set in the context, if any. Use 'runai project set <project>' to set the default.
```

## Options inherited from parent commands

```
      --config-file string   config file name; can be set by environment variable RUNAI_CLI_CONFIG_FILE (default "config.json")
      --config-path string   config path; can be set by environment variable RUNAI_CLI_CONFIG_PATH
  -d, --debug                enable debug mode
  -q, --quiet                enable quiet mode, suppress all output except error messages
      --verbose              enable verbose mode
```

## SEE ALSO

* [runai workload](/self-hosted/reference/cli/runai/runai_workload.md) - workload management


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://run-ai-docs.nvidia.com/self-hosted/reference/cli/runai/runai-workload-submit.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
