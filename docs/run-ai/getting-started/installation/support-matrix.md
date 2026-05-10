# Support Matrix

The support matrix outlines the verified compatibility standards for NVIDIA Run:ai v2.25. To ensure a stable and performant deployment, all infrastructure components, including Kubernetes/OpenShift distributions, NVIDIA Operators, and specialized frameworks, must align with the versions specified below. Use this matrix as a validation checklist prior to performing new installations or upgrades.

## Operator and Framework Versions <a href="#operator-and-framework-versions" id="operator-and-framework-versions"></a>

| Component                                                                                                                                              | Supported Versions   |
| ------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------- |
| [NVIDIA GPU Operator](/self-hosted/getting-started/installation/install-using-helm/system-requirements.md#nvidia-gpu-operator)                         | 25.10 - 26.3         |
| [NVIDIA Network Operator](/self-hosted/getting-started/installation/install-using-helm/system-requirements.md#nvidia-network-operator)                 | 25.10 - 26.1         |
| [NVIDIA DRA driver](/self-hosted/getting-started/installation/install-using-helm/system-requirements.md#nvidia-dynamic-resource-allocation-dra-driver) | 25.8 - 25.12         |
| [Prometheus / Kube‑Prometheus Stack](/self-hosted/getting-started/installation/install-using-helm/system-requirements.md#prometheus)                   | 3.5 / 76.0 and above |
| [Kubeflow Training Operator](/self-hosted/getting-started/installation/install-using-helm/system-requirements.md#distributed-training)                 | 1.9.2                |
| [MPI Operator](/self-hosted/getting-started/installation/install-using-helm/system-requirements.md#distributed-training)                               | 0.6.0 or later       |
| [Knative Serving](/self-hosted/getting-started/installation/install-using-helm/system-requirements.md#inference)                                       | 1.19 - 1.21          |
| [Leader-Worker Set (LWS)](/self-hosted/getting-started/installation/install-using-helm/system-requirements.md#distributed-inference)                   | 0.7.0 or higher      |

## Supported NVIDIA GPUs

NVIDIA Run:ai v2.25 is compatible with all Data Center GPUs supported by the NVIDIA GPU Operator. Hardware compatibility is determined by the specific version of the GPU Operator deployed within your cluster.

* Supported operator range - NVIDIA Run:ai v2.25 supports GPU Operator versions 25.3 through 25.10.
* Hardware verification - To confirm if a specific GPU model is supported, please cross-reference your Operator version with the [Supported NVIDIA Data Center GPUs and Systems](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/platform-support.html#supported-nvidia-data-center-gpus-and-systems) documentation.

{% hint style="info" %}
**Note**

* NVIDIA DGX Spark, NVIDIA Jetson and workstations are not supported.
* vGPU is not supported. NVIDIA Run:ai currently supports GPU passthrough only.
* In addition to GPU Operator compatibility, support also depends on the framework being used (for example, CUDA, PyTorch, TensorFlow, or NVIDIA NIM). Before running a workload, verify that the selected framework version supports your target GPU architecture according to the relevant support matrix.
  {% endhint %}

## Orchestration Platform Compatibility

NVIDIA Run:ai v2.25 supports a wide range of Kubernetes distributions across on-premises, hybrid, and public cloud environments. Use the table below to verify version requirements for your specific platform.

| Orchestration Platform                 | Versions                         | Engine     | x86       | ARM       |
| -------------------------------------- | -------------------------------- | ---------- | --------- | --------- |
| Upstream Kubernetes                    | 1.33-1.35                        | Containerd | Supported | Supported |
| Red Hat OpenShift                      | 4.18-4.21                        | CRI-O      | Supported | Supported |
| Amazon Elastic Kubernetes Engine (EKS) | Based on the upstream Kubernetes | Containerd | Supported | Supported |
| Google Kubernetes Engine (GKE)         | Based on the upstream Kubernetes | Containerd | Supported | Supported |
| Azure Kubernetes Service (AKS)         | Based on the upstream Kubernetes | Containerd | Supported | Supported |
| Oracle Kubernetes Engine (OKE)         | Based on the upstream Kubernetes | Containerd | Supported | Supported |
| Rancher Kubernetes Engine 2 (RKE2)     | Based on the upstream Kubernetes | Containerd | Supported | Supported |


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://run-ai-docs.nvidia.com/self-hosted/getting-started/installation/support-matrix.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
