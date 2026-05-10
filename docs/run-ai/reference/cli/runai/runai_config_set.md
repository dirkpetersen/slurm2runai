# runai config set

Set configuration values

```
runai config set [flags]
```

## Examples

```
runai config set --status-timeout-duration 5s
runai config set --status-timeout-duration 300ms
```

## Options

```
      --auth-url string                  set the authorization URL; most likely the same as the control plane URL
      --auto-update enable               enable/disable automatic CLI updates
      --cp-url string                    set the control plane URL
  -h, --help                             help for set
      --interactive enable               set interactive mode (enabled|disabled)
      --list-format-align enable         enable/disable aligned output formatting for list commands to improve readability (disabled by default).
      --output string                    set the default output type
      --status-timeout-duration string   set cluster status call timeout duration value, the default is 3 second ("3s")
      --update-shell string              set the shell to use for updates (e.g., bash, zsh)
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

* [runai config](/self-hosted/reference/cli/runai/runai_config.md) - configuration management


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://run-ai-docs.nvidia.com/self-hosted/reference/cli/runai/runai_config_set.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
