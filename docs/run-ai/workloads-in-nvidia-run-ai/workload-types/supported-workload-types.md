# Supported Workload Types

NVIDIA Run:ai supports a broad range of workloads from the ML and Kubernetes ecosystem that are already registered as workload types in the platform and ready to use. These workloads are managed by the [Resource Interface](/self-hosted/workloads-in-nvidia-run-ai/workload-types/extending-workload-support.md#resource-interface-overview) (RI), which ensures they receive the same advanced scheduling, orchestration, and monitoring capabilities as NVIDIA Run:ai native workloads. For more details on feature support, see [Supported features](/self-hosted/workloads-in-nvidia-run-ai/workload-types/supported-features.md).

All supported workload types are pre-registered using the [Workload Types](https://run-ai-docs.nvidia.com/api/2.25/workloads/workload-properties#post-api-v1-workload-types) API. You can retrieve the full list of these workloads and their current configuration defaults.

{% hint style="info" %}
**Note**

To define and register workload types beyond those provided by NVIDIA Run:ai, see [Extending workload support with Resource Interface](/self-hosted/workloads-in-nvidia-run-ai/workload-types/extending-workload-support.md).
{% endhint %}

## List of Supported Workload Types

The following workload types are already registered in the platform and ready to use:

* **NVIDIA** - [NIM Services](https://docs.nvidia.com/nim-operator/latest/service.html), [DynamoGraphDeployment](https://docs.nvidia.com/dynamo/latest/index.html)
* **Kubernetes** - LeaderWorkerSet (LWS), Deployment, StatefulSet, ReplicaSet, Pod, CronJob, Job, JobSet ([kubernetes.io](https://kubernetes.io/))
* **Kubeflow** - TFJob, PyTorchJob, MPIJob, XGBoostJob, JAXJob, Notebook, ScheduledWorkflow ([kubeflow.org](http://kubeflow.org))
* **Ray** - RayService, RayCluster, RayJob ([ray.io](http://ray.io))
* **Tekton** - PipelineRun, TaskRun ([tekton.dev](http://tekton.dev))
* **Additional frameworks** - [SeldonDeployment](http://machinelearning.seldon.io), [AMLJob](https://learn.microsoft.com/en-us/cli/azure/ml/job?view=azure-cli-latest\&utm_source=chatgpt.com), [Workflow](http://argoproj.io), [DevWorkspace](http://workspace.devfile.io), [Service](http://serving.knative.dev), [VirtualMachineInstance](http://kubevirt.io/), InferenceService ([KServe](https://kserve.github.io/website/))

## Submitting Supported Workload Types

Supported workload types are submitted as standard Kubernetes YAML manifest&#x73;**.** Once submitted, the workload is created and appears in the [Workloads](/self-hosted/workloads-in-nvidia-run-ai/workloads.md) table for monitoring and management. See [Submit supported workload types via YAML](/self-hosted/workloads-in-nvidia-run-ai/submit-via-yaml.md).

## Workload Types and Defaults

Each workload type is assigned a default category, which determines its default priority and preemptibility. These defaults influence how workloads are scheduled and prioritized within a project, as well as how they are grouped for monitoring and reporting.

{% hint style="info" %}
**Note**

To retrieve the default category, priority and preemptibility per workload type, refer to the [List workload types](https://run-ai-docs.nvidia.com/api/2.25/workloads/workload-properties#get-api-v1-workload-types) API.
{% endhint %}

| Category | Default Priority | Default Preemptibility |
| -------- | ---------------- | ---------------------- |
| Build    | High             | Non-preemptible        |
| Train    | Low              | Preemptible            |
| Deploy   | Very high        | Non-preemptible        |

### Workload Types by Default Category

<table><thead><tr><th>Workload Type</th><th data-type="checkbox">Build</th><th data-type="checkbox">Train</th><th data-type="checkbox">Deploy</th></tr></thead><tbody><tr><td>AMLJob</td><td>false</td><td>true</td><td>false</td></tr><tr><td>CronJob</td><td>false</td><td>false</td><td>true</td></tr><tr><td>Deployment</td><td>false</td><td>false</td><td>true</td></tr><tr><td>DevWorkspace</td><td>true</td><td>false</td><td>false</td></tr><tr><td>DynamoGraphDeployment</td><td>false</td><td>false</td><td>true</td></tr><tr><td>InferenceService (KServe)</td><td>false</td><td>false</td><td>true</td></tr><tr><td>JAXJob</td><td>false</td><td>true</td><td>false</td></tr><tr><td>Job</td><td>true</td><td>false</td><td>false</td></tr><tr><td>JobSet</td><td>false</td><td>true</td><td>false</td></tr><tr><td>LeaderWorkerSet (LWS)</td><td>false</td><td>false</td><td>true</td></tr><tr><td>MPIJob</td><td>false</td><td>true</td><td>false</td></tr><tr><td>NIMCache</td><td>false</td><td>false</td><td>true</td></tr><tr><td>NIMServices</td><td>false</td><td>false</td><td>true</td></tr><tr><td>Notebook</td><td>true</td><td>false</td><td>false</td></tr><tr><td>PipelineRun</td><td>false</td><td>false</td><td>true</td></tr><tr><td>Pod</td><td>false</td><td>false</td><td>true</td></tr><tr><td>PyTorchJob</td><td>false</td><td>true</td><td>false</td></tr><tr><td>RayCluster</td><td>false</td><td>true</td><td>false</td></tr><tr><td>RayJob</td><td>false</td><td>true</td><td>false</td></tr><tr><td>RayService</td><td>false</td><td>false</td><td>true</td></tr><tr><td>ReplicaSet</td><td>false</td><td>false</td><td>true</td></tr><tr><td>ScheduledWorkflow</td><td>false</td><td>false</td><td>true</td></tr><tr><td>SeldonDeployment</td><td>false</td><td>false</td><td>true</td></tr><tr><td>Service</td><td>false</td><td>false</td><td>true</td></tr><tr><td>SPOTRequest</td><td>false</td><td>false</td><td>false</td></tr><tr><td>StatefulSet</td><td>false</td><td>false</td><td>true</td></tr><tr><td>TaskRun</td><td>true</td><td>false</td><td>false</td></tr><tr><td>TFJob</td><td>false</td><td>true</td><td>false</td></tr><tr><td>VirtualMachineInstance</td><td>false</td><td>true</td><td>false</td></tr><tr><td>Workflow</td><td>false</td><td>false</td><td>true</td></tr><tr><td>XGBoostJob</td><td>false</td><td>true</td><td>false</td></tr></tbody></table>

## Updating Default Category and Priority Mapping

Administrators can change the default priority and category assigned to a workload type by updating the mapping using the [NVIDIA Run:ai API](https://run-ai-docs.nvidia.com/api/2.25/):

* To update the priority mapping, see [Workload priority and preemption](/self-hosted/platform-management/runai-scheduler/scheduling/workload-priority-control.md#updating-the-default-mapping)
* To update the category mapping, see [Monitor workloads by category](/self-hosted/platform-management/monitor-performance/workload-categories.md#update-the-default-category-mapping)


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://run-ai-docs.nvidia.com/self-hosted/workloads-in-nvidia-run-ai/workload-types/supported-workload-types.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
