# runai inference nim scale

scale a nim inference workload

```
runai inference nim scale [WORKLOAD_NAME] [flags]
```

## Examples

```
# Scale a workload (replicas flag is required)
runai inference nim scale <workload-name> --replicas 5

# Scale with --force to skip autoscaling confirmation
runai inference nim scale <workload-name> --replicas 3 --force
```

## Options

```
      --dry-run          If true, only print the object that would be sent, without sending it
      --force            Skip the confirmation prompt when scaling a workload that has autoscaling enabled
  -h, --help             help for scale
  -p, --project string   Specify the project for the command to use. Defaults to the project set in the context, if any. Use 'runai project set <project>' to set the default.
      --replicas int32   The number of replicas (sets of leader and workers) to run. Defaults to 1
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

* [runai inference nim](/self-hosted/reference/cli/runai/runai-inference-nim.md) - \[Experimental] Runs NVIDIA NIM (NVIDIA Inference Microservices) workloads. Optimized for deploying foundation models.


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://run-ai-docs.nvidia.com/self-hosted/reference/cli/runai/runai-inference-nim-scale.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
