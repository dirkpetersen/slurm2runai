# Monitor Workloads by Category

A workload category represents the role or purpose of a workload such as training, building, or deploying models. Each workload type is automatically assigned a default category to ensure consistent classification across the platform.

Categories appear in the Overview dashboard, allowing administrators to filter, group, and monitor workloads based on their function. Administrators can modify the default category mapping for a workload type using the NVIDIA Run:ai API.

## Default Category Mapping

NVIDIA Run:ai defines the following default mappings of workload types to categories. To retrieve the default category per workload type, refer to the [List workload types](https://run-ai-docs.nvidia.com/api/2.25/workloads/workload-properties#get-api-v1-workload-types) API.

{% hint style="info" %}
**Note**

* For more information on workload support, see [Introduction to workloads](/self-hosted/workloads-in-nvidia-run-ai/introduction-to-workloads.md).
* To see the default priority assigned to each of the workload types listed below, refer to [Workload priority control](/self-hosted/platform-management/runai-scheduler/scheduling/workload-priority-control.md).
  {% endhint %}

### NVIDIA Run:ai Native Workloads

<table><thead><tr><th>Workload Type</th><th data-type="checkbox">Build</th><th data-type="checkbox">Train</th><th data-type="checkbox">Deploy</th></tr></thead><tbody><tr><td>Workspaces</td><td>true</td><td>false</td><td>false</td></tr><tr><td>Standard training</td><td>false</td><td>true</td><td>false</td></tr><tr><td>Distributed training</td><td>false</td><td>true</td><td>false</td></tr><tr><td>Custom inference</td><td>false</td><td>false</td><td>true</td></tr><tr><td>NVIDIA NIM inference</td><td>false</td><td>false</td><td>true</td></tr><tr><td>Hugging Face inference</td><td>false</td><td>false</td><td>true</td></tr><tr><td>Distributed inference</td><td>false</td><td>false</td><td>true</td></tr></tbody></table>

### Supported Workload Types

<table><thead><tr><th>Workload Type</th><th data-type="checkbox">Build</th><th data-type="checkbox">Train</th><th data-type="checkbox">Deploy</th></tr></thead><tbody><tr><td>AMLJob</td><td>false</td><td>true</td><td>false</td></tr><tr><td>CronJob</td><td>false</td><td>false</td><td>true</td></tr><tr><td>Deployment</td><td>false</td><td>false</td><td>true</td></tr><tr><td>DevWorkspace</td><td>true</td><td>false</td><td>false</td></tr><tr><td>DynamoGraphDeployment</td><td>false</td><td>false</td><td>true</td></tr><tr><td>InferenceService (KServe)</td><td>false</td><td>false</td><td>true</td></tr><tr><td>JAXJob</td><td>false</td><td>true</td><td>false</td></tr><tr><td>Job</td><td>true</td><td>false</td><td>false</td></tr><tr><td>JobSet</td><td>false</td><td>true</td><td>false</td></tr><tr><td>LeaderWorkerSet (LWS)</td><td>false</td><td>false</td><td>true</td></tr><tr><td>MPIJob</td><td>false</td><td>true</td><td>false</td></tr><tr><td>NIMCache</td><td>false</td><td>false</td><td>true</td></tr><tr><td>NIMServices</td><td>false</td><td>false</td><td>true</td></tr><tr><td>Notebook</td><td>true</td><td>false</td><td>false</td></tr><tr><td>PipelineRun</td><td>false</td><td>false</td><td>true</td></tr><tr><td>Pod</td><td>false</td><td>false</td><td>true</td></tr><tr><td>PyTorchJob</td><td>false</td><td>true</td><td>false</td></tr><tr><td>RayCluster</td><td>false</td><td>true</td><td>false</td></tr><tr><td>RayJob</td><td>false</td><td>true</td><td>false</td></tr><tr><td>RayService</td><td>false</td><td>false</td><td>true</td></tr><tr><td>ReplicaSet</td><td>false</td><td>false</td><td>true</td></tr><tr><td>ScheduledWorkflow</td><td>false</td><td>false</td><td>true</td></tr><tr><td>SeldonDeployment</td><td>false</td><td>false</td><td>true</td></tr><tr><td>Service</td><td>false</td><td>false</td><td>true</td></tr><tr><td>SPOTRequest</td><td>false</td><td>false</td><td>false</td></tr><tr><td>StatefulSet</td><td>false</td><td>false</td><td>true</td></tr><tr><td>TaskRun</td><td>true</td><td>false</td><td>false</td></tr><tr><td>TFJob</td><td>false</td><td>true</td><td>false</td></tr><tr><td>VirtualMachineInstance</td><td>false</td><td>true</td><td>false</td></tr><tr><td>Workflow</td><td>false</td><td>false</td><td>true</td></tr><tr><td>XGBoostJob</td><td>false</td><td>true</td><td>false</td></tr></tbody></table>

## Update the Default Category Mapping

Administrators can change the default category assigned to a workload type by updating the category mapping using the [NVIDIA Run:ai API](https://run-ai-docs.nvidia.com/api/2.25/). To update the category mapping:

1. Retrieve the list of workload types and their IDs using `GET /api/v1/workload-types`.
2. Identify the `workloadTypeId` of the workload type you want to modify.
3. Retrieve the list of available categories and their IDs using `GET /api/v1/workload-categories`.
4. Send a request to update the workload type with the new category using\
   `PUT /api/v1/workload-types/{workloadTypeId}` and include the `categoryId` in the request body.

## Using API

Go to the [Workload properties](https://run-ai-docs.nvidia.com/api/2.25/workloads/workload-properties#get-api-v1-workload-categories) API reference to view the available actions.


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://run-ai-docs.nvidia.com/self-hosted/platform-management/monitor-performance/workload-categories.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
