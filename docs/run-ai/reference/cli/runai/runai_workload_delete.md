# runai workload delete

Delete workloads

```
runai workload delete [flags]
```

## Examples

```
# Delete multiple workloads
runai workload delete -p proj1 workload01 workload02 workload03

# Delete list of workloads with PyTorch framework filter
runai workload delete -p proj1 --framework pytorch workload01 workload02 workload03

# Delete list of workloads with training type filter
runai workload delete -p proj1 --type training workload01 workload02 workload03

# Delete multiple workloads by bypassing confirmation
runai workload delete -p proj1 -y workload01 workload02 workload03
```

## Options

```
      --framework string   Filter by workload framework (TensorFlow, PyTorch, MPI, XGBoost, JAX).
  -h, --help               help for delete
  -p, --project string     Specify the project for the command to use. Defaults to the project set in the context, if any. Use 'runai project set <project>' to set the default.
      --type string        Filter by workload type. Valid values: training, workspace, inference.
  -y, --yes                bypass confirmation dialog by answering yes
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
GET https://run-ai-docs.nvidia.com/self-hosted/reference/cli/runai/runai_workload_delete.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
