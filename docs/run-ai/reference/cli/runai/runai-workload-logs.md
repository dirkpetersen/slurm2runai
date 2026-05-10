# runai workload logs

view logs of a workload

## Synopsis

```
runai workload logs [flags]
```

## Examples

<pre><code># Get logs for a workload
runai workload logs

# Get logs for a specific pod in a workload
runai workload logs --pod=

# Get logs for a specific container in a workload
runai workload logs --container=

# Get the last 100 lines of logs
runai workload logs --tail=100

# Get logs with timestamps
runai workload logs --timestamps

# Follow the logs
runai workload logs --follow

# Get logs for the previous instance of the workload
runai workload logs --previous

# Limit the logs to 1024 bytes
runai workload logs --limit-bytes=1024

# Get logs since the last 5 minutes
runai workload logs --since=300s

# Get logs since a specific timestamp
runai workload logs --since-time=2023-05-30T10:00:00Z

<strong># Wait up to 30 seconds for a workload to be ready for logs
</strong>runai workload logs --wait-timeout=30s
</code></pre>

## Options

```
  -c, --container string        The name of the container within the pod.
  -f, --follow                  Stream logs in real time.
  -h, --help                    help for logs
      --limit-bytes int         Maximum bytes of logs to return. Defaults to no limit (e.g, 20, 2000).
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

* [runai workload](/self-hosted/reference/cli/runai/runai_workload.md) - workload management


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://run-ai-docs.nvidia.com/self-hosted/reference/cli/runai/runai-workload-logs.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
