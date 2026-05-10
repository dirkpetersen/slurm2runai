# runai my-credential create

create a personal credential

## Synopsis

Create a personal credential. Set --type and pass data with --item using the keys below.

genericSecret Keys: key, value (repeat --item for multiple pairs). Requires cluster version 2.22+. dockerRegistry Keys: user, password, url. Requires cluster version 2.22+. ngcApiKey Keys: ngc-api-key. Requires cluster version 2.23+.

```
runai my-credential create SECRET_NAME --type <genericSecret|dockerRegistry|ngcApiKey> [flags]
```

## Examples

```
  runai my-credential create app-config --type genericSecret --item key=API_URL,value=https://api.example.com --item key=DB_PASS,value=secret
  runai my-credential create dockerhub-creds --type dockerRegistry --item user=myuser,password=secret,url=https://index.docker.io/v1/
  runai my-credential create ngc-prod --type ngcApiKey --item ngc-api-key=YOUR_KEY
```

## Options

```
      --description string   Optional description for the credential (e.g. "My API config" or a single word).
  -h, --help                 help for create
      --item stringArray     Key=value pairs; required keys depend on --type (see above). For genericSecret only, repeat to add multiple pairs to one credential.
      --type string          Credential type: genericSecret, dockerRegistry, or ngcApiKey (required)
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

* [runai my-credential](/self-hosted/reference/cli/runai/runai-my-credential.md) - manage personal credentials associated with the current user


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://run-ai-docs.nvidia.com/self-hosted/reference/cli/runai/runai-my-credential-create.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
