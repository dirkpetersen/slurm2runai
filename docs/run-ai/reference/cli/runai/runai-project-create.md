# runai project create

Create a new project

```
runai project create PROJECT_NAME [flags]
```

## Examples

```
# Create a project using single nodepools
runai project create <name> --resources nodepool=<nodepool_name>,gpu-deserved=<gpu_deserved_number>,gpu-limit=<gpu_limit_number>,priority=<priority_name> 
							--description <description>

# Create a project using multiple nodepools
runai project create <name> --resources nodepool=<nodepool_name>,gpu-deserved=<gpu_deserved_number>,gpu-limit=<gpu_limit_number>,priority=<priority_name> 
							--resources nodepool=<nodepool_name>,gpu-deserved=<gpu_deserved_number>,gpu-limit=<gpu_limit_number>,priority=<priority_name> 
							--description <description>

# Create a project using existing namespace
runai project create <name> --resources nodepool=<nodepool_name>,gpu-deserved=<gpu_deserved_number>,gpu-limit=<gpu_limit_number>,priority=<priority_name> 
							--description <description>
							--namespace <namespace>

# Create a project using default values for gpu-deserved (0) and gpu-limit (-1)
runai project create <name> --resources nodepool=<nodepool_name>,priority=<priority_name> 
							--description <description>
							--namespace <namespace>

# Create a project using default nodepool and all default values for gpu-deserved (0) and gpu-limit (-1)
runai project create <name>

```

## Options

```
      --department string     Department for the project (default "default")
      --description string    Description for the project
  -h, --help                  help for create
      --json                  Output structure JSON
      --namespace string      Namespace for the project
      --no-headers            Output structure table without headers
      --resources resources   Resources for the project (can be specified multiple times)
      --table                 Output structure table
      --yaml                  Output structure YAML
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

* [runai project](/self-hosted/reference/cli/runai/runai_project.md) - project management


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://run-ai-docs.nvidia.com/self-hosted/reference/cli/runai/runai-project-create.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
