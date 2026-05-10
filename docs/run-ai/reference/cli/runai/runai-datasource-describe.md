# runai datasource describe

describe a data source asset

```
runai datasource describe [DATASOURCE_NAME] --type TYPE [flags]
```

## Examples

```
# Describe a data source asset with a default project
runai datasource describe training-data --type pvc

# Describe a data source asset in a specific project
runai datasource describe training-data --type pvc -p <project_name>

# Describe a data source asset with specific output format
runai datasource describe training-data --type nfs -o json
```

## Options

```
  -h, --help             help for describe
  -o, --output string    Output format: table, json, or yaml. Default is table. (default "table")
  -p, --project string   Specify the project. Higher-scope data-sources in the same tenant are included. Use 'runai project set <project>' to set the default.
      --type string      Filter by data source type (nfs, pvc, s3, git, hostPath, configMap, secretVolume, dataVolume)
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
GET https://run-ai-docs.nvidia.com/self-hosted/reference/cli/runai/runai-datasource-describe.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
