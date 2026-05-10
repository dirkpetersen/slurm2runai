# Installation

NVIDIA Run:ai is a Kubernetes-native orchestration and management platform designed to maximize GPU utilization for AI workloads.

## NVIDIA Run:ai System Components

NVIDIA Run:ai is made up of two components both installed over a [Kubernetes](https://kubernetes.io) cluster:

* **NVIDIA Run:ai control plane** - Provides resource management, handles workload submission and provides cluster monitoring and analytics.
* **NVIDIA Run:ai cluster** - Provides enhanced scheduling and workload management, extending Kubernetes native capabilities.

As part of the installation process, you will install:

* NVIDIA Run:ai [control plane](/self-hosted/getting-started/installation/install-using-helm/install-control-plane.md) that manages one or more clusters
* One or more NVIDIA Run:ai [clusters](/self-hosted/getting-started/installation/install-using-helm/helm-install.md)

Both the Nvidia Run:ai control plane and cluster/s require Kubernetes. In typical deployment, the control plane and first cluster are installed on the same Kubernetes cluster.

<figure><img src="/files/5aE58sv42RwxQhGkBWqY" alt="" width="375"><figcaption></figcaption></figure>

## Installation Types

The self-hosted option is for organizations that cannot use a SaaS solution due to data leakage concerns. NVIDIA Run:ai self-hosting comes with two variants:

| Type       | Description                                                                           |
| ---------- | ------------------------------------------------------------------------------------- |
| Connected  | The organization can freely download from the internet (though upload is not allowed) |
| Air-gapped | The organization has no connection to the internet                                    |

## Software Artifact Sources

NVIDIA Run:ai software artifacts (container images and Helm charts) can be obtained from two sources:

| Source                   | Description                                                                                                    |
| ------------------------ | -------------------------------------------------------------------------------------------------------------- |
| NVIDIA NGC (Recommended) | The NVIDIA NGC catalog. Recommended for all new and existing installations.                                    |
| JFrog                    | The NVIDIA Run:ai artifact repository. JFrog artifacts are deprecated and will be removed in a future release. |

Before installing, complete the [Preparations](/self-hosted/getting-started/installation/install-using-helm/preparations.md) steps to set up access to your chosen artifact source.


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://run-ai-docs.nvidia.com/self-hosted/getting-started/installation.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
