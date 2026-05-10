# Supported Features

This page compares feature support across different workload types in NVIDIA Run:ai. Use it to understand which scheduling, resource management, and platform capabilities are available for each workload type before selecting a workload model or submission method.

* [Native workloads](/self-hosted/workloads-in-nvidia-run-ai/workload-types/native-workloads.md) - Fully integrated into the platform - Workspace, Training and Inference.
* [Supported workload types](/self-hosted/workloads-in-nvidia-run-ai/workload-types/supported-workload-types.md) - A broad range of workloads from the ML and Kubernetes ecosystem enabled through the Resource Interface (RI).
* [Externally submitted Kubernetes workloads](#externally-submitted-kubernetes-workloads) - Workloads submitted outside of NVIDIA Run:ai. These workloads receive only minimal scheduling and platform capabilities.

Feature availability may vary across NVIDIA Run:ai versions and cluster deployments. Refer to this page and the linked documentation for the most up-to-date support details.

## Workload Submission <a href="#workload-submission-methods" id="workload-submission-methods"></a>

<table><thead><tr><th></th><th data-type="checkbox">Workspace</th><th data-type="checkbox">Standard Training</th><th data-type="checkbox">Distributed Training</th><th data-type="checkbox">Inference</th><th data-type="checkbox">Distributed Inference</th><th data-type="checkbox">Supported workload types</th></tr></thead><tbody><tr><td>UI</td><td>true</td><td>true</td><td>true</td><td>true</td><td>true</td><td>false</td></tr><tr><td>UI (via YAML)</td><td>false</td><td>false</td><td>false</td><td>false</td><td>false</td><td>true</td></tr><tr><td>API (Workloads v1)</td><td>true</td><td>true</td><td>true</td><td>true</td><td>true</td><td>false</td></tr><tr><td>API (Workloads v2)</td><td>false</td><td>false</td><td>false</td><td>false</td><td>false</td><td>true</td></tr><tr><td>CLI</td><td>true</td><td>true</td><td>true</td><td>true</td><td>true</td><td>true</td></tr></tbody></table>

## Scheduling and Resource Management

<table><thead><tr><th>Functionality</th><th data-type="checkbox">Workspace</th><th data-type="checkbox">Standard Training</th><th data-type="checkbox">Distributed Training</th><th data-type="checkbox">Inference</th><th data-type="checkbox">Distributed Inference</th><th data-type="checkbox">Supported workload types</th></tr></thead><tbody><tr><td><a href="/pages/0Zh8e1AF0MDFy3pRR8B9#fairness-fair-resource-distribution">Fairness</a></td><td>true</td><td>true</td><td>true</td><td>true</td><td>true</td><td>true</td></tr><tr><td><a href="/pages/0Zh8e1AF0MDFy3pRR8B9#priority-and-preemption">Priority and preemption</a></td><td>true</td><td>true</td><td>true</td><td>true</td><td>true</td><td>true</td></tr><tr><td><a href="/pages/0Zh8e1AF0MDFy3pRR8B9#over-quota">Over quota</a></td><td>true</td><td>true</td><td>true</td><td>true</td><td>true</td><td>true</td></tr><tr><td><a href="/pages/daynclyBQ5PgNGDd6VXx">Node pools</a></td><td>true</td><td>true</td><td>true</td><td>true</td><td>true</td><td>true</td></tr><tr><td><a href="/pages/0Zh8e1AF0MDFy3pRR8B9#placement-strategy-bin-pack-and-spread">Bin packing / Spread</a></td><td>true</td><td>true</td><td>true</td><td>true</td><td>true</td><td>true</td></tr><tr><td><a href="/pages/QUlh6zKg2ym96UblcVfl">Multi-GPU fractions</a></td><td>true</td><td>true</td><td>true</td><td>true</td><td>true</td><td>true</td></tr><tr><td><a href="/pages/8sXJJ3wnbd8YfnKlngoZ">Multi-GPU dynamic fractions</a></td><td>true</td><td>true</td><td>true</td><td>true</td><td>true</td><td>true</td></tr><tr><td><a href="/pages/mikyn4oeWVLjmsFxC7wI">Node level scheduler</a></td><td>true</td><td>true</td><td>true</td><td>true</td><td>true</td><td>true</td></tr><tr><td><a href="/pages/ovx0MZwzzIpmPPuI1xPl">Multi-GPU memory swap</a></td><td>true</td><td>true</td><td>true</td><td>true</td><td>true</td><td>true</td></tr><tr><td>Elastic scaling</td><td>false</td><td>false</td><td>true</td><td>true</td><td>true</td><td>true</td></tr><tr><td><a href="/pages/0Zh8e1AF0MDFy3pRR8B9#gang-scheduling">Gang scheduling</a></td><td>true</td><td>true</td><td>true</td><td>true</td><td>true</td><td>true</td></tr><tr><td><a href="/pages/MctnJAQFLLC3UwXrmyLj">Network topology-aware scheduling</a></td><td>false</td><td>false</td><td>true</td><td>false</td><td>true</td><td>true</td></tr><tr><td><a href="/pages/4te5ws3qWvt0ccTELALc">GB200 NVL72 and Multi-Node NVLink domains (MNNVL)</a></td><td>false</td><td>false</td><td>true</td><td>false</td><td>true</td><td>true</td></tr><tr><td><a href="/pages/Kj4Ukxn88PZF4QFjdUfF">Scheduling rules</a></td><td>true</td><td>true</td><td>true</td><td>true</td><td>false</td><td>false</td></tr></tbody></table>

## Operational and Platform Features

<table><thead><tr><th>Functionality</th><th data-type="checkbox">Workspace</th><th data-type="checkbox">Standard Training</th><th data-type="checkbox">Distributed Training</th><th data-type="checkbox">Inference</th><th data-type="checkbox">Distributed Inference</th><th data-type="checkbox">Supported workload types</th></tr></thead><tbody><tr><td><a href="/pages/pCzDnVqJYX8k8aVibNJF">Monitoring</a></td><td>true</td><td>true</td><td>true</td><td>true</td><td>true</td><td>true</td></tr><tr><td>Workload awareness</td><td>true</td><td>true</td><td>true</td><td>true</td><td>true</td><td>true</td></tr><tr><td><a href="/pages/zCk8XJ5nMmNsOHWFTcNz#role-based-access-control-rbac-in-run-ai">RBAC</a></td><td>true</td><td>true</td><td>true</td><td>true</td><td>true</td><td>true</td></tr><tr><td><a href="/pages/f1sAxzJehoBYpAMir3LF">Workload actions (stop/run)</a></td><td>true</td><td>true</td><td>true</td><td>false</td><td>false</td><td>false</td></tr><tr><td><a href="/pages/Muk0hdGJ2rTpWgFqheYG">Rolling updates</a></td><td>false</td><td>false</td><td>false</td><td>true</td><td>false</td><td>false</td></tr><tr><td><a href="/pages/UNR3wY6mBjsKurlgvvRV">Workload templates</a></td><td>true</td><td>true</td><td>true</td><td>true</td><td>false</td><td>false</td></tr><tr><td><a href="/pages/VZHRkU7LnGdbh7nafDiJ">Workload assets</a></td><td>true</td><td>true</td><td>true</td><td>true</td><td>false</td><td>false</td></tr><tr><td><a href="/pages/D6XcXxyPPPBqTAmlE2ho">Workload Policies</a></td><td>true</td><td>true</td><td>true</td><td>true</td><td>true</td><td>false</td></tr></tbody></table>

{% hint style="info" %}
**Workload awareness**

Specific workload-aware visibility, so that different pods are identified and treated as a single workload (for example GPU utilization, workload view, dashboards).
{% endhint %}

## Externally Submitted Kubernetes Workloads

Kubernetes workloads can be submitted outside of NVIDIA Run:ai, for example by using `kubectl` directly or Helm charts as part of an [AI application](/self-hosted/ai-applications/ai-applications.md). These workloads are scheduled by NVIDIA Run:ai and receive full monitoring support, along with a subset of scheduling capabilities.

* Supported scheduling capabilities include:
  * [Fairness](/self-hosted/platform-management/runai-scheduler/scheduling/concepts-and-principles.md#fairness-fair-resource-distribution)
  * [Priority and preemption](/self-hosted/platform-management/runai-scheduler/scheduling/concepts-and-principles.md#priority-and-preemption)
  * [Over quota](/self-hosted/platform-management/runai-scheduler/scheduling/concepts-and-principles.md#over-quota)
  * [Node pools](/self-hosted/platform-management/aiinitiatives/resources/node-pools.md)
  * [Bin packing / Spread](/self-hosted/platform-management/runai-scheduler/scheduling/concepts-and-principles.md#placement-strategy-bin-pack-and-spread)
  * [Multi-GPU fractions](/self-hosted/platform-management/runai-scheduler/resource-optimization/fractions.md)
  * [Multi-GPU dynamic fractions](/self-hosted/platform-management/runai-scheduler/resource-optimization/dynamic-fractions.md)
  * [Node level scheduler](/self-hosted/platform-management/runai-scheduler/resource-optimization/node-level-scheduler.md)
  * [Multi-GPU memory swap](/self-hosted/platform-management/runai-scheduler/resource-optimization/memory-swap.md)
  * [Gang scheduling](/self-hosted/platform-management/runai-scheduler/scheduling/concepts-and-principles.md#gang-scheduling)
* All [monitoring](/self-hosted/workloads-in-nvidia-run-ai/workloads.md#show-hide-details) capabilities are supported including event history, metrics and logs.


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://run-ai-docs.nvidia.com/self-hosted/workloads-in-nvidia-run-ai/workload-types/supported-features.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
