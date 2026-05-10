# Workload Priority and Preemption

NVIDIA Run:ai defines workload priority and preemptibility to determine how workloads are scheduled within a project. These mechanisms influence scheduling order, resource allocation, and whether running workloads may be interrupted when higher-priority workloads require resources.

* **Workload priority** - Determines the workload's position in the project scheduling queue managed by the NVIDIA Run:ai [Scheduler](/self-hosted/platform-management/runai-scheduler/scheduling/how-the-scheduler-works.md). By adjusting the priority, you can increase the likelihood that a workload will be scheduled and preferred over others within the same project, ensuring that critical tasks are given higher priority and resources are allocated efficiently.
* **Workload preemptibility** - Determines the workload's resource usage policy and its guarantee against interruption:
  * Non-preemptible workloads must run within the project’s deserved quota, cannot use over-quota resources, and will not be interrupted once scheduled.
  * Preemptible workloads can use opportunistic resources beyond the project’s quota and may be interrupted at any time by higher priority workload, even if running within the project's quota.

{% hint style="info" %}
**Note**

This applies only within a single project. It does not impact the scheduling queues or workloads of other projects.
{% endhint %}

## Priority Dictionary

Workload priority is defined by selecting a priority from a predefined list in the NVIDIA Run:ai priority dictionary. Each string corresponds to a specific Kubernetes [PriorityClass](/self-hosted/platform-management/runai-scheduler/scheduling/concepts-and-principles.md#priority-and-preemption), which in turn determines scheduling behavior.

<table><thead><tr><th width="370.5078125">Priority Class Name</th><th>Kubernetes Priority Value</th></tr></thead><tbody><tr><td><code>very-low</code></td><td>25</td></tr><tr><td><code>low</code></td><td>40</td></tr><tr><td><code>medium-low</code></td><td>65</td></tr><tr><td><code>medium</code></td><td>80</td></tr><tr><td><code>medium-high</code></td><td>90</td></tr><tr><td><code>high</code></td><td>125</td></tr><tr><td><code>very-high</code></td><td>150</td></tr></tbody></table>

## Default Priority and Preemptibility per Workload

NVIDIA Run:ai defines the following default mappings of workload types to priorities and preemptibility. Each workload type comes with a default category that determines it default priority and preemptibility value. To retrieve the default priority and preemptibility per workload type, refer to the [List workload types](https://run-ai-docs.nvidia.com/api/2.25/workloads/workload-properties#get-api-v1-workload-types) API.

{% hint style="info" %}
**Note**

* For more information on workload support, see [Introduction to workloads](/self-hosted/workloads-in-nvidia-run-ai/introduction-to-workloads.md).
* Changing the priority is not supported for NVCF workloads.
  {% endhint %}

| Category | Default Priority | Default Preemptibility |
| -------- | ---------------- | ---------------------- |
| Build    | High             | Non-preemptible        |
| Train    | Low              | Preemptible            |
| Deploy   | Very high        | Non-preemptible        |

### NVIDIA Run:ai Native Workloads

<table><thead><tr><th>Workload Type</th><th data-type="checkbox">Build</th><th data-type="checkbox">Train</th><th data-type="checkbox">Deploy</th></tr></thead><tbody><tr><td>Workspaces</td><td>true</td><td>false</td><td>false</td></tr><tr><td>Standard training</td><td>false</td><td>true</td><td>false</td></tr><tr><td>Distributed training</td><td>false</td><td>true</td><td>false</td></tr><tr><td>Custom inference</td><td>false</td><td>false</td><td>true</td></tr><tr><td>NVIDIA NIM inference</td><td>false</td><td>false</td><td>true</td></tr><tr><td>Hugging Face inference</td><td>false</td><td>false</td><td>true</td></tr><tr><td>Distributed inference</td><td>false</td><td>false</td><td>true</td></tr></tbody></table>

### Supported Workload Types

<table><thead><tr><th>Workload Type</th><th data-type="checkbox">Build</th><th data-type="checkbox">Train</th><th data-type="checkbox">Deploy</th></tr></thead><tbody><tr><td>AMLJob</td><td>false</td><td>true</td><td>false</td></tr><tr><td>CronJob</td><td>false</td><td>false</td><td>true</td></tr><tr><td>Deployment</td><td>false</td><td>false</td><td>true</td></tr><tr><td>DevWorkspace</td><td>true</td><td>false</td><td>false</td></tr><tr><td>DynamoGraphDeployment</td><td>false</td><td>false</td><td>true</td></tr><tr><td>InferenceService (KServe)</td><td>false</td><td>false</td><td>true</td></tr><tr><td>JAXJob</td><td>false</td><td>true</td><td>false</td></tr><tr><td>Job</td><td>true</td><td>false</td><td>false</td></tr><tr><td>JobSet</td><td>false</td><td>true</td><td>false</td></tr><tr><td>LeaderWorkerSet (LWS)</td><td>false</td><td>false</td><td>true</td></tr><tr><td>MPIJob</td><td>false</td><td>true</td><td>false</td></tr><tr><td>NIMCache</td><td>false</td><td>false</td><td>true</td></tr><tr><td>NIMServices</td><td>false</td><td>false</td><td>true</td></tr><tr><td>Notebook</td><td>true</td><td>false</td><td>false</td></tr><tr><td>PipelineRun</td><td>false</td><td>false</td><td>true</td></tr><tr><td>Pod</td><td>false</td><td>false</td><td>true</td></tr><tr><td>PyTorchJob</td><td>false</td><td>true</td><td>false</td></tr><tr><td>RayCluster</td><td>false</td><td>true</td><td>false</td></tr><tr><td>RayJob</td><td>false</td><td>true</td><td>false</td></tr><tr><td>RayService</td><td>false</td><td>false</td><td>true</td></tr><tr><td>ReplicaSet</td><td>false</td><td>false</td><td>true</td></tr><tr><td>ScheduledWorkflow</td><td>false</td><td>false</td><td>true</td></tr><tr><td>SeldonDeployment</td><td>false</td><td>false</td><td>true</td></tr><tr><td>Service</td><td>false</td><td>false</td><td>true</td></tr><tr><td>SPOTRequest</td><td>false</td><td>false</td><td>false</td></tr><tr><td>StatefulSet</td><td>false</td><td>false</td><td>true</td></tr><tr><td>TaskRun</td><td>true</td><td>false</td><td>false</td></tr><tr><td>TFJob</td><td>false</td><td>true</td><td>false</td></tr><tr><td>VirtualMachineInstance</td><td>false</td><td>true</td><td>false</td></tr><tr><td>Workflow</td><td>false</td><td>false</td><td>true</td></tr><tr><td>XGBoostJob</td><td>false</td><td>true</td><td>false</td></tr></tbody></table>

## Setting Priority and Preemptibility During Workload Submission

{% hint style="info" %}
**Note**

* If preemptibility is not explicitly configured, the system uses the default preemptibility behavior associated with the selected workload priority.
* Changing a workload’s priority and preemptibility may impact its ability to be scheduled. For example, switching a workload from a low priority, preemptible value (which allows over-quota usage) to high priority, non-preemptible value (which requires in-quota resources) may reduce its chances of being scheduled in cases where the required quota is unavailable.
  {% endhint %}

### NVIDIA Run:ai Native Workloads

For native NVIDIA Run:ai workloads, priority and preemptibility can be set during workload submission using one of the following methods:

* **UI** - Set workload priority and preemptibility under **General** settings
* **API** - Set using the `priorityClass` and `preemptibility` field
* **CLI** - Set using the `--priority` and `--preemptibility` flag

### Supported Workload Types

{% hint style="info" %}
**Note**

If priority or preemptibility is set through the UI, API, or CLI, those values override any values defined in the YAML manifest.
{% endhint %}

For [supported workload types](/self-hosted/workloads-in-nvidia-run-ai/workload-types/supported-workload-types.md) submitted with a YAML manifest, priority and preemptibility can be set as follows:

* **UI** - Set workload priority and preemptibility under **General** settings
* **API** - Set using the `priority` and `preemptibility` fields
* **CLI** - Set using the `--priority` and `--preemptibility` flags
* **via YAML manifest** - Set by adding the following labels to your YAML manifest under the `metadata.labels` section of your workload definition.
  * Use the following values for priority - `very-low`, `low`, `medium-low`, `medium`, `medium-high`, `high`, `very-high` :
  * Use the following values for preemptibility - `preemptible` or `non-preemptible`

    ```yaml
    metadata:
      labels:
        priorityClassName: <priority>
        kai.scheduler/preemptibility: <preemptibility_value>
    ```

## Updating the Default Mapping

Administrators can change the default priority and preemptibility assigned to a workload type by updating the mapping using the [NVIDIA Run:ai API](https://run-ai-docs.nvidia.com/api/2.25/). To update the priority mapping:

1. Retrieve the list of workload types and their IDs using `GET /api/v1/workload-types`.
2. Identify the `workloadTypeId` of the workload type you want to modify.
3. Retrieve the list of available priorities and their IDs using `GET /api/v1/workload-priorities`.
4. Send a request to update the workload type with the new priority using\
   `PUT /api/v1/workload-types/{workloadTypeId}` and include the `priorityId` in the request body.

## Using API

Go to the [Workload priorities](https://run-ai-docs.nvidia.com/api/2.25/workloads/workload-properties#get-api-v1-workload-priorities) API reference to view the available actions.


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://run-ai-docs.nvidia.com/self-hosted/platform-management/runai-scheduler/scheduling/workload-priority-control.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
