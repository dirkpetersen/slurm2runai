# runai diagnostics collect-logs

Examples:

```bash
# Collect logs from all default namespaces
runai diagnostics collect-logs

# Collect logs to a specific output directory
runai diagnostics collect-logs --output-dir /tmp/logs

# Collect logs without previous logs from pods
runai diagnostics collect-logs --no-previous

# Collect logs from specific namespaces
runai diagnostics collect-logs --namespaces runai,runai-backend
```

### Options

```
  -h, --help                   help for collect-logs
      --namespaces enumSlice   Comma-separated list of namespaces to collect logs from (default [runai,runai-reservation,runai-backend,training-operator,knative,gpu-operator,nim-operator])
      --no-previous            Do not collect previous logs from pods
      --output-dir string      Directory to output the archive file (default "./")
```

### Options inherited from parent commands

```
      --config-file string   config file name; can be set by environment variable RUNAI_CLI_CONFIG_FILE (default "config.json")
      --config-path string   config path; can be set by environment variable RUNAI_CLI_CONFIG_PATH
  -d, --debug                enable debug mode
  -q, --quiet                enable quiet mode, suppress all output except error messages
      --verbose              enable verbose mode
```

### See also

* [runai diagnostics](/self-hosted/reference/cli/runai/runai-diagnostics.md) - system diagnostics and troubleshooting tools


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://run-ai-docs.nvidia.com/self-hosted/reference/cli/runai/runai-diagnostics-collect-logs.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
