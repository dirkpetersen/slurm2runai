# runai inference distributed

Runs multiple coordinated inference processes across multiple nodes. Required for models too large to run on a single node.

## Options

```
  -h, --help   help for distributed
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

* [runai inference](/self-hosted/reference/cli/runai/runai_inference.md) - inference management
* [runai inference distributed bash](/self-hosted/reference/cli/runai/runai-inference-distributed-bash.md) - open a bash shell in a distributed inference workload
* [runai inference distributed delete](/self-hosted/reference/cli/runai/runai-inference-distributed-delete.md) - delete a distributed inference workload
* [runai inference distributed describe](/self-hosted/reference/cli/runai/runai-inference-distributed-describe.md) - describe a distributed inference workload
* [runai inference distributed exec](/self-hosted/reference/cli/runai/runai-inference-distributed-exec.md) - execute a command in a distributed inference workload
* [runai inference distributed list](/self-hosted/reference/cli/runai/runai-inference-distributed-list.md) - list distributed inference workloads
* [runai inference distributed logs](/self-hosted/reference/cli/runai/runai-inference-distributed-logs.md) - view logs of a distributed inference workload
* [runai inference distributed port-forward](/self-hosted/reference/cli/runai/runai-inference-distributed-port-forward.md) - forward one or more local ports to a distributed inference workload
* [runai inference distributed scale](/self-hosted/reference/cli/runai/runai-inference-distributed-scale.md) - scale a distributed inference workload
* [runai inference distributed submit](/self-hosted/reference/cli/runai/runai-inference-distributed-submit.md) - submit a distributed inference workload


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://run-ai-docs.nvidia.com/self-hosted/reference/cli/runai/runai-inference-distributed.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
