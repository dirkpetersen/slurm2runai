# runai training mpi exec

execute a command in a mpi training workload

```
runai training mpi exec [WORKLOAD_NAME] [flags]
```

## Examples

```
# Execute bash in the workload's main worker
runai training mpi exec <workload-name> --tty --stdin -- /bin/bash 

# Execute ls command in the workload's main worker
runai training mpi exec <workload-name> -- ls

# Execute a command in a specific worker of the workload
runai training mpi exec <workload-name> --pod <pod-name> -- nvidia-smi
```

## Options

```
  -c, --container string               The name of the container within the pod.
  -h, --help                           help for exec
      --pod string                     The pod ID. If not specified, the first pod will be used.
      --pod-running-timeout duration   Timeout for pod to reach running state (e.g. 5s, 2m, 3h).
  -p, --project string                 Specify the project for the command to use. Defaults to the project set in the context, if any. Use 'runai project set <project>' to set the default.
  -i, --stdin                          Pass stdin to the container
  -t, --tty                            Stdin is a TTY
      --wait-timeout duration          Timeout while waiting for the workload to become ready for log streaming (e.g., 5s, 2m, 3h).
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

* [runai training mpi](/self-hosted/reference/cli/runai/runai_training_mpi.md) - mpi management


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://run-ai-docs.nvidia.com/self-hosted/reference/cli/runai/runai_training_mpi_exec.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
