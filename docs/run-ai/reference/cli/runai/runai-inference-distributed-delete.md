# runai inference distributed delete

delete a distributed inference workload

```
runai inference distributed delete [WORKLOAD_NAME] [flags]
```

## Examples

```
# Delete a workload with a default project
runai inference distributed delete <workload-name>

# Delete a workload with a specific project
runai inference distributed delete <workload-name> -p <project-name>

# Delete a workload by UUID
runai inference distributed delete --uuid=<workload-id> -p <project-name>
```

## Options

```
  -h, --help             help for delete
  -p, --project string   Specify the project for the command to use. Defaults to the project set in the context, if any. Use 'runai project set <project>' to set the default.
  -u, --uuid string      The unique identifier (UUID) of the resource, as returned by the API.
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

* [runai inference distributed](/self-hosted/reference/cli/runai/runai-inference-distributed.md) - Runs multiple coordinated inference processes across multiple nodes. Required for models too large to run on a single node.


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://run-ai-docs.nvidia.com/self-hosted/reference/cli/runai/runai-inference-distributed-delete.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
