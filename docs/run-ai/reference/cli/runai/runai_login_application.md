# runai login application

login as an application

```
runai login application [flags]
```

## Examples

```
  
  # Login interactive using application credentials
  runai login app

  # Login using application credentials
  login app --client-id=<app_client_id> --secret=<app_secret> --interactive=disabled

  # Login and Save application credentials
  login app --client-id=<app_client_id> --secret=<app_secret> --interactive=disabled --save

```

## Options

```
      --client-id string     application client ID
  -h, --help                 help for application
      --interactive enable   set interactive mode (enabled|disabled)
      --save                 save application credentials in config file
      --secret string        application secret
      --secret-file string   use application secret from file
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

* [runai login](/self-hosted/reference/cli/runai/runai_login.md) - login to the control plane


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://run-ai-docs.nvidia.com/self-hosted/reference/cli/runai/runai_login_application.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
