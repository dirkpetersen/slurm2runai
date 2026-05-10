# Workload Assets

NVIDIA Run:ai [workload](/self-hosted/workloads-in-nvidia-run-ai/workloads.md) assets are preconfigured building blocks that simplify the workload submission effort and remove the complexities of Kubernetes and networks for AI practitioners.

Workload assets enable organizations to:

* Create and reuse preconfigured setup for code, data, storage and resources to be used by AI practitioners to simplify the process of submitting workloads
* Share the preconfigured setup with a wide audience of AI practitioners with similar needs

{% hint style="info" %}
**Note**

* The creation of assets is possible only via API and the NVIDIA Run:ai UI.
* The submission of workloads using assets, is possible only via the NVIDIA Run:ai UI.
  {% endhint %}

## Workload Asset Types

There are four workload asset types used by the workload:

* [Environments](/self-hosted/workloads-in-nvidia-run-ai/assets/environments.md)\
  The container image, tools and connections for the workload
* [Data sources](/self-hosted/workloads-in-nvidia-run-ai/assets/datasources.md)\
  The type of data, its origin and the target storage location such as PVCs or cloud storage buckets where datasets are stored
* [Compute resources](/self-hosted/workloads-in-nvidia-run-ai/assets/compute-resources.md)\
  The compute specification, including GPU and CPU compute and memory
* [Credentials](/self-hosted/workloads-in-nvidia-run-ai/assets/credentials.md)\
  The secrets to be used to access sensitive data, services, and applications such as docker registry or S3 buckets

## Asset Scope

When a workload asset is created, a [scope](/self-hosted/platform-management/aiinitiatives/adapting-ai-initiatives.md#scopes-in-an-organization) is required. The scope defines who in the organization can view and/or use the asset.

{% hint style="info" %}
**Note**

When an asset is created via API, the scope can be the entire account. This is currently an experimental feature.
{% endhint %}

## Who Can Create an Asset?

Any subject (user, service account, or SSO group) with a [role](/self-hosted/infrastructure-setup/authentication/roles.md) that has permissions to **Create** an asset, can do so within their scope.

## Who Can Use an Asset?

Assets are used when submitting workloads. Any subject (user, service account or SSO group) with a [role](/self-hosted/infrastructure-setup/authentication/roles.md) that has permissions to **Create** workloads, can also use assets.

## Who Can View an Asset?

Any subject (user, service account, or SSO group) with a [role](/self-hosted/infrastructure-setup/authentication/roles.md) that has permission to **View** an asset, can do so within their scope.


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://run-ai-docs.nvidia.com/self-hosted/workloads-in-nvidia-run-ai/assets/overview.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
