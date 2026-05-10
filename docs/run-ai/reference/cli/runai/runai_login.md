# runai login

login to the control plane

```
runai login [flags]
```

## Examples

```

  # Login using browser
  runai login

  # Login using SSO with remote browser
  runai login sso
  runai login remote-browser

  # Login using username and password without browser
  runai login user -u <username> 

  # Login using browser with specific port and host
  runai login --listen-port=43121 --listen-host=localhost

```

## Options

```
  -h, --help                 help for login
      --listen-host string   the host to listen on for the authentication callback (for browser mode only) (default "localhost")
      --listen-port int      the port to listen on for the authentication callback (for browser mode only) (default 43121)
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
* [runai login access-key](/self-hosted/reference/cli/runai/runai-login-access-key.md) - login as a service account or a user using an access key
* [runai login sso](/self-hosted/reference/cli/runai/runai_login_sso.md) - login using sso without browser
* [runai login user](/self-hosted/reference/cli/runai/runai_login_user.md) - login for local user without browser


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://run-ai-docs.nvidia.com/self-hosted/reference/cli/runai/runai_login.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
