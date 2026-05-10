# What's New in Version 2.25

The NVIDIA Run:ai v2.25 what's new provides a detailed summary of the latest features, enhancements, and updates introduced in this version. They serve as a guide to help users, administrators, and researchers understand the new capabilities and how to leverage them for improved workload management, resource optimization, and more.

{% hint style="info" %}
**Important**

For a complete list of deprecations, see [Deprecation notifications](#deprecation-notifications). Deprecated features, APIs, and capabilities remain available for **two versions** from the time of the deprecation notice, after which they may be removed.
{% endhint %}

## AI Practitioners <a href="#ai-practitioners" id="ai-practitioners"></a>

### Workloads <a href="#workloads" id="workloads"></a>

* **Deploy AI applications directly from NGC catalog** - Blueprints (and other Helm charts) from the NVIDIA NGC catalog or via direct URL can be deployed as AI applications through the UI and API, without requiring direct cluster access. Deploying them as AI applications enables fast assembly of the building blocks that power agentic pipelines in a single workflow. You can override Helm values before deployment (for example, request GPU fractions), enabling flexible configuration and faster deployment of complex, multi-component AI applications. See [AI applications](/self-hosted/ai-applications/ai-applications.md) for more details. <mark style="color:green;">`Experimental`</mark> `From cluster v2.25 onward`
* **Topology placement visibility for workloads** - NVIDIA Run:ai exposes the actual topology placement of a workload, making it easy to validate scheduling decisions and troubleshoot performance issues for multi-node workloads. For each workload, you can see the topology name, the actual placement (topology level and value), the requested constraints, and whether those constraints were met. This information is available for both native and supported workload types via the [Workloads](https://run-ai-docs.nvidia.com/api/2.25/workloads/workloads) API, and for native workloads in the workload [Details](/self-hosted/workloads-in-nvidia-run-ai/workloads.md#show-hide-details) view in the UI. See [Accelerating workloads with network topology-aware scheduling](/self-hosted/platform-management/aiinitiatives/resources/topology-aware-scheduling.md#topology-constraints-visibility) for more details. `From cluster v2.25 onward`
* **MNNVL acceleration for YAML-based workload submission** - When submitting YAML-based workloads, you can specify whether Multi-Node NVLink (MNNVL) acceleration is required on a per-workload basis. When required, workloads are scheduled only on MNNVL-capable nodes; otherwise, they can run on any compatible nodes. This provides more precise control over placement and performance for multi-GPU workloads. See [Submit supported workload types via YAML](/self-hosted/workloads-in-nvidia-run-ai/submit-via-yaml.md) for more details. `From cluster v2.24 onward`
* **Enhanced workload structure visibility** - NVIDIA Run:ai now surfaces the full internal structure of [supported workload types](/self-hosted/workloads-in-nvidia-run-ai/submit-via-yaml.md), allowing users to navigate from the top-level workload down to individual elements and pods. For each element, you can inspect its name, type, and parent-child relationships both via the API and in the UI through a new hierarchical **Structure** tab in the workload [Details](/self-hosted/workloads-in-nvidia-run-ai/workloads.md#show-hide-details) panel. Administrators can use the Resource Interface to define the structure of additional workload types. This enables newly introduced workloads to expose the same hierarchy and relationships, making them visible and consistent across the API and UI. See [Defining a Resource Interface](/self-hosted/workloads-in-nvidia-run-ai/workload-types/extending-workload-support/defining-a-resource-interface.md) for more details. `From cluster v2.25 onward`
* **DRA support for GPU devices** - NVIDIA Run:ai supports scheduling supported workload types submitted [via YAML](/self-hosted/workloads-in-nvidia-run-ai/submit-via-yaml.md) using Kubernetes Dynamic Resource Allocation (DRA) ResourceClaims for GPU devices, in addition to the existing extended resources method (`nvidia.com/gpus`). This enables more flexible and expressive GPU resource requests, improving scheduling accuracy and laying the foundation for advanced capabilities. DRA-based workloads are fully supported across the NVIDIA Run:ai UI, API, and CLI. To avoid conflicts when mixing DRA and extended resources, it is recommended to use separate node pools for DRA workloads. See [Dynamic resource allocation (DRA)](/self-hosted/platform-management/runai-scheduler/scheduling/concepts-and-principles.md#dynamic-resource-allocation-dra) for more details. `From cluster v2.25 onward`
* **Automatic external endpoint discovery for workloads and AI applications** - After deploying a workload, its externally reachable endpoints are automatically discovered and displayed in the **Connections** column of the [Workloads](/self-hosted/workloads-in-nvidia-run-ai/workloads.md#connections-associated-with-the-workload) and [AI Applications](/self-hosted/ai-applications/ai-applications.md#connections-associated-with-the-ai-application) tables. Endpoints are also exposed as part of the workload object via the [Workloads](https://run-ai-docs.nvidia.com/api/2.25/workloads/workloads) API. For AI applications composed of multiple workloads, endpoints from all workloads are aggregated and can be viewed in the UI or queried at the application level via the [AI Applications](https://run-ai-docs.nvidia.com/api/2.25/ai-applications/ai-applications) API. Endpoint state is kept in sync automatically as networking resources are created, updated, or deleted. `From cluster v2.25 onward`
* **UI adjustments for distributed training** - The distributed training workflow (workloads and templates) in the UI now includes a third step for mutual workload setup. The "Allow different setup for the master" toggle has been removed. By default, the master and workers use the same setup unless a policy defines different behavior. This applies to Flexible submission only. See [Train models using a distributed training workload](/self-hosted/workloads-in-nvidia-run-ai/using-training/distributed-training-models.md) for more details.
* **Pod logs and terminal access** - Accessing pod logs and interactive shells is now faster and more consistent across the Workloads experience. You can open logs or connect to running pods directly from multiple entry points, with pod selection and status kept in sync as you move between views. See [Workloads](/self-hosted/workloads-in-nvidia-run-ai/workloads.md#show-hide-details) for more details. `From cluster v2.23 onward`
  * One-click access to logs and terminals from the Pods view and Logs view, with the selected pod opened automatically.
  * New Terminal tab for interactive access to pods and containers, including automatic connection when launching from the Workload grid.
  * Synchronized pod selection and status across Pods, Logs, and Terminal views, while preserving existing responsive pod name behavior.
  * View logs from previous container instances using the **Container's logs from** dropdown, allowing you to switch between logs from the current running container instance and the previous one.

### Inference <a href="#inference" id="inference"></a>

* **Hierarchical topology-aware scheduling for Dynamo workloads** - Dynamo workloads support hierarchical, multi-component topology-aware scheduling using Grove topology definitions. Administrators define and link Grove and NVIDIA Run:ai topologies, which are then used to apply topology constraints at both the workload (Deployment) and component (Service) levels. The NVIDIA Run:ai scheduler enforces these constraints, enabling precise placement across clusters with multiple topologies. This improves performance and avoids over-constrained scheduling compared to previous workload-level topology constraints. See [Accelerating workloads with network topology-aware scheduling](/self-hosted/platform-management/aiinitiatives/resources/topology-aware-scheduling.md#topology-aware-scheduling-for-dynamo-over-grove) for more details. `From cluster v2.25 onward`
* **Distributed inference deployment from the UI** - AI practitioners can now submit and manage distributed (multi-node) inference workloads directly from the NVIDIA Run:ai UI. This enables deployment of large models that exceed the capacity of a single node. Each distributed replica consists of a leader and multiple workers, both configured as part of the submission form. Distributed mode is supported for custom inference only. See [Deploy a distributed inference workload](/self-hosted/workloads-in-nvidia-run-ai/using-inference/distributed-inference.md) for more details. `From cluster v2.22 onward`
* **Deployment of models from Hugging Face** - Models from Hugging Face can now be deployed directly through the NIM serving path using Multi-LLM NIM — a single container that enables deployment of a broad range of models. Previously, only NGC catalog models with dedicated NIM images could use the NIM serving flow; Hugging Face models were restricted to generic serving options. This removes the one-image-per-model dependency and allows a wider range of models to be served through the NIM path, directly from the Run:ai UI. See [Deploy inference workloads with NVIDIA NIM](/self-hosted/workloads-in-nvidia-run-ai/using-inference/nim-inference.md) for more details.
* **Endpoint access control for NIM services API** - NVIDIA NIM services deployed via the NIM Operator support endpoint access control for NVIDIA Run:ai users, groups, and service accounts through the API. This enables secure access to inference endpoints and aligns NIM services with enterprise security requirements. See [NVIDIA NIM](https://run-ai-docs.nvidia.com/api/2.25/workloads/nvidia-nim) API for more details. `From cluster v2.25 onward`
* **CLI support for NVIDIA NIM services** - NVIDIA NIM services deployed via the NIM Operator can be managed directly from the NVIDIA Run:ai CLI, bringing a full command-line experience without requiring API access. See [CLI command reference](/self-hosted/reference/cli/runai/runai-inference-nim.md) for more details. `From cluster v2.25 onward`
  * Supports the full service lifecycle: submit, update, list, delete, exec, logs, port-forward, and describe.
  * Applies to existing NIM capabilities including autoscaling, fractional GPU, multi-node deployments, and Multi-LLM workloads.
* **Increased initialization timeout for inference workloads** - The maximum initialization timeout for inference [workloads](/self-hosted/workloads-in-nvidia-run-ai/using-inference.md) and [templates](/self-hosted/workloads-in-nvidia-run-ai/workload-templates/inference-templates.md) in the UI has been increased to 720 minutes, allowing workloads with longer startup times, such as large models, to complete successfully without premature failure.
* **Model descriptions in NIM model selection** - The NIM model selection dropdown displays a short description beneath each model name, sourced from the NGC model card. AI practitioners can evaluate available models directly in the NVIDIA Run:ai UI without needing to look them up externally.
* **Trending model indicators in the Hugging Face model catalog** - The Hugging Face model catalog highlights trending models directly in the model selection dropdown. The top 20 trending models are marked with a trending indicator, making it easier to discover popular and emerging models alongside the most downloaded ones.
* **Delete predefined environment assets** - Users can delete predefined environment assets for inference workloads, `chatbot-ui`, `gpt2`, and `llm-server`, giving greater control over environment configuration.

### Command-line Interface (CLI v2) <a href="#command-line-interface-cli-v2-1" id="command-line-interface-cli-v2-1"></a>

* **User credentials support in the CLI** - Credentials configured in User settings (My Credentials) can now be managed through the CLI including creating, listing, and deleting credentials. Supported credential types include Generic, Docker registry, and NGC API keys. Credentials can also be used during workload submission as image pull secrets or environment variables, enabling a more streamlined and consistent submission workflow across the CLI, UI, and API. See [CLI command reference](/self-hosted/reference/cli/runai/runai-my-credential.md) for more details. `From cluster v2.22 onward`
* **Extended CLI support for YAML-based workloads -** The CLI supports additional operations for supported workload types submitted via YAML, including `runai workload-type list` and `runai workload-type describe`. This improves visibility and control over supported workload types without requiring access to the UI or direct interaction with Kubernetes resources. See [CLI command reference](/self-hosted/reference/cli/runai/runai-workload-type.md) for more details. `From cluster v2.23 onward`

## Platform Administrators

### Organizations - Projects/Departments

**New guided tour for projects and departments** - A built-in tour guides administrators through the projects and departments experience, highlighting key areas and workflows to help them get started quickly.

### Node Pools <a href="#authentication-and-authorization" id="authentication-and-authorization"></a>

**Time-based fairshare UI parameters** - Administrators can now configure key time-based fairshare parameters directly in the UI, including Historical usage weight and Historical usage window. Previously, these settings were only available through the node pool API. This makes it easier to tune how resource fairness is calculated based on historical and current usage, improving control over fairshare behavior without requiring API-level configuration. See [Node pools](/self-hosted/platform-management/aiinitiatives/resources/node-pools.md#adding-a-new-node-pool) for more details. `From cluster v2.24 onward`

### Authentication and Authorization <a href="#authentication-and-authorization" id="authentication-and-authorization"></a>

**Assign access rules during user and service account creation** - When creating a local [user](/self-hosted/infrastructure-setup/authentication/users.md#creating-a-local-user) or [service account](/self-hosted/infrastructure-setup/authentication/service-accounts.md#creating-a-service-account), you can optionally assign access rules directly within the creation flow. This step is only shown to users with permissions to manage access rules.

### Notifications

**Notifications API and Slack integration updates** - The notifications API was redesigned to provide a clearer and more structured model for managing notification state and channels. Email and Slack integrations are handled through dedicated APIs, replacing the previous unified notification channel endpoints. Slack integration is now fully supported through the UI across all deployment types, with the platform managing app creation, connection, and permissions. Legacy notification channel and Slack-specific endpoints are [deprecated](#api-deprecation-notifications) as part of this update. `From cluster v2.25 onward`

### Policies

**New blocked rule for workload policies** - A new `blocked` rule was added to workload policies, allowing administrators to prevent AI practitioners from specifying a value for a field. This can be used to lock security-related configurations from user modification without enforcing a specific default value (for example, supplemental groups). See [Policy YAML reference](/self-hosted/platform-management/policies/policy-yaml-reference.md#rule-types) for more details.

### Analytics <a href="#analytics" id="analytics"></a>

* **Permission-based access to the Overview dashboard** - The Overview dashboard is available to roles that have at least one of the relevant READ permissions listed below. Dashboard widgets and data are displayed according to each user's permissions, and widgets that are not applicable to the user's permissions are automatically hidden. This enhancement also supports custom roles with different permission sets.
  * Clusters READ
  * Node pools READ
  * Nodes READ
  * Projects READ
  * Departments READ
  * Workloads READ
* **Scope-aware filtering for over-time widgets** - Over-time widgets in the Overview dashboard now support scope-aware filtering by department or project. Users without full cluster permissions can select a single department or project within their allowed scope, and the widgets update accordingly. If only one department or project is available to the user, it is selected automatically. The Overview dashboard is now fully aware of the user’s scope and displays only relevant data.
* **Removal of legacy Grafana dashboards** - Legacy Grafana dashboards (Overview, Analytics, Consumption, and Multi-cluster), which were deprecated in v2.23, have been removed, along with their associated settings and permissions. The new dashboards provide equivalent functionality and are the recommended replacement.

### General Enhancements <a href="#general-enhancements" id="general-enhancements"></a>

* **UI inactivity timeout updates** - The **Session timeout** setting was renamed to **UI inactivity timeout**. If left blank, users are logged out after 24 hours of inactivity by default. CLI and API access remain unaffected. See [General settings](/self-hosted/settings/general-settings.md#security) for more details.
* **Sort by pod name in the Pods modal** - The Pods modal on both the [Nodes](/self-hosted/platform-management/aiinitiatives/resources/nodes.md#pods-associated-with-a-node) view and the [Workloads](/self-hosted/workloads-in-nvidia-run-ai/workloads.md#pods-associated-with-the-workload) view supports sorting by pod name.
* **Extended metrics time range for workloads** - The [Metrics](/self-hosted/workloads-in-nvidia-run-ai/workloads.md#metrics) view includes a **Since first run** option in the time range selector, displaying metrics from the first time a workload transitioned to the Running phase until the current time.

## Infrastructure Administrator

### Installation

* **NVIDIA Run:ai artifacts now available on NGC** - NVIDIA Run:ai artifacts are now published to NVIDIA NGC, including Helm charts, container images, CLI packages, air-gapped packages, and documentation. This provides a unified experience with other NVIDIA products, allowing customers to access and manage NVIDIA Run:ai software using the same NGC tools and credentials. JFrog support is now [deprecated](#jfrog-artifacts). Existing deployments will continue to work during the deprecation period, and customers are encouraged to migrate to NGC. See [Installation](/self-hosted/getting-started/installation.md) for more details. `From cluster v2.25 onward`
* **Host-based routing is now the default** - To support tools such as RStudio and Visual Studio Code without requiring additional configuration after installation, host-based routing is enabled by default. Workload URLs are exposed as subdomains, allowing workloads to run at the root path and avoiding file path issues. Kubernetes clusters require additional setup as part of system requirements configuration. OpenShift clusters require no additional configuration. Clusters upgrading from path-based routing are not affected. For setup instructions, see [System requirements](/self-hosted/getting-started/installation/install-using-helm/system-requirements.md#host-based-routing). For more details, see [External access to containers](/self-hosted/infrastructure-setup/advanced-setup/container-access/external-access-to-containers.md). `From cluster v2.25 onward`
* **Kubernetes Gateway API support** - NVIDIA Run:ai supports the Kubernetes Gateway API as a modern routing infrastructure, providing an alternative to Kubernetes Ingress. The feature is available as an opt-in option in v2.25 and can run alongside Ingress to enable zero-downtime migration. Ingress remains the default, with Gateway API expected to become the default in a future release. See [Kubernetes Gateway API](/self-hosted/infrastructure-setup/advanced-setup/kubernetes-gateway-api.md) for more details. `From cluster v2.25 onward`

### Cluster Configuration

**Vertical Pod Autoscaling (VPA) for cluster services** - NVIDIA Run:ai now supports configuring Vertical Pod Autoscaling (VPA) on cluster-level services to automatically right-size CPU and memory resources based on observed usage. VPA can be configured globally, per scaling group, or per component via `runaiconfig`, with multiple update modes including `Off` (recommendations only), `Initial`, `Auto`, and `InPlaceOrRecreate`. See [Vertical pod autoscaling](/self-hosted/infrastructure-setup/advanced-setup/vpa.md) for more details. `From cluster v2.25 onward`

### System Requirements <a href="#system-requirements" id="system-requirements"></a>

* NVIDIA Run:ai supports [OpenShift](/self-hosted/getting-started/installation/support-matrix.md#orchestration-platform-compatibility) version 4.21.
* NVIDIA Run:ai supports [Knative](/self-hosted/getting-started/installation/support-matrix.md#operator-and-framework-versions) version 1.19 to 1.21.
* NVIDIA Run:ai supports [GPU Operator](/self-hosted/getting-started/installation/support-matrix.md) version 26.3.
* NVIDIA Run:ai supports [Network Operator](/self-hosted/getting-started/installation/support-matrix.md) version 26.1.
* NVIDIA Run:ai supports [DRA driver](/self-hosted/getting-started/installation/support-matrix.md) version 25.15.
* Kubernetes version 1.32 is no longer supported.
* OpenShift version 4.17 is no longer supported.

## Deprecation Notifications

{% hint style="info" %}
**Note**

Deprecated features, APIs, and capabilities remain available for **two versions** from the time of the deprecation notice, after which they may be removed.
{% endhint %}

### JFrog Artifacts

Support for JFrog as an artifact registry is now deprecated. JFrog will continue to be supported for existing deployments, but it will be removed in a future release within approximately one year. Customers are encouraged to migrate to NVIDIA NGC, which is now the recommended artifact registry for NVIDIA Run:ai.

### TGI Server - Hugging Face

The Text Generation Inference (TGI) server used in the Hugging Face flow is deprecated. TGI is in maintenance mode and expected to reach end-of-life. Existing deployments will continue to work, but users should transition to other supported inference options.

### Administrator CLI

The Administrator CLI (`runai-adm`) is deprecated. The two tasks it supported are now handled as follows:

* **Log collection** - Use `runai diagnostics collect-logs` to collect diagnostic logs from the Kubernetes cluster for troubleshooting or sharing with NVIDIA Run:ai Support. See [CLI command reference](/self-hosted/reference/cli/runai/runai-diagnostics.md) for more details.
* **Node role management** - Use `kubectl` to configure node roles, which is already the recommended approach for node management. See [Node roles](/self-hosted/infrastructure-setup/advanced-setup/node-roles.md) for more details.

### Node Level Scheduler

The Node-level Scheduler feature is deprecated. This allows NVIDIA Run:ai to focus on more scalable and flexible GPU resource optimization capabilities. Existing deployments will continue to work, but the feature will be removed in a future release.

### Department Administrator Role

The previous Department administrator role has been deprecated and renamed to Department administrator legacy. A new Department administrator role replaces it with the same permissions, except it no longer includes Read Clusters access. Existing role assignments are not affected, as roles are referenced by ID in all APIs.

### API Deprecation Notifications <a href="#api-deprecation-notifications" id="api-deprecation-notifications"></a>

#### Deprecated Endpoints

| Deprecated Endpoint                                   | Replacement Endpoint                                                                           |
| ----------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| `/api/v1/token`                                       | `/api/v2/token`                                                                                |
| `POST /api/v1/notification-channels/slack/create-app` | `POST /api/v1/slack/app`                                                                       |
| `GET /api/v1/notification-channels/slack/add-app`     | `POST /api/v1/slack/workspace`                                                                 |
| `POST /api/v1/notification-channels/slack/auth-app`   | `GET /api/v1/slack/auth`                                                                       |
| `GET /api/v1/notification-state`                      | <p><code>GET /api/v1/email/state</code><br><code>GET /api/v1/slack/state</code></p>            |
| `PATCH /api/v1/notification-state`                    | <p><code>PATCH /api/v1/slack/state</code></p><p><code>PATCH /api/v1/email/state</code></p>     |
| `GET /api/v1/notification-state/detailed`             | `GET /api/v1/slack/state/detailed`                                                             |
| `POST /api/v1/validate-notification-channel`          | <p><code>POST /api/v1/slack/validate</code></p><p><code>POST /api/v1/email/validate</code></p> |
| `/api/v1/clusters/{clusterUuid}/nodes`                | `/api/v1/nodes`                                                                                |
| `/api/v1/org-unit/priorities`                         | `/api/v1/org-unit/ranks`                                                                       |
| `/api/v1/administration/user-applications`            | `/api/v1/administration/access-keys`                                                           |
| `/api/v1/administration/user-applications/{appId}`    | `/api/v1/administration/access-keys{accessKeyId}`                                              |

#### Deprecated Parameters

| Endpoint             | Deprecated Parameter    | Replacement Parameter                       |
| -------------------- | ----------------------- | ------------------------------------------- |
| `/api/v1/node-pools` | `overProvisioningRatio` | N/A                                         |
| `/api/v1/node-pools` | `placementStrategy`     | `schedulingConfiguration.placementStrategy` |
| `/api/v1/workloads`  | `externalConnections`   | `endpoints`                                 |
| `/api/v1/workloads`  | `urls`                  | `endpoints`                                 |


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://run-ai-docs.nvidia.com/self-hosted/getting-started/whats-new/whats-new-2-25.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
