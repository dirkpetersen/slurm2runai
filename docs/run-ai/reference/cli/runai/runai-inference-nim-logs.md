# runai inference nim logs

view logs of a nim inference workload

## Synopsis

If no pod is specified, a ready pod from the workload is used.

```
runai inference nim logs [WORKLOAD_NAME] [flags]
```

## Examples

```
# Get logs for a workload
runai inference nim logs <workload-name>

# Get logs for a specific pod in a workload
runai inference nim logs <workload-name> --pod=<pod-name>

# Get logs for a specific container in a workload
runai inference nim logs <workload-name> --container=<container-name>

# Get the last 100 lines of logs
runai inference nim logs <workload-name> --tail=100

# Get logs with timestamps
runai inference nim logs <workload-name> --timestamps

# Follow the logs
runai inference nim logs <workload-name> --follow

# Get logs for the previous instance of the workload
runai inference nim logs <workload-name> --previous

# Limit the logs to 1024 bytes
runai inference nim logs <workload-name> --limit-bytes=1024

# Get logs since the last 5 minutes
runai inference nim logs <workload-name> --since=300s

# Get logs since a specific timestamp
runai inference nim logs <workload-name> --since-time=2023-05-30T10:00:00Z

# Wait up to 30 seconds for a workload to be ready for logs
runai inference nim logs <workload-name> --wait-timeout=30s
```

## Options

```
  -c, --container string        The name of the container within the pod.
  -f, --follow                  Stream logs in real time.
  -h, --help                    help for logs
      --limit-bytes int         Maximum bytes of logs to return. Defaults to no limit (e.g, 20, 2000).
      --name string             The name of the workload. Must match the name used at submission.
      --pod string              The pod ID. If not specified, the first pod will be used.
      --previous                Show logs from the previous instance of the pod, if it was restarted.
  -p, --project string          Specify the project for the command to use. Defaults to the project set in the context, if any. Use 'runai project set <project>' to set the default.
      --since duration          Show logs newer than a relative duration (e.g., 5s, 2m, 3h).
      --since-time string       Show logs generated after a specific RFC3339 timestamp (e.g. 2025-05-25T14:30:00Z).
  -t, --tail int                The number of log lines to display from the end of the logs. Use -1 to show all lines. (default -1)
      --timestamps              Include timestamps in log output.
      --wait-timeout duration   Timeout while waiting for the workload to become ready for log streaming (e.g., 5s, 2m, 3h).
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
GET https://run-ai-docs.nvidia.com/self-hosted/reference/cli/runai/runai-inference-nim-logs.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
