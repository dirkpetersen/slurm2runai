# General Settings

The **General settings** section in the Admin panel provides centralized controls for enabling or disabling key platform features. These settings allow administrators to tailor the behavior of the NVIDIA Run:ai environment based on organizational policies, user needs, and workload types.

## Analytics

| Setting               | Description                                                                                                                                                                                                                                                                                                                               |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| GPU profiling metrics | Enable to view metrics in the Nodes table and the Workload Metrics tab. To configure the [NVIDIA exporter](https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/feature-overview.html#metrics) and NVIDIA Run:ai cluster, see [GPU profiling metrics](/self-hosted/platform-management/monitor-performance/gpu-profiling-metrics.md) |

## Resources

| Setting                                                             | Description                                                                                                                                                                                                                                                                                                             |
| ------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Limit projects from exceeding department quota                      | Enable to prevent projects’ total quota from exceeding the department’s quota or being less than the total usage by non-preemptible workloads. For more information, see the [NVIDIA Run:ai Scheduler guide](/self-hosted/platform-management/runai-scheduler/scheduling/concepts-and-principles.md#over-subscription). |
| CPU quota                                                           | Enable resource quota based on CPU resources. For more information, see the [Departments guide](/self-hosted/platform-management/aiinitiatives/organization/departments.md) and the [Projects guide](/self-hosted/platform-management/aiinitiatives/organization/projects.md).                                          |
| Over quota weight                                                   | Enable over quota weight to set what proportion of unused resources a project can get on top of its quota. For more information, see the [Over quota weight guide](/self-hosted/platform-management/runai-scheduler/scheduling/concepts-and-principles.md#over-quota-weight).                                           |
| GPU resource optimization <mark style="color:orange;">`Beta`</mark> | Enable to set a GPU memory limit for workloads. To enable this on each NVIDIA Run:ai cluster, see the [Dynamic GPU fractions guide](/self-hosted/platform-management/runai-scheduler/resource-optimization/dynamic-fractions.md).                                                                                       |

## Workloads

| Setting                                                                    | Description                                                                                                                                                                                                                                                                                                                                                                                               |
| -------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Policies                                                                   | Enable to impose restrictions and default values on workloads' fields. For more information, see the [Policies guide](/self-hosted/platform-management/policies/policies-and-rules.md)                                                                                                                                                                                                                    |
| Hugging face models                                                        | Enable instant deployment of Hugging Face models via the Models view or the workload submission form. For more information, see the [Deploy inference workloads from Hugging Face](/self-hosted/workloads-in-nvidia-run-ai/using-inference/hugging-face-inference.md).                                                                                                                                    |
| NIM models                                                                 | Enable instant deployment of NIM models via the workload submission form. For more information, see the [Deploy inference workloads with NVIDIA NIM](/self-hosted/workloads-in-nvidia-run-ai/using-inference/nim-inference.md).                                                                                                                                                                           |
| Flexible workload submission                                               | Enable to submit workloads via the new flexible form. Allow selecting an existing setup or starting from scratch, reviewing existing setups and understanding policy definitions. The form also includes advanced features tailored for inference workloads. For more information, see [Flexible submission](/self-hosted/2.21/getting-started/whats-new/whats-new-2-21.md#flexible-workload-submission). |
| Flexible workload templates                                                | Enable to create workload templates via the new flexible form. For more information, see the [Workload Templates guide](/self-hosted/workloads-in-nvidia-run-ai/workload-templates.md).                                                                                                                                                                                                                   |
| Data volumes                                                               | Enable to allow creation of data volumes to share underlying data across scopes. For more information, see the [Data volumes guide](/self-hosted/workloads-in-nvidia-run-ai/assets/data-volumes.md).                                                                                                                                                                                                      |
| Submit supported workload types via YAML                                   | Enable to submit a range of workload types using a standard Kubernetes YAML. For more information, see the [Submit supported workload types via YAML guide](/self-hosted/workloads-in-nvidia-run-ai/submit-via-yaml.md).                                                                                                                                                                                  |
| AI application submission <mark style="color:green;">`Experimental`</mark> | Enable to deploy agentic AI application stacks from the NGC catalog or Helm repositories, with resource overrides for multi-component pipelines. For more information, see the [AI applications guide](/self-hosted/ai-applications/ai-applications.md).                                                                                                                                                  |
| NGC catalog <mark style="color:orange;">`Beta`</mark>                      | Enable to browse and select container images from the NVIDIA NGC catalog for faster environment setup.                                                                                                                                                                                                                                                                                                    |
| NGC private registry <mark style="color:orange;">`Beta`</mark>             | Enable browsing of your organization's proprietary container image registry, hosted on the NGC private registry service                                                                                                                                                                                                                                                                                   |

## Security

| Setting                   | Description                                                                                                                                                                                                                                                            |
| ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Identity provider         | Anyone given access to the NVIDIA Run:ai application via the identity provider system will be able to join the platform and authenticate using SSO. See [Single Sign-On (SSO) guide](/self-hosted/infrastructure-setup/authentication/overview.md#single-sign-on-sso). |
| Set logout redirect URL   | Users will be redirected to this URL after logging out from NVIDIA Run:ai                                                                                                                                                                                              |
| Set UI inactivity timeout | Users will be automatically logged out of NVIDIA Run:ai after the set period of inactivity. CLI and API access are not affected. (If left blank, users are logged out after 24 hours of inactivity by default.)                                                        |

## Notifications

| Setting             | Description                                                             |
| ------------------- | ----------------------------------------------------------------------- |
| Email notifications | Set the email server through which the email notifications will be sent |
| Slack notifications | Authorize and connect your Slack workspace to NVIDIA Run:ai             |
| System notification | Write a message that will be displayed to all users                     |

For more details, see [Notifications](/self-hosted/settings/general-settings/notifications.md).

## Cluster Authentication

To allow users to securely submit workloads using `kubectl`, you must configure the Kubernetes API server to authenticate users via the NVIDIA Run:ai identity provider. This is done by adding OpenID Connect (OIDC) flags to the Kubernetes API server configuration on each cluster. See [Cluster authentication](/self-hosted/infrastructure-setup/authentication/cluster-authentication.md) for more details.

## Branding

Upload the logo you want displayed in the top-right corner of the NVIDIA Run:ai platform interface. Logos can be uploaded in SVG or PNG format (up to 128 KB).

To display a custom logo in the platform interface:

1. Click **+ LOGO**.
2. In the upload window, click the upload icon and select your logo file
3. Click **SAVE**

You can update or remove it at any time by clicking the **edit** or **remove** icons.


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://run-ai-docs.nvidia.com/self-hosted/settings/general-settings.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
