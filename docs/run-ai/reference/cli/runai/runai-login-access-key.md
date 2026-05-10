# runai login access-key

login as a service account or a user using an access key

```
runai login access-key [flags]
```

## Examples

```
# Login interactive using access key
runai login access-key

# Login using access key credentials
runai login access-key --client-id=<client_id> --secret=<secret> --interactive=disabled

# Login and save access key credentials
runai login access-key --client-id=<client_id> --secret=<secret> --interactive=disabled --save
```

## Options

```
      --client-id string     client ID for service account or user
  -h, --help                 help for access-key
      --interactive enable   set interactive mode (enabled|disabled)
      --save                 save access key credentials in config file
      --secret string        access key secret
      --secret-file string   use access key secret from file
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
GET https://run-ai-docs.nvidia.com/self-hosted/reference/cli/runai/runai-login-access-key.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
