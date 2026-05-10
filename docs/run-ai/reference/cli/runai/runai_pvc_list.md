# runai pvc list

List PVC

```
runai pvc list [flags]
```

## Examples

```
# List of PVC by project with table output
runai pvc list -p <project-name>

# List of PVC by project with table JSON output
runai pvc list -p <project-name> --json

# List of PVC by project with YAML  output
runai pvc list -p <project-name> --yaml
```

## Options

```
  -h, --help             help for list
      --json             Output structure JSON
      --no-headers       Output structure table without headers
  -p, --project string   Specify the project for the command to use. Defaults to the project set in the context, if any. Use 'runai project set <project>' to set the default.
      --table            Output structure table
      --yaml             Output structure YAML
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

* [runai pvc](/self-hosted/reference/cli/runai/runai_pvc.md) - PVC management


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://run-ai-docs.nvidia.com/self-hosted/reference/cli/runai/runai_pvc_list.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
