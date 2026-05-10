# runai inference

inference management

## Options

```
  -h, --help   help for inference
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

* [runai](/self-hosted/reference/cli/runai.md) - Run:ai Command-line Interface
* [runai inference bash](/self-hosted/reference/cli/runai/runai-inference-bash.md) - open a bash shell in an inference workload
* [runai inference delete](/self-hosted/reference/cli/runai/runai_inference_delete.md) - delete an inference workload
* [runai inference describe](/self-hosted/reference/cli/runai/runai_inference_describe.md) - describe an inference workload
* [runai inference distributed](/self-hosted/reference/cli/runai/runai-inference-distributed.md) - Runs multiple coordinated inference processes across multiple nodes. Required for models too large to run on a single node.
* [runai inference exec](/self-hosted/reference/cli/runai/runai-inference-exec.md) - execute a command in an inference workload
* [runai inference list](/self-hosted/reference/cli/runai/runai_inference_list.md) - list inference workloads
* [runai inference logs](/self-hosted/reference/cli/runai/runai-inference-logs.md) - view logs of an inference workload
* runai inference nim - \[Experimental] Runs NVIDIA NIM (NVIDIA Inference Microservices) workloads. Optimized for deploying foundation models.
* [runai inference port-forward](/self-hosted/reference/cli/runai/runai-inference-port-forward.md) - forward one or more local ports to an inference workload
* [runai inference standard](/self-hosted/reference/cli/runai/runai-inference-standard.md) - Runs a single inference process on one node. Suitable for smaller models or simpler inference tasks.
* [runai inference submit](/self-hosted/reference/cli/runai/runai_inference_submit.md) - submit an inference workload
* [runai inference update](/self-hosted/reference/cli/runai/runai_inference_update.md) - update an inference workload


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://run-ai-docs.nvidia.com/self-hosted/reference/cli/runai/runai_inference.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
