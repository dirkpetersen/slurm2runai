# Uninstall

## Uninstall the Control Plane

To delete the control plane, run:

```bash
helm uninstall runai-backend -n runai-backend
```

## Uninstall the Cluster

To uninstall the NVIDIA Run:ai cluster, run the following [helm](https://helm.sh/) command in your terminal:

```bash
helm uninstall runai-cluster -n runai
```

To remove the NVIDIA Run:ai cluster from the NVIDIA Run:ai platform, see [Removing a cluster](/self-hosted/infrastructure-setup/procedures/clusters.md#removing-a-cluster).

{% hint style="info" %}
**Note**

Uninstall of NVIDIA Run:ai cluster from the Kubernetes cluster does **not** delete existing projects, departments or workloads submitted by users.
{% endhint %}


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://run-ai-docs.nvidia.com/self-hosted/getting-started/installation/install-using-helm/uninstall.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
