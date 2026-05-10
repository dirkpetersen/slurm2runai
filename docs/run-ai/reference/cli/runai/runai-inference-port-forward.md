# runai inference port-forward

forward one or more local ports to an inference workload

```
runai inference port-forward [WORKLOAD_NAME] [flags]
```

## Examples

```
# Forward connections from localhost:8080 to a workload on port 8090:
runai inference port-forward <workload-name> --port 8080:8090 --address localhost

# Forward connections from 0.0.0.0:8080 to a workload on port 8080:
runai inference port-forward <workload-name> --port 8080 --address 0.0.0.0 [requires privileges]

# Forward multiple connections from localhost:8080 to a workload on port 8090 and from localhost:6443 to a workload on port 443:
runai inference port-forward <workload-name> --port 8080:8090 --port 6443:443 --address localhost
```

## Options

```
      --address string                 --address [local-interface-ip\host] --address localhost --address 0.0.0.0 [privileged] (default "localhost")
  -h, --help                           help for port-forward
      --pod string                     Workload pod ID for port-forward, default: distributed(master) otherwise(random)
      --pod-running-timeout duration   Pod check for running state timeout.
      --port stringArray               port
  -p, --project string                 Specify the project to which the command applies. By default, commands apply to the default project. To change the default project use ‘runai config project <project name>’
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
GET https://run-ai-docs.nvidia.com/self-hosted/reference/cli/runai/runai-inference-port-forward.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
