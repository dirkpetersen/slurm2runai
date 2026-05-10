# runai environment list

list environment assets

```
runai environment list [flags]
```

## Examples

```
# List all environment assets
runai environment list -A

# List environment assets in a specific project
runai environment list -p <project_name>

# List environment assets with a specific output format
runai environment list --yaml
```

## Options

```
  -A, --all                   Show resources from all projects
      --columns strings       Specify which columns to display (comma-separated list)
  -h, --help                  help for list
      --json                  Output structure JSON
      --no-headers            Output structure table without headers
  -p, --project string        Specify the project. Higher-scope environments in the same tenant are included. Use 'runai project set <project>' to set the default.
      --raw                   Return the unprocessed response from the API call
      --set-default-columns   [Experimental] Set the columns flag value to the default output
      --table                 Output structure table
      --yaml                  Output structure YAML
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

* [runai environment](/self-hosted/reference/cli/runai/runai-environment.md) - Environment asset management


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://run-ai-docs.nvidia.com/self-hosted/reference/cli/runai/runai-environment-list.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
