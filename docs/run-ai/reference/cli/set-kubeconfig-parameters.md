# Add NVIDIA Run:ai Authorization to Kubeconfig

The `runai kubeconfig set` command allows users to configure their kubeconfig file with NVIDIA Run:ai authorization token. This setup enables users to gain access to the Kubernetes (K8s) cluster seamlessly.

{% hint style="info" %}
**Note**

Setting kubeconfig is not required in order to use the CLI. This command is used to enable third-party workloads under NVIDIA Run:ai authorization.
{% endhint %}

## Usage

To set the token (will be fetched automatically) inside the kubeconfig file, run the following command:

```sh
runai kubeconfig set
```

## Prerequisites

Before executing the command, ensure that

1. [Cluster authentication](/self-hosted/infrastructure-setup/authentication/cluster-authentication.md) is configured and enabled.
2. The user has a kubeconfig file configured.
3. The user is logged in (use the [runai login](/self-hosted/reference/cli/runai/runai_login.md) command).

## User Kubeconfig Configuration

Add the following to the Kubernetes client configuration file (.`/kube/config`). For the full command reference, see [kubeconfig set](/self-hosted/reference/cli/runai/runai_kubeconfig_set.md).

* Make sure to replace values with the actual cluster information and user credentials.
* There can be multiple contexts in the kubeconfig file. The command will configure the current context.

```yaml
apiVersion: v1
kind: Config
preferences:
  colors: true
current-context: <CONTEXT_NAME>
contexts:
- context:
    cluster: <CLUSTER_NAME>
    user: <USER_NAME>
  name: <CONTEXT_NAME>
clusters:
- cluster:
    server: <CLUSTER_URL>
    certificate-authority-data: <CLUSTER_CERT>
  name: <CLUSTER_NAME>
users:
- name: <USER_NAME>
```


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://run-ai-docs.nvidia.com/self-hosted/reference/cli/set-kubeconfig-parameters.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
