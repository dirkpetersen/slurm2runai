# Scheduling Rules

Scheduling rules are restrictions applied to workloads. These restrictions apply to either the resources (nodes) on which workloads can run or the duration of the run time. Scheduling rules are set for [Projects](/self-hosted/platform-management/aiinitiatives/organization/projects.md) or [Departments](/self-hosted/platform-management/aiinitiatives/organization/departments.md) and apply to specific workload types. Once scheduling rules are set for a project or department, all matching workloads associated with the project have the restrictions applied to them, as defined, when the workload was submitted. New scheduling rules added to a project are not applied over previously created workloads associated with that project.

## Workload Duration (Time Limit)

This rule limits the duration of a workload run time. Workload run time is calculated as the total time in which the workload was in status Running. You can apply a single rule per workload type - Preemptible Workspaces, Non-preemptible Workspaces, and Training.

## Idle GPU Time Limit

This rule limits the total GPU time of a workload. Workload idle time is counted from the first time the workload is in status Running and the GPU was idle. Idleness is calculated by employing the `runai_gpu_idle_seconds_per_workload` metric. This metric determines the total duration of zero GPU utilization within each 30-second interval. If the GPU remains idle throughout the 30-second window, 30 seconds are added to the idleness sum; otherwise, the idleness count is reset. You can apply a single rule per workload type - “Preemptible” Workspaces, “Non-preemptible” Workspaces, and Training.

{% hint style="info" %}
**Note**

To make Idle GPU timeout effective, it must be set to a shorter duration than the workload duration of the same workload type.
{% endhint %}

## Node Type (Affinity)

Node type is used to select a group of nodes, typically with specific characteristics such as a hardware feature, storage type, fast networking interconnection, etc. The [Scheduler](/self-hosted/platform-management/runai-scheduler/scheduling/how-the-scheduler-works.md) uses node type as an indication of which nodes should be used for your workloads, within this project.

Node type is a label in the form of `run.ai/type` and a value (e.g. run.ai/type = dgx200) that the administrator uses to tag a set of nodes. Adding the node type to the project’s scheduling rules mandates the user to submit workloads with a node type label/value pairs from this list, according to the workload type - Workspace or Training. The Scheduler then schedules workloads using a node selector, targeting nodes tagged with the NVIDIA Run:ai node type label/value pair. Node pools and a node type can be used in conjunction. For example, specifying a node pool and a smaller group of nodes from that node pool that includes a fast SSD memory or other unique characteristics.

### Labelling Nodes for Node Types Grouping

The administrator should use a node label with the key of `run.ai/type` and any coupled value

To assign a label to nodes you want to group, set the ‘node type (affinity)’ on each relevant node:

1. Obtain the list of nodes and their current labels by copying the following to your terminal:

```bash
kubectl get nodes --show-labels
```

2. Annotate a specific node with a new label by copying the following to your terminal:

```bash
kubectl label node <node-name> run.ai/type=<value>
```


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://run-ai-docs.nvidia.com/self-hosted/platform-management/policies/scheduling-rules.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
