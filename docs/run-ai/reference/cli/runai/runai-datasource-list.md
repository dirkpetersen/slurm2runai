# runai datasource list

list data source assets

```
runai datasource list [flags]
```

## Examples

```
# List all data source assets
runai datasource list -A

# List data source assets in a specific project
runai datasource list -p <project_name>

# List data source assets with a specific output format
runai datasource list --yaml
```

## Options

```
  -A, --all                   Show resources from all projects
      --columns strings       Specify which columns to display (comma-separated list)
  -h, --help                  help for list
      --json                  Output structure JSON
      --no-headers            Output structure table without headers
  -p, --project string        Specify the project. Higher-scope data-sources in the same tenant are included. Use 'runai project set <project>' to set the default.
      --raw                   Return the unprocessed response from the API call
      --set-default-columns   [Experimental] Set the columns flag value to the default output
      --table                 Output structure table
      --type string           Filter by data source type (nfs, pvc, s3, git, hostPath, configMap, secretVolume, dataVolume)
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

* [runai datasource](/self-hosted/reference/cli/runai/runai-datasource.md) - Data Source asset management


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://run-ai-docs.nvidia.com/self-hosted/reference/cli/runai/runai-datasource-list.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
