# runai inference logs

view logs of an inference workload

```
runai inference logs [WORKLOAD_NAME] [flags]
```

## Examples

```
# Get logs for a workload
runai inference logs <workload-name>

# Get logs for a specific pod in a workload
runai inference logs <workload-name> --pod=<pod-name>

# Get logs for a specific container in a workload
runai inference logs <workload-name> --container=<container-name>

# Get the last 100 lines of logs
runai inference logs <workload-name> --tail=100

# Get logs with timestamps
runai inference logs <workload-name> --timestamps

# Follow the logs
runai inference logs <workload-name> --follow

# Get logs for the previous instance of the workload
runai inference logs <workload-name> --previous

# Limit the logs to 1024 bytes
runai inference logs <workload-name> --limit-bytes=1024

# Get logs since the last 5 minutes
runai inference logs <workload-name> --since=300s

# Get logs since a specific timestamp
runai inference logs <workload-name> --since-time=2023-05-30T10:00:00Z

# Wait up to 30 seconds for a workload to be ready for logs
runai inference logs <workload-name> --wait-timeout=30s
```

## Options

```
  -c, --container string        Container name for log extraction
  -f, --follow                  Follow log output
  -h, --help                    help for logs
      --limit-bytes int         Limit the number of bytes returned from the server
      --name string             Set workload name for log extraction
      --pod string              Workload pod ID for log extraction, default: master (0-0) if exists, else first worker by id
      --previous                Show previous pod log output
  -p, --project string          Specify the project to which the command applies. By default, commands apply to the default project. To change the default project use ‘runai config project <project name>’
      --since duration          Return logs newer than a relative duration like 5s, 2m, or 3h. Defaults to all logs
      --since-time string       Return logs after a specific date (RFC3339)
  -t, --tail int                Number of tailed lines to fetch from the log, for no limit set to -1 (default -1)
      --timestamps              Show timestamps in log output
      --wait-timeout duration   Timeout for waiting for workload to be ready for log streaming
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

* runai inference - inference management


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://run-ai-docs.nvidia.com/self-hosted/reference/cli/runai/runai-inference-logs.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
