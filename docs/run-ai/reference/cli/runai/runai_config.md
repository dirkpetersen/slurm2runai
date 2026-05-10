# runai config

configuration management

```
runai config [flags]
```

## Options

```
  -h, --help                 help for config
      --interactive enable   set interactive mode (enabled|disabled)
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
* [runai config describe](/self-hosted/reference/cli/runai/runai_config_describe.md) - Returns information about the configuration.
* [runai config generate](/self-hosted/reference/cli/runai/runai_config_generate.md) - generate config file
* [runai config set](/self-hosted/reference/cli/runai/runai_config_set.md) - Set configuration values


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://run-ai-docs.nvidia.com/self-hosted/reference/cli/runai/runai_config.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
