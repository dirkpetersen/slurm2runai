# Introduction to Workloads

NVIDIA Run:ai enhances visibility and simplifies [management](/self-hosted/workloads-in-nvidia-run-ai/workloads.md), by monitoring, presenting and orchestrating all AI workloads in the clusters it is installed. Workloads are the fundamental building blocks for consuming resources, enabling AI practitioners such as researchers, data scientists and engineers to efficiently support the entire life cycle of an [AI initiative](/self-hosted/platform-management/aiinitiatives/adapting-ai-initiatives.md).

## Workloads Across the AI Life cycle

A typical AI initiative progresses through several key stages, each with distinct workloads and objectives. With NVIDIA Run:ai, research and engineering teams can host and manage all these workloads to achieve the following:

* **Data preparation:** Aggregating, cleaning, normalizing, and labeling data to prepare for training.
* **Training:** Conducting resource-intensive model development and iterative performance optimization.
* **Fine-tuning:** Adapting pre-trained models to domain-specific datasets while balancing efficiency and performance.
* **Inference:** Deploying models for real-time or batch predictions with a focus on low latency and high throughput.
* **Monitoring and optimization:** Ensuring ongoing performance by addressing data drift, usage patterns, and retraining as needed.

## What Is a Workload?

A workload runs in the cluster, is associated with a namespace, and operates to fulfill its targets, whether that is running to completion for a [batch job](/self-hosted/workloads-in-nvidia-run-ai/workload-types.md#training-scaling-resources-for-model-development), allocating resources for [experimentation](/self-hosted/workloads-in-nvidia-run-ai/workload-types.md#workspaces-the-experimentation-phase) in an integrated development environment (IDE)/notebook, or serving [inference](/self-hosted/workloads-in-nvidia-run-ai/workload-types.md#inference-deploying-and-serving-models) requests in production.

The workload, defined by the AI practitioner, consists of:

* **Container images:** This includes the application, its dependencies, and the runtime environment.
* **Compute resources:** CPU, GPU, and RAM to execute efficiently and address the workload’s needs.
* **Data & storage configuration:** The data needed for processing such as training and testing datasets or input from external databases, and the storage configuration which refers to the way this data is managed, stored and accessed.
* **Credentials:** The access to certain data sources or external services, ensuring proper authentication and authorization.

## Workload Scheduling and Orchestration

NVIDIA Run:ai’s core mission is to optimize AI resource usage at scale. This is achieved through efficient [scheduling and orchestrating](/self-hosted/platform-management/runai-scheduler/scheduling/how-the-scheduler-works.md) of all cluster workloads using the NVIDIA Run:ai [Scheduler](/self-hosted/platform-management/runai-scheduler/scheduling/concepts-and-principles.md). The Scheduler allows the prioritization of workloads across different departments and projects within the organization at large scales, based on the resource distribution set by the system administrator.

## Workloads in NVIDIA Run:ai <a href="#types-of-workloads-in-runai" id="types-of-workloads-in-runai"></a>

Workloads in NVIDIA Run:ai can be either built into the platform or brought in from any ML framework, tool, or the broader Kubernetes ecosystem. All workloads benefit from platform-level features such as scheduling, monitoring, and orchestration. For a list of feature support across workloads, see [Supported features](/self-hosted/workloads-in-nvidia-run-ai/workload-types/supported-features.md).

### NVIDIA Run:ai Native Workloads

These are the native platform workload types provided by NVIDIA Run:ai - Workspaces, Training, and Inference. They are submitted directly from the NVIDIA Run:ai platform and are represented by Kubernetes Custom Resource Definitions (CRDs) and APIs. Native workloads include built-in support for orchestration, scheduling, and policy controls, ensuring optimization, governance, and security standards. These workloads are fully integrated and immediately available as part of the platform. See [NVIDIA Run:ai native workloads](/self-hosted/workloads-in-nvidia-run-ai/workload-types/native-workloads.md) for more details.

### Extending Supported Workload Types with Resource Interface

NVIDIA Run:ai enables support for workload types that originate from any ML framework, tool, or the broader Kubernetes ecosystem. These workloads can be managed and monitored directly through the NVIDIA Run:ai platform, allowing seamless integration with external tools and providing teams flexibility to deploy and scale various ML frameworks alongside NVIDIA Run:ai native workloads.

Some workload types are already available in the platform, ready to use with default category and priority mappings applied. See [Supported workload types](/self-hosted/workloads-in-nvidia-run-ai/workload-types/supported-workload-types.md) for a full list.

Administrators can extend workload support by introducing new workload types at any time using the [Workload Types](https://run-ai-docs.nvidia.com/api/2.25/workloads/workload-properties#post-api-v1-workload-types) API. The Resource Interface (RI) infrastructure interprets and manages these workloads, enabling advanced orchestration, scheduling, and monitoring. See [Extending workload support with Resource Interface](/self-hosted/workloads-in-nvidia-run-ai/workload-types/extending-workload-support.md) for more details.


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://run-ai-docs.nvidia.com/self-hosted/workloads-in-nvidia-run-ai/introduction-to-workloads.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
