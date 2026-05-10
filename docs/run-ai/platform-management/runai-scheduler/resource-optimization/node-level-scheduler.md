# Optimize Performance with Node Level Scheduler

{% hint style="info" %}
**Note**

Node Level Scheduler has been deprecated and will be removed in a future release.
{% endhint %}

The Node Level Scheduler optimizes the performance of your pods and maximizes the utilization of GPUs by making optimal local decisions on GPU allocation to your pods. While the [NVIDIA Run:ai Scheduler](/self-hosted/platform-management/runai-scheduler/scheduling/how-the-scheduler-works.md) chooses the specific node for a pod, it has no visibility to the node’s GPUs' internal state. The Node Level Scheduler is aware of the local GPUs' states and makes optimal local decisions such that it can optimize both the GPU utilization and pods’ performance running on the node’s GPUs.

This guide provides an overview of the best use cases for the Node Level Scheduler and instructions for configuring it to maximize GPU performance and pod efficiency.

## Deployment Considerations

* While the Node Level Scheduler applies to all [workload types](/self-hosted/workloads-in-nvidia-run-ai/workload-types.md), it will best optimize the performance of burstable workloads. Burstable workloads are workloads that use [dynamic GPU fractions](/self-hosted/platform-management/runai-scheduler/resource-optimization/dynamic-fractions.md), giving those more GPU memory than requested and up to the Limit specified.
* Burstable workloads are always susceptible to an OOM Kill signal if the owner of the excess memory requires it back. This means that using the Node Level Scheduler with inference or training workloads may cause pod preemption.
* Using interactive workloads with notebooks is the best use case for burstable workloads and Node Level Scheduler. These workloads behave differently since the OOM Kill signal will cause the notebooks' GPU process to exit but not the notebook itself. This keeps the interactive pod running and retrying to attach a GPU again.

## Interactive Notebooks Use Case

This use case is one scenario that shows how Node Level Scheduler locally optimizes and maximizes GPU utilization and workspaces’ performance.

1. The below shows a node with 2 GPUs and 2 submitted workspaces:

![Unallocated GPU nodes](/files/wjASw3RozY0ZEzwN5N6k)

2. The Scheduler instructs the node to put the 2 workspaces on a single GPU, [bin-packing](/self-hosted/platform-management/aiinitiatives/resources/node-pools.md#adding-a-new-node-pool) a single GPU and leaving the other free for a workload that requires resources. This means GPU#2 is idle while the two workspaces can only use up to half a GPU, even if they temporarily need more:

![Single allocated GPU node](/files/i650iIsrzmpRKG2f9xtm)

3. With the Node Level Scheduler enabled, the local decision will be to spread those 2 workspaces on 2 GPUs and allow them to maximize both workspaces’ performance and GPUs’ utilization by bursting out up to the full GPU memory and GPU compute resources:

![Two allocated GPU nodes](/files/UTwseex56BHrseL0xoEY)

4. The NVIDIA Run:ai Scheduler still sees a node with one fully empty GPU and one fully occupied GPU. When a 3rd workload is scheduled, and it requires a full GPU (or more than 0.5 GPU), the Scheduler will schedule it to that node, and the Node Level Scheduler will move one of the workspaces to run with the other in GPU#1, as was the Scheduler’s initial plan. Moving the workspace from GPU#1 back to GPU#2 maintains the workspace running while the GPU process within the Jupyter notebook is killed and re-established on GPU#2, continuing to serve the workspace:

![Node Level Scheduler locally optimized GPU nodes](/files/Zrr46Af0rOuYT1rOicSq)

## Using Node Level Scheduler

The Node Level Scheduler can be enabled per node pool. To use Node Level Scheduler, follow the below steps.

### Enable on Your Cluster

Enable the Node Level Scheduler at the cluster level (per cluster):

1. **Using Helm** - Set the following value in your `values.yaml` file under `clusterConfig` and upgrade the chart:

   <pre class="language-yaml"><code class="lang-yaml">clusterConfig: 
   <strong>  global: 
   </strong>      core: 
           nodeScheduler:
             enabled: true
   </code></pre>
2. **Using runaiconfig at runtime** - Use the following `kubectl` patch command:

   ```bash
   kubectl patch -n runai runaiconfigs.run.ai/runai --type='merge' --patch '{"spec":{"global":{"core":{"nodeScheduler":{"enabled": true}}}}}'
   ```

See [Advanced cluster configurations](/self-hosted/infrastructure-setup/advanced-setup/cluster-config.md) for more details.

### Enable on a Node Pool

{% hint style="info" %}
**Note**

GPU resource optimization is disabled by default. It must be enabled by your Administrator, under **General Settings** → Resources → GPU resource optimization.
{% endhint %}

Enable Node Level Scheduler on any of the node pools:

1. Select Resources → Node pools
2. [Create a new node pool](/self-hosted/platform-management/aiinitiatives/resources/node-pools.md#adding-a-new-node-pool) or [edit an existing node pool](/self-hosted/platform-management/aiinitiatives/resources/node-pools.md#editing-a-node-pool)
3. Under the **Resource Utilization Optimization** tab, change the **number of workloads on each GPU** to any value other than **Not Enforced** (i.e. 2, 3, 4, 5)

The Node Level Scheduler is now ready to be used on that node pool.

### Submit a Workload

In order for a workload to be considered by the Node Level Scheduler for rerouting, it must be submitted with a GPU Request and Limit where the Limit is larger than the Request:

* Enable and set [dynamic GPU fractions](/self-hosted/platform-management/runai-scheduler/resource-optimization/dynamic-fractions.md)
* Then [submit a workload](/self-hosted/workloads-in-nvidia-run-ai/workloads.md) using dynamic GPU fractions


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://run-ai-docs.nvidia.com/self-hosted/platform-management/runai-scheduler/resource-optimization/node-level-scheduler.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
