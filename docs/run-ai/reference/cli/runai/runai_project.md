# runai project

project management

```
runai project [flags]
```

## Options

```
  -h, --help                    help for project
      --interactive enable      set interactive mode (enabled|disabled)
      --max-items int32         set the max number of items to return, default is all of the items
      --next-token next_token   set the token for requesting the next page
      --no-pagination           return a single page instead of full list, by default set to false
      --page-size int32         set the single page size (default 100)
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
* [runai project create](/self-hosted/reference/cli/runai/runai-project-create.md) - create a new project
* [runai project list](/self-hosted/reference/cli/runai/runai_project_list.md) - list available project
* [runai project set](/self-hosted/reference/cli/runai/runai_project_set.md) - set default project name


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://run-ai-docs.nvidia.com/self-hosted/reference/cli/runai/runai_project.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
