# runai pytorch list

list pytorch training workloads

```
runai pytorch list [flags]
```

## Examples

```
# List all pytorch training workloads
runai training pytorch list -A

# List workloads with default project
runai training pytorch list

# List workloads in a specific project
runai training pytorch list -p <project-name>

# List all workloads with a specific output format
runai training pytorch list --yaml

# List workloads with pagination
runai training pytorch list --limit 20 --offset 40
```

## Options

```
  -A, --all                     Show resources from all projects
      --columns strings         Specify which columns to display (comma-separated list)
      --deleted                 Return only resources that have been deleted.
  -h, --help                    help for list
      --json                    Output structure JSON
      --max-items int32         set the max number of items to return, default is all of the items
      --next-token next_token   set the token for requesting the next page
      --no-headers              Output structure table without headers
      --no-pagination           return a single page instead of full list, by default set to false
      --page-size int32         set the single page size (default 100)
  -p, --project string          Specify the project for the command to use. Defaults to the project set in the context, if any. Use 'runai project set <project>' to set the default.
      --raw                     Return the unprocessed response from the API call
      --set-default-columns     [Experimental] Set the columns flag value to the default output
      --status string           Filter by workload state (e.g., Pending, Running, Completed, Failed, Stopped, Initializing).
      --table                   Output structure table
      --yaml                    Output structure YAML
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

* [runai pytorch](/self-hosted/reference/cli/runai/runai_pytorch.md) - alias for pytorch management


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://run-ai-docs.nvidia.com/self-hosted/reference/cli/runai/runai_pytorch_list.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
