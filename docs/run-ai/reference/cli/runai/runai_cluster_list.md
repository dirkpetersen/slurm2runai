# runai cluster list

cluster list command

```
runai cluster list [flags]
```

## Options

```
      --columns strings      Specify which columns to display (comma-separated list)
  -h, --help                 help for list
      --json                 Output structure JSON
      --no-headers           Output structure table without headers
      --raw                  Return the unprocessed response from the API call
      --set-default-columns  [Experimental] Set the columns flag value to the default output
      --table                Output structure table
      --yaml                 Output structure YAML
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

* [runai cluster](/self-hosted/reference/cli/runai/runai_cluster.md) - cluster management


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://run-ai-docs.nvidia.com/self-hosted/reference/cli/runai/runai_cluster_list.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
