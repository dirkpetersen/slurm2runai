# High Availability

This guide outlines the best practices for configuring the NVIDIA Run:ai platform to ensure high availability and maintain service continuity during system failures or under heavy load. The goal is to reduce downtime and eliminate single points of failure by leveraging Kubernetes best practices alongside NVIDIA Run:ai specific configuration options. The NVIDIA Run:ai platform relies on two fundamental high availability strategies:

* **Use of system nodes** - Assigning multiple dedicated nodes for critical system services ensures control, resource isolation, and enables system-level scaling.
* **Replication of core and third-party services** - Configuring multiple replicas of essential services, including both platform and third-party components, distributes workloads and reduces single points of failure. If a component fails on one node, requests can seamlessly route to another instance.

## System Nodes

The NVIDIA Run:ai platform allows you to dedicate specific nodes (system nodes) exclusively for core platform services. This approach provides improved operational isolation and easier resource management.

Ensure that at least **three system nodes** are configured to support high availability. If you use only a single node for core services, horizontally scaled components will not be distributed, resulting in a single point of failure. See [NVIDIA Run:ai system nodes](/self-hosted/infrastructure-setup/advanced-setup/node-roles.md) for more details. This practice applies to both the NVIDIA Run:ai cluster and control plane (self-hosted).

## Service Replicas <a href="#undefined" id="undefined"></a>

### Control Plane Service Replicas

The NVIDIA Run:ai control plane runs in the `runai-backend` namespace and consists of multiple Kubernetes [Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) and [StatefulSets](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/). To achieve high availability, it is recommended to configure multiple replicas during installation or upgrade using Helm flags.

In addition, the control plane supports autoscaling for certain services to handle variable load and improve system resiliency. Autoscaling can be enabled or configured during installation or upgrade using Helm flags.

#### Deployments

By default, NVIDIA Run:ai deployments are deployed with a single replica. To achieve high availability, it is recommended to configure multiple replicas for core NVIDIA Run:ai services. For more information, see [Advanced control plane configuration](/self-hosted/infrastructure-setup/advanced-setup/control-plane-config.md).

#### StatefulSets

NVIDIA Run:ai uses the following third-party components which are managed as Kubernetes StatefulSets. For more information, see [Advanced control plane configurations](/self-hosted/infrastructure-setup/advanced-setup/control-plane-config.md):

* **PostgreSQL** - The internal PostgreSQL cannot be scaled horizontally. To connect NVIDIA Run:ai to an external PostgreSQL service which can be configured for high availability, see [External Postgres Database](/self-hosted/getting-started/installation/install-using-helm/cp-system-requirements.md#external-postgres-database-optional).
* **Thanos** - To enable Thanos autoscaling, use the following NVIDIA Run:ai control plane helm flags:

  ```bash
  --set thanos.query.autoscaling.enabled=true \  
  --set thanos.query.autoscaling.maxReplicas=2 \
  --set thanos.query.autoscaling.minReplicas=2 
  ```
* **Keycloak** **-** By default, Keycloak sets a minimum of 3 pods and will scale to more on transaction load. To scale Keycloak, use the following NVIDIA Run:ai control plane helm flags:

  ```bash
  --set keycloakx.autoscaling.enabled=true
  ```

### Cluster Services Replicas <a href="#nvidia-run-ai-services-replicas" id="nvidia-run-ai-services-replicas"></a>

By default, NVIDIA Run:ai cluster services are deployed with a single replica. To achieve high availability, it is recommended to configure multiple replicas for core NVIDIA Run:ai services. For more information, see [NVIDIA Run:ai services replicas](/self-hosted/infrastructure-setup/advanced-setup/cluster-config.md#nvidia-run-ai-services-replicas).


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://run-ai-docs.nvidia.com/self-hosted/infrastructure-setup/procedures/high-availability.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
