# Submit Supported Workload Types via YAML

This guide describes how to run supported workload types using the NVIDIA Run:ai UI by submitting a YAML manifest directly.

To learn more about workload types in NVIDIA Run:ai and determine what is the most suitable workload type for your goals, see [Workload types and features](/self-hosted/workloads-in-nvidia-run-ai/workload-types/supported-workload-types.md).

{% hint style="info" %}
**Note**

Workloads can be submitted using YAML outside of NVIDIA Run:ai (for example, with `kubectl`). For details, see [Supported features](/self-hosted/workloads-in-nvidia-run-ai/workload-types/supported-features.md#externally-submitted-kubernetes-workloads).
{% endhint %}

<figure><img src="/files/SuAW1dKGV2bAV71s4xmQ" alt=""><figcaption></figcaption></figure>

## Before You Start

Make sure you have created a [project](/self-hosted/platform-management/aiinitiatives/organization/projects.md) or have one created for you.

{% hint style="info" %}
**Note**

Via YAML submission is enabled by default. If you do not see it in the menu, contact your administrator to enable it under **General settings** → Workloads → Submit supported workload types via YAML.
{% endhint %}

## Supported Workload Types

Supported workload types include a broad range of workloads from the ML and Kubernetes ecosystem that are already registered as workload types in the platform and ready to use. See [Supported workload types](/self-hosted/workloads-in-nvidia-run-ai/workload-types/supported-workload-types.md) for more details.

* Your administrator can also register additional workload types for your organization. See [Registering new workload types](/self-hosted/workloads-in-nvidia-run-ai/workload-types/extending-workload-support.md#registering-new-workload-types) for more details.
* By default, workload types are grouped into Build, Train and Deploy categories. These categories determine how the workload is scheduled and prioritized within a project and how they are grouped for monitoring and reporting.

{% hint style="info" %}
**Note**

Some supported workload types require additional installation or cluster preparation before they can be used. Refer to the documentation for each workload type for specific prerequisites.
{% endhint %}

## Workload Priority and Preemption <a href="#workload-priority-class" id="workload-priority-class"></a>

By default, supported workload types are assigned a priority and preemptibility based on their workload type. These defaults determine how workloads are scheduled relative to others within the same project, whether they can use over-quota resources, and whether they may be interrupted once running. You can override the defaults by configuring priority and preemptibility. For more details on the default values per workload type, see [Workload types default](/self-hosted/workloads-in-nvidia-run-ai/workload-types/supported-workload-types.md#workload-types-defaults).

## Creating a New Workload

1. To create a workload, go to Workload manager → Workloads.
2. Click **+ NEW WORKLOAD** and select **Via YAML** from the dropdown.
3. In the YAML submission form, select the **cluster** where the workload will run.
4. Upload or paste your YAML manifest. Hover over **Supported workload types** to view a full list of available workloads:
   * To upload a file, click **UPLOAD YAML FILE** and choose your YAML.
   * To **paste the YAML**, insert it directly into the editor.
5. Select a **project**:
   * If the `namespace` is not defined in the YAML, select a **project** from the submission form. To create a new project, click **+NEW PROJECT** and refer to [Projects](/self-hosted/platform-management/aiinitiatives/organization/projects.md) for a step-by-step guide.
   * If a project is selected in the form, it **overrides** the `namespace` defined in the YAML.
   * Alternatively, set the project directly in the YAML using the `metadata.namespace` field.

     ```yaml
     metadata:
       namespace: my-project-name
     ```
6. Set whether the **workload may be interrupted**. Change this setting only if you want to override the default preemptibility defined for the workload type. Non-preemptible workloads use the project's available GPU quota and will not be interrupted once they start running. Preemptible workloads may be interrupted if resources are needed for higher priority workloads:
   * In the UI, select **Preemptible** or **Non-preemptible** from the dropdown.
   * In the YAML, set the following label under `metadata.labels`:

     ```yaml
     metadata:
       labels:
         kai.scheduler/preemptibility: non-preemptible
     ```
7. Set the **workload priority**. Change this setting only if you want to override the default priority defined for the workload type. Higher priority workloads are scheduled before lower-priority ones:
   * In the UI, select a **priority** from the dropdown.
   * In the YAML, set `priorityClassName` under `metadata.labels` using one of the supported values: `very-low`, `low`, `medium-low`, `medium`, `medium-high`, `high`, `very-high`:

     ```yaml
     metadata:
       labels:
         priorityClassName: high
     ```
8. If the project's node pools support MNNVL, set whether **Multi-Node NVLink (MNNVL) acceleration** is required for this workload. MNNVL provides high-bandwidth, low-latency communication between GPUs on supported nodes, improving performance for multi-GPU workloads:

   * **Not required** - The workload will not use MNNVL acceleration, even if MNNVL-capable nodes are available.
   * **Required** - The workload will require MNNVL-capable nodes. Scheduling may be restricted to compatible nodes, and if none are available, the workload may remain pending.

   For more information, see [Using GB200 NVL72 and Multi-Node NVLink Domains](/self-hosted/platform-management/aiinitiatives/resources/using-gb200.md).
9. Click **CREATE WORKLOAD**

## Managing and Monitoring

After the workload is created, it is added to the [Workloads](/self-hosted/workloads-in-nvidia-run-ai/workloads.md) table, where it can be managed and monitored.

## Accessing Workload Endpoints

NVIDIA Run:ai automatically discovers and displays network endpoints for workloads that include Kubernetes networking resources. For more information, see [Kubernetes Services, Load Balancing, and Networking](https://kubernetes.io/docs/concepts/services-networking/).

To expose endpoints, include the relevant networking configuration in your YAML. For example, the following Dynamo workload defines an Ingress that NVIDIA Run:ai will automatically discover:

```yaml
apiVersion: nvidia.com/v1alpha1
kind: DynamoGraphDeployment
metadata:
  name: secure-llm
spec:
  services:
    Frontend:
      dynamoNamespace: secure-llm
      componentType: frontend
      replicas: 1
      ingress:
        enabled: true
        host: api
        hostPrefix: llm-
        hostSuffix: runailabs.com
        ingressControllerClassName: haproxy
      extraPodSpec:
        mainContainer:
          image: nvcr.io/nvidia/ai-dynamo/vllm-runtime:1.0.1
```

Once the workload is running, the **Connections** column shows the endpoint URL directly if there is one, or the number of endpoints if there are multiple. See [Connections associated with the workload](/self-hosted/workloads-in-nvidia-run-ai/workloads.md#connections-associated-with-the-workload) for more details.

**Using an endpoint:**

* Click **Copy** to copy the URL to your clipboard.

**No endpoints displayed:**

If no endpoints appear, the workload may not yet be in a running state, or the networking configuration in your YAML manifest may not be set up correctly. Check the following:

* Verify the workload status is **Running**.
* Confirm that your YAML manifest includes the required networking configuration.
* Check that the networking configuration is correctly defined and applied.

## Using CLI

To view the available actions, see the [CLI v2 reference](/self-hosted/reference/cli/runai.md).

## Using API

To view the available actions, see the [Workloads V2](https://run-ai-docs.nvidia.com/api/2.25/workloads/workloads-v2) API reference.

## Troubleshooting

<details>

<summary>Generic or unknown errors</summary>

**Description:** Not specific enough to diagnose from the message alone.

```
Something went wrong
```

</details>

<details>

<summary>Authentication and permissions</summary>

**Description**: You may not be authorized to submit/manage workloads in the selected scope, or your token issuer is not recognized.

```
insufficient permissions
Issuer is not familiar
```

</details>

<details>

<summary>Cluster or API compatibility</summary>

**Description**: The API endpoint you used is not compatible with the target cluster version.

```
This API is incompatible with the version of cluster '<clusterId>'
```

</details>

<details>

<summary>Priority or category not available</summary>

**Description**: The selected priority or category isn’t supported in the target cluster.

```
category '<name>' is not available in this cluster
priority '<name>' is not available in this cluster
```

</details>

<details>

<summary>Workload name validation</summary>

**Description**: The workload name is missing, invalid, too long, or already exists.

```
Workload name must not be empty
The length of a workload name must not exceed 63 characters
The workload name must consist of lower case alphanumeric characters or '-', and start with an alphabetic character.
workload with name '<name>' already exists in this project
```

</details>

<details>

<summary>Project or cluster selection errors</summary>

**Description**: The request context is missing or ambiguous.

```
either projectId or clusterId must be provided
projectId and clusterId are mutually exclusive, provide only one
Failed to read request body
```

</details>

<details>

<summary>Workload type (GVK) not found or not ready in the cluster</summary>

**Description**: NVIDIA Run:ai can’t map your manifest’s **GVK** (group/version/kind) to a workload type that is registered and ready in the selected cluster. See [Supported workload types](/self-hosted/workloads-in-nvidia-run-ai/workload-types/supported-workload-types.md).

```
failed to extract resource info: <error>
failed to get workload types: <error>
workload type not found for GVK: <group>/<version>/<kind>
workload type has no cluster status information
workload type has no status information for cluster <clusterId> and version <version>
workload type phase is not available for this cluster
workload type is not ready in cluster <clusterId> (phase: <phase>) - <conditions>
```

</details>

<details>

<summary>Manifest structure and parsing errors</summary>

**Description**: The submitted YAML is not a valid Kubernetes-style manifest, or it can’t be parsed.

```
these are all the validations missing required field: apiVersion
missing required field: kind
manifest metadata is not a valid map
failed to convert YAML to JSON
failed to unmarshal JSON manifest
```

</details>


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://run-ai-docs.nvidia.com/self-hosted/workloads-in-nvidia-run-ai/submit-via-yaml.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
