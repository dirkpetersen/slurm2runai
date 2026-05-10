# Shared Storage

Shared storage is a critical component in AI and machine learning workflows, particularly in scenarios involving distributed training and shared datasets. In AI and ML environments, data must be readily accessible across multiple nodes, especially when training large models or working with vast datasets. Shared storage enable seamless access to data, ensuring that all nodes in a distributed training setup can read and write to the same datasets simultaneously. This setup not only enhances efficiency but is also crucial for maintaining consistency and speed in high-performance computing environments.

While NVIDIA Run:ai Platform supports a variety of remote data sources, such as Git and S3, it is often more efficient to keep data close to the compute resources. This proximity is typically achieved through the use of shared storage, accessible to multiple nodes in your Kubernetes cluster.

## Shared Storage

When implementing shared storage in Kubernetes, there are two primary approaches:

* Utilizing the [Kubernetes Storage Classes](https://kubernetes.io/docs/concepts/storage/storage-classes/) of your storage provider (Recommended)
* Using a direct NFS (Network File System) mount

NVIDIA Run:ai [Data Sources](/self-hosted/workloads-in-nvidia-run-ai/assets/datasources.md) support both direct NFS mount and Kubernetes Storage Classes.

### Kubernetes Storage Classes

Storage classes in Kubernetes defines how storage is provisioned and managed. This allows you to select storage types optimized for AI workloads. For example, you can choose storage with high IOPS (Input/Output Operations Per Second) for rapid data access during intensive training sessions, or tiered storage options to balance cost and performance-based on your organization’s requirements. This approach supports dynamic provisioning, enabling storage to be allocated on-demand as required by your applications.

NVIDIA Run:ai data sources such as [Persistent Volume Claims (PVC)](/self-hosted/workloads-in-nvidia-run-ai/assets/datasources.md#pvc) and [Data Volumes](/self-hosted/workloads-in-nvidia-run-ai/assets/data-volumes.md) leverage storage class to manage and allocate storage efficiently. This ensures that the most suitable storage option is always accessible, contributing to the efficiency and performance of AI workloads.

{% hint style="info" %}
**Note**

NVIDIA Run:ai lists all available storage classes in the Kubernetes cluster, making it easy for users to select the appropriate storage. Additionally, [policies](/self-hosted/platform-management/policies/policies-and-rules.md) can be set to restrict or enforce the use of specific storage classes, to help maintain compliance with organizational standards and optimize resource utilization.
{% endhint %}

### Direct NFS Mount

Direct NFS allows you to mount a shared file system directly across multiple nodes in your Kubernetes cluster. This method provides a straightforward way to share data among nodes and is often used for simple setups or when a dedicated NFS server is available.

However, using NFS can present challenges related to security and control. Direct NFS setups might lack the fine-grained control and security features available with storage class.


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://run-ai-docs.nvidia.com/self-hosted/infrastructure-setup/procedures/shared-storage.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
