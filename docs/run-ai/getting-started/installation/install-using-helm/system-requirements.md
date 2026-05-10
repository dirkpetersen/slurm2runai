# Cluster System Requirements

The NVIDIA Run:ai cluster is a Kubernetes application. It has specific system and Kubernetes environment requirements that must be met before installation. These requirements ensure that NVIDIA Run:ai cluster services can be deployed successfully and support AI workloads after connecting to the NVIDIA Run:ai control plane.

This section describes the minimum hardware, supported Kubernetes and OpenShift versions, and environment prerequisites required for cluster installation. Environment prerequisites include critical infrastructure components such as a properly configured Fully Qualified Domain Name (FQDN) with DNS resolution, TLS certificate configuration and ingress readiness.

The cluster requires the NVIDIA GPU Operator and other operators and frameworks to be installed in the cluster to provision and manage GPUs and support AI workload execution. For detailed version compatibility, including supported Kubernetes, GPU Operator versions and more, refer to the [Support matrix](/self-hosted/getting-started/installation/support-matrix.md).

{% hint style="info" %}
**Note**

The system requirements needed depend on where the control plane and cluster are installed. The following applies to **Kubernetes only**:

* If you are installing the first cluster and control plane on the same Kubernetes cluster, [Kubernetes ingress controller](#kubernetes-ingress-controller) and [Fully Qualified Domain Name](#fully-qualified-domain-name-fqdn) **are not required**.
* If you are installing the first cluster and control plane on separate Kubernetes clusters, the [Kubernetes ingress controller](#kubernetes-ingress-controller) and [Fully Qualified Domain Name](#fully-qualified-domain-name-fqdn) **are required**.
  {% endhint %}

## Hardware Requirements

The following hardware requirements are for the Kubernetes cluster nodes. By default, all NVIDIA Run:ai cluster services run on all available nodes. For production deployments, you may want to set [node roles](/self-hosted/infrastructure-setup/advanced-setup/node-roles.md) to separate between system and worker nodes, reduce downtime and save CPU cycles on expensive GPU machines.

### Architecture

* **x86** - Supported for Kubernetes and OpenShift.
* **ARM** - Supported for Kubernetes and OpenShift.

### NVIDIA Run:ai Cluster - System Nodes

This configuration is the minimum requirement you need to install and use NVIDIA Run:ai cluster.

| Component  | Required Capacity |
| ---------- | ----------------- |
| CPU        | 10 cores          |
| Memory     | 20GB              |
| Disk space | 50GB              |

{% hint style="info" %}
**Note**

To designate nodes to NVIDIA Run:ai system services, follow the instructions as described in [System nodes](/self-hosted/infrastructure-setup/advanced-setup/node-roles.md#system-nodes).
{% endhint %}

### NVIDIA Run:ai Cluster - Worker Nodes

The NVIDIA Run:ai cluster supports x86 and ARM CPUs, and any NVIDIA GPUs supported by the NVIDIA GPU Operator. The list of supported GPUs depends on the version of the NVIDIA GPU Operator installed in the cluster. NVIDIA Run:ai supports GPU Operator versions 25.10 to 26.3.

For the list of supported GPUs, see [Supported NVIDIA Data Center GPUs and Systems](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/platform-support.html#supported-nvidia-data-center-gpus-and-systems). To install the GPU Operator, see [NVIDIA GPU Operator](#nvidia-gpu-operator).

{% hint style="info" %}
**Note**

* NVIDIA DGX Spark, NVIDIA Jetson and workstations are not supported.
* vGPU is not supported. NVIDIA Run:ai currently supports GPU passthrough only.
  {% endhint %}

The following configuration represents the minimum hardware requirements for installing and operating the NVIDIA Run:ai cluster on worker nodes. Each node must meet these specifications:

| Component | Required Capacity |
| --------- | ----------------- |
| CPU       | 2 cores           |
| Memory    | 4GB               |

{% hint style="info" %}
**Note**

To designate nodes to NVIDIA Run:ai workloads, follow the instructions as described in [Worker nodes](/self-hosted/infrastructure-setup/advanced-setup/node-roles.md#worker-nodes).
{% endhint %}

### Shared Storage

NVIDIA Run:ai workloads must be able to access data from any worker node in a uniform way, to access training data and code as well as save checkpoints, weights, and other machine-learning-related artifacts.

Typical protocols are Network File Storage (NFS) or Network-attached storage (NAS). NVIDIA Run:ai cluster supports both. For more information, see [Shared storage](/self-hosted/infrastructure-setup/procedures/shared-storage.md).

## Software Requirements

The following software requirements must be fulfilled on the Kubernetes cluster.

### Operating System

The following notes apply to the operating system running on NVIDIA Run:ai cluster nodes:

* Any **Linux** operating system supported by both Kubernetes and NVIDIA GPU Operator.
* NVIDIA Run:ai cluster on Google Kubernetes Engine (GKE) supports both Ubuntu and Container Optimized OS (COS).
  * COS is supported only with NVIDIA GPU Operator 24.6 and above, and NVIDIA Run:ai cluster version 2.19 and above.
* NVIDIA Run:ai cluster on Elastic Kubernetes Service (EKS) does not support Bottlerocket or Amazon Linux.
* NVIDIA Run:ai cluster on Oracle Kubernetes Engine (OKE) supports only Ubuntu.
* Internal tests are being performed on **Ubuntu** and **CoreOS** for OpenShift.

### Kubernetes Distribution

#### NVIDIA-Certified Distributions

NVIDIA Run:ai cluster requires Kubernetes. The following Kubernetes distributions are supported:

* Vanilla Kubernetes
* OpenShift Container Platform (OCP)
* Elastic Kubernetes Engine (EKS)
* Google Kubernetes Engine (GKE)
* Azure Kubernetes Service (AKS)
* Oracle Kubernetes Engine (OKE)
* Rancher Kubernetes Engine 2 (RKE2)

{% hint style="info" %}
**Note**

* The latest release of the NVIDIA Run:ai cluster supports **Kubernetes 1.33 to 1.35** and **OpenShift 4.18 to 4.21**.
* For [Multi-Node NVLink](/self-hosted/platform-management/aiinitiatives/resources/using-gb200.md) support (e.g. GB200), Kubernetes 1.32 and above is required.
  {% endhint %}

For existing Kubernetes clusters, see the following Kubernetes version support matrix for the latest NVIDIA Run:ai cluster releases:

| NVIDIA Run:ai version | Supported Kubernetes versions | Supported OpenShift versions |
| --------------------- | ----------------------------- | ---------------------------- |
| 2.25 (latest)         | 1.33 to 1.35                  | 4.18 to 4.21                 |
| 2.24                  | 1.33 to 1.35                  | 4.17 to 4.20                 |
| 2.23                  | 1.31 to 1.34                  | 4.16 to 4.19                 |
| 2.22                  | 1.31 to 1.33                  | 4.15 to 4.19                 |

For information on supported versions of managed Kubernetes, it's important to consult the release notes provided by your Kubernetes service provider. There, you can confirm the specific version of the underlying Kubernetes platform supported by the provider, ensuring compatibility with NVIDIA Run:ai. For an up-to-date end-of-life statement see [Kubernetes Release History](https://kubernetes.io/releases/) or [OpenShift Container Platform Life Cycle Policy](https://access.redhat.com/support/policy/updates/openshift).

#### Partner-Certified Distributions

The following Kubernetes distributions are **partner-certified**. They are tested and validated by the partner, who is responsible for maintaining compatibility with NVIDIA Run:ai:

* Crusoe Managed Kubernetes (CMK)
* Mirantis k0rdent
* Rafay platform
* vCluster
* VMware vSphere Kubernetes Service (VKS)

See the following Kubernetes version support matrix for the NVIDIA Run:ai cluster releases:

| Kubernetes distribution                                                                        | NVIDIA Run:ai version               | Supported Kubernetes versions                     |
| ---------------------------------------------------------------------------------------------- | ----------------------------------- | ------------------------------------------------- |
| Crusoe Managed Kubernetes (CMK)                                                                | 2.22                                | 1.33                                              |
| [Mirantis k0rdent](https://catalog.k0rdent.io/v1.7.0/apps/runai-cp/)                           | <ul><li>2.22</li><li>2.23</li></ul> | <ul><li>1.32-1.33</li><li>1.33-1.34</li></ul>     |
| [Rafay platform](https://docs.rafay.co/aiml/app_marketplace/helm_app/apps/runai/requirements/) | <ul><li>2.23</li><li>2.24</li></ul> | <ul><li>1.33 - 1.34</li><li>1.33 - 1.35</li></ul> |
| [vCluster](https://www.vcluster.com/docs/platform/integrations/certified-stacks/runai)         | 2.24                                | 1.34                                              |
| VMware vSphere Kubernetes Service (VKS)                                                        | 2.22                                | 1.33                                              |

### Container Runtime

NVIDIA Run:ai supports the following [container runtimes](https://kubernetes.io/docs/setup/production-environment/container-runtimes/). Make sure your Kubernetes cluster is configured with one of these runtimes:

* [Containerd](https://kubernetes.io/docs/setup/production-environment/container-runtimes/#containerd) (default in Kubernetes)
* [CRI-O](https://cri-o.io/) (default in OpenShift)

### Kubernetes Pod Security Admission

NVIDIA Run:ai supports `restricted` policy for [Pod Security Admission](https://kubernetes.io/docs/concepts/security/pod-security-admission/) (PSA) on OpenShift only. Other Kubernetes distributions are only supported with `privileged` policy.

For NVIDIA Run:ai on OpenShift to run with PSA `restricted` policy:

* Label the `runai` namespace as described in [Pod Security Admission](https://kubernetes.io/docs/concepts/security/pod-security-admission/) with the following labels:

  ```bash
  pod-security.kubernetes.io/audit=privileged
  pod-security.kubernetes.io/enforce=privileged
  pod-security.kubernetes.io/warn=privileged
  ```
* The workloads submitted through NVIDIA Run:ai should comply with the restrictions of PSA restricted policy. This can be enforced using [Policies](/self-hosted/platform-management/policies/workload-policies.md).

### NVIDIA Run:ai Namespace

The NVIDIA Run:ai must be installed in a namespace or project (OpenShift) called `runai`. Use the following to create the namespace/project:

{% tabs %}
{% tab title="Kubernetes" %}

```bash
kubectl create ns runai
```

{% endtab %}

{% tab title="OpenShift" %}

```bash
oc new-project runai
```

{% endtab %}
{% endtabs %}

### Kubernetes Load Balancer

{% hint style="info" %}
**Note**

If you are deploying the NVIDIA Run:ai cluster on the same Kubernetes instance of the NVIDIA Run:ai control plane, you do not need to install the Load Balancer, as it was already installed as part of the [Control plane system requirements](/self-hosted/getting-started/installation/install-using-helm/cp-system-requirements.md#kubernetes-load-balancer).
{% endhint %}

In Kubernetes, services of type `LoadBalancer` are used to expose applications outside the cluster through a single, stable IP address, providing a consistent entry point for external traffic. In managed cloud environments this capability is built-in, while in self-hosted and on-premise deployments it must be provided explicitly.

MetalLB fulfills this role by allocating external IP addresses from a predefined pool and advertising them on the external network, enabling access to services running inside the cluster.

In NVIDIA Run:ai, this is required to support north-south traffic, including access to the NVIDIA Run:ai control plane, APIs, UI, inference endpoints, and externally exposed development workspaces and training workloads.

1. Reserve a range of IP addresses (recommended a full 32 subnet) for example: `172.20.10.0-172.20.10.255`
2. Install MetalLB:

   ```bash
   helm repo add metallb https://metallb.github.io/metallb
   helm repo update
   helm install metallb metallb/metallb --version 0.15.3 --namespace metallb-system --create-namespace
   ```
3. Create a YAML file named `metalLB-config.yaml` and replace `<IPADDRESS-RANGE-START>-<IPADDRESS-RANGE-END>` with the reserved range of IP addresses:

   ```yaml
   apiVersion: metallb.io/v1beta1
   kind: IPAddressPool
   metadata:
     name: runai-ip-pool
     namespace: metallb-system
   spec:
     addresses:
     - <IPADDRESS-RANGE-START>-<IPADDRESS-RANGE-END> # for example 172.20.10.0-172.20.10.255
   ---
   apiVersion: metallb.io/v1beta1
   kind: L2Advertisement
   metadata:
     name: runai-l2-advertisement
     namespace: metallb-system
   spec:
     ipAddressPools:
     - runai-ip-pool
   ```
4. Apply the YAML:

   ```bash
   kubectl apply -f metalLB-config.yaml
   ```

### Kubernetes Ingress Controller

The NVIDIA Run:ai cluster requires [Kubernetes Ingress Controller](https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/) to be installed on the Kubernetes cluster.

{% hint style="info" %}
**Note**

If you are deploying the NVIDIA Run:ai cluster on the same Kubernetes instance of the NVIDIA Run:ai control plane, you do not need to install the Ingress Controller, as it was already installed as part of the [Control plane system requirements](/self-hosted/getting-started/installation/install-using-helm/cp-system-requirements.md#kubernetes-ingress-controller).
{% endhint %}

* OpenShift and RKE2 come with a pre-installed ingress controller.
* Make sure that a default ingress controller, `global.ingress.ingressClass` is set. For more details, see [Advanced cluster configurations](/self-hosted/infrastructure-setup/advanced-setup/cluster-config.md).

There are multiple ways to install and configure an ingress controller. The following example demonstrates how to install and configure the [HAProxy](https://www.haproxy.com/documentation/kubernetes-ingress/community/) ingress controller using [helm](https://helm.sh/).

<details>

<summary>Vanilla Kubernetes</summary>

<pre class="language-bash"><code class="lang-bash">helm repo add haproxytech https://haproxytech.github.io/helm-charts
helm repo update
<strong>helm install haproxy-kubernetes-ingress haproxytech/kubernetes-ingress \
</strong> --create-namespace \
<strong> --namespace haproxy-controller \
</strong> --set controller.kind=DaemonSet \
 --set controller.service.type=NodePort
</code></pre>

</details>

<details>

<summary>Managed Kubernetes (EKS, GKE, AKS)</summary>

```bash
helm repo add haproxytech https://haproxytech.github.io/helm-charts
helm repo update
helm install haproxy-kubernetes-ingress haproxytech/kubernetes-ingress \
 --create-namespace \
 --namespace haproxy-controller \
 --set controller.service.type=LoadBalancer
```

</details>

<details>

<summary>Oracle Kubernetes Engine (OKE)</summary>

```bash
helm repo add haproxytech https://haproxytech.github.io/helm-charts
helm repo update
helm install haproxy-kubernetes-ingress haproxytech/kubernetes-ingress \
 --create-namespace \
 --namespace haproxy-controller \
 --set controller.kind=DaemonSet \
 --set controller.service.type=LoadBalancer \
 --set controller.service.externalTrafficPolicy=Local \
 --set controller.service.annotations."oci-network-load-balancer\.oraclecloud\.com/is-preserve-source"="True" \
 --set controller.service.annotations."oci-network-load-balancer\.oraclecloud\.com/security-list-management-mode"=All \
 --set controller.service.annotations."oci\.oraclecloud\.com/load-balancer-type"=nlb
```

</details>

### NVIDIA GPU Operator

The NVIDIA Run:ai cluster requires NVIDIA GPU Operator to be installed on the Kubernetes cluster. GPU Operator versions 25.10 to 26.3 are supported.

{% hint style="info" %}
**Note**

For [Multi-Node NVLink](/self-hosted/platform-management/aiinitiatives/resources/using-gb200.md) support (e.g. GB200), GPU Operator 25.3 and above is required.
{% endhint %}

* For installation instructions, see [Installing the NVIDIA GPU Operator](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/getting-started.html).
* For air-gapped installation, follow the instructions in [Install NVIDIA GPU Operator in Air-Gapped Environments](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/install-gpu-operator-air-gapped.html).
* See the following notes below:
  * Use the default `gpu-operator` namespace. Otherwise, you must specify the target namespace using the flag `runai-operator.config.nvidiaDcgmExporter.namespace` as described in [Advanced cluster configurations](/self-hosted/infrastructure-setup/advanced-setup/cluster-config.md).
  * NVIDIA drivers may already be installed on the nodes. In such cases, use the NVIDIA GPU Operator flags `--set driver.enabled=false`. [DGX OS](https://docs.nvidia.com/dgx/dgx-os-6-user-guide/release_notes.html) is one such example as it comes bundled with NVIDIA Drivers.
* For distribution-specific requirements and additional instructions, see the sections below:

<details>

<summary>OpenShift Container Platform (OCP)</summary>

The Node Feature Discovery (NFD) Operator is a prerequisite for the NVIDIA GPU Operator in OpenShift. Install the NFD Operator using the Red Hat OperatorHub catalog in the OpenShift Container Platform web console. For more information, see [Installing the Node Feature Discovery (NFD) Operator](https://docs.nvidia.com/datacenter/cloud-native/openshift/latest/install-nfd.html).

</details>

<details>

<summary>Elastic Kubernetes Service (EKS)</summary>

* When setting up the cluster, do **not** install the NVIDIA device plug-in (we want the NVIDIA GPU Operator to install it instead).
* When using the [eksctl](https://eksctl.io/) tool to create a cluster, use the flag `--install-nvidia-plugin=false` to disable the installation.

For GPU nodes, EKS uses an AMI which already contains the NVIDIA drivers. As such, you must use the GPU Operator flags: `--set driver.enabled=false.`

</details>

<details>

<summary>Google Kubernetes Engine (GKE)</summary>

Before installing the GPU Operator:

1. Create the `gpu-operator` namespace by running:

   ```bash
   kubectl create ns gpu-operator
   ```
2. Create the following file:

   ```yaml
   #resourcequota.yaml

   apiVersion: v1
   kind: ResourceQuota
   metadata:
   name: gcp-critical-pods
   namespace: gpu-operator
   spec:
   scopeSelector:
       matchExpressions:
       - operator: In
       scopeName: PriorityClass
       values:
       - system-node-critical
       - system-cluster-critical
   ```
3. Run:

   ```bash
   kubectl apply -f resourcequota.yaml
   ```

</details>

<details>

<summary>Rancher Kubernetes Engine 2 (RKE2)</summary>

Before installing the GPU Operator, verify the [host OS requirements](https://docs.rke2.io/add-ons/gpu_operators?GPUoperator=v25.3.x#host-os-requirements) are met. Then, install the [operator](https://docs.rke2.io/add-ons/gpu_operators#operator-installation).

When installing GPU Operator v25.3, update the Helm values file as follows:

```yaml
apiVersion: helm.cattle.io/v1
kind: HelmChart
metadata:
  name: gpu-operator
  namespace: kube-system
spec:
  repo: https://helm.ngc.nvidia.com/nvidia
  chart: gpu-operator
  version: v25.3.4
  targetNamespace: gpu-operator
  createNamespace: true
  valuesContent: |-
    toolkit:
      env:
      - name: CONTAINERD_SOCKET
        value: /run/k3s/containerd/containerd.sock
```

</details>

<details>

<summary>Oracle Kubernetes Engine (OKE)</summary>

* During cluster setup, [create a node pool](https://docs.oracle.com/en-us/iaas/tools/python/latest/api/container_engine/models/oci.container_engine.models.NodePool.html#oci.container_engine.models.NodePool.initial_node_labels), and set `initial_node_labels` to include `oci.oraclecloud.com/disable-gpu-device-plugin=true` which disables the NVIDIA GPU device plugin.
* For GPU nodes, OKE defaults to Oracle Linux, which is incompatible with NVIDIA drivers. To resolve this, use a custom Ubuntu image instead.

</details>

For troubleshooting information, see the [NVIDIA GPU Operator Troubleshooting Guide](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/troubleshooting.html).

### NVIDIA Network Operator

When deploying on clusters with RDMA or Multi-Node NVLink‑capable nodes (e.g. B200, GB200), the NVIDIA Network Operator is required to enable high-performance networking features such as GPUDirect RDMA in Kubernetes. Network Operator versions 25.10 to 26.1 are supported.

The Network Operator works alongside the NVIDIA GPU Operator to provide:

* NVIDIA networking drivers for advanced network capabilities.
* Kubernetes device plugins to expose high‑speed network hardware to workloads.
* Secondary network components to support network‑intensive applications.

The Network Operator must be installed and configured as follows:

1. Install the network operator as detailed in [Network Operator Deployment on Vanilla Kubernetes Cluster](https://docs.nvidia.com/networking/display/kubernetes2440/getting-started-kubernetes.html#network-operator-deployment-on-vanilla-kubernetes-cluster).
2. Configure SR-IOV InfiniBand support as detailed in [Network Operator Deployment with an SR-IOV InfiniBand Network](https://docs.nvidia.com/networking/display/kubernetes2440/getting-started-kubernetes.html#network-operator-deployment-with-an-sr-iov-infiniband-network).

For air-gapped installation, follow the instructions in [Network Operator Deployment in an Air-gapped Environment](https://docs.nvidia.com/networking/display/kubernetes2540/advanced/proxy-airgapped.html#network-operator-deployment-in-an-air-gapped-environment).

### NVIDIA Dynamic Resource Allocation (DRA) Driver

When deploying on clusters with Multi-Node NVLink (e.g. GB200), the NVIDIA DRA driver is required to enable Dynamic Resource Allocation at the Kubernetes level. To install, follow the instructions in [Configure and Helm-install the driver](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/dra-intro-install.html#configure-and-helm-install-the-driver). For air-gapped installations, the DRA driver is installed with the [GPU Operator](#nvidia-gpu-operator). DRA driver versions 25.8 to 25.12 are supported.

After the DRA driver is installed, update the cluster configuration using `GPUNetworkAccelerationEnabled` flag to enable GPU network acceleration. This triggers an update of the NVIDIA Run:ai workload controller deployment and restarts the controller. For details on how to configure this value using Helm or `runaiconfig`, see [Advanced cluster configurations](/self-hosted/infrastructure-setup/advanced-setup/cluster-config.md).

{% hint style="info" %}
**Note**

For air-gapped installation, contact [NVIDIA Run:ai support](https://www.nvidia.com/en-eu/support/enterprise/#contact-us).
{% endhint %}

### Prometheus

{% hint style="info" %}
**Note**

Installing Prometheus applies to Kubernetes only.
{% endhint %}

NVIDIA Run:ai cluster requires Prometheus to be installed on the Kubernetes cluster.

* OpenShift clusters include Prometheus by default.
* For RKE2, see [Enable Monitoring](https://ranchermanager.docs.rancher.com/how-to-guides/advanced-user-guides/monitoring-alerting-guides/enable-monitoring) for instructions on installing Prometheus.

There are multiple ways to install Prometheus. The following example shows how to install the community [Kube-Prometheus Stack](https://artifacthub.io/packages/helm/prometheus-community/kube-prometheus-stack) using [helm](https://helm.sh/):

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install prometheus prometheus-community/kube-prometheus-stack \
    -n monitoring --create-namespace --set grafana.enabled=false
```

## Routing Traffic to and from NVIDIA Run:ai Services

This section describes how to route traffic to and from NVIDIA Run:ai services. Proper traffic routing is required to enable secure access to the NVIDIA Run:ai control plane (via the UI or API), as well as external access to development workspaces, training workloads, and inference workloads.

NVIDIA Run:ai supports two routing approaches for exposing services: host-based routing and path-based routing. While path-based routing exposes multiple services under a shared domain using URL paths, host-based routing assigns each service its own subdomain. Since many development tools and applications expect to run at the root path, host-based routing avoids common compatibility issues and is therefore used by default in NVIDIA Run:ai.

NVIDIA Run:ai uses host-based routing by default, which relies on DNS and TLS configuration to securely expose services. To support this, three key components must be configured:

* A [Fully Qualified Domain Name (FQDN)](#fully-qualified-domain-name-fqdn) structure
* [TLS certificates](#tls-certificate) for secure communication
* [Host-based routing](#host-based-routing-default) for workload exposure

Together, these components ensure that traffic is routed correctly and securely across all NVIDIA Run:ai services.

{% hint style="info" %}
**Note**

* NVIDIA Run:ai also supports path-based routing. If this approach better fits your environment, you can use it instead of the default host-based routing. In this case, the [workspace and training wildcard certificate](#workspaces-and-training-workload-certificate) is not required.
* To use path-based routing, disable host-based routing by setting `clusterConfig.global.subdomainSupport: false` during Helm installation. See [Advanced cluster configurations](/self-hosted/infrastructure-setup/advanced-setup/cluster-config.md).
  {% endhint %}

### Fully Qualified Domain Name (FQDN)

{% hint style="info" %}
**Note**

* Fully Qualified Domain Name applies to Kubernetes only.
* If you are deploying the NVIDIA Run:ai cluster on the same Kubernetes instance as the NVIDIA Run:ai control plane, you do not need to configure a fully qualified domain name (FQDN), as it was already defined as part of the [Control plane system requirements](/self-hosted/getting-started/installation/install-using-helm/cp-system-requirements.md#fully-qualified-domain-name-fqdn).
  {% endhint %}

NVIDIA Run:ai services rely on Fully Qualified Domain Names (FQDNs) to route traffic between system components and to expose workloads externally. In NVIDIA Run:ai, the FQDN settings are needed for:

* Enabling communication between the control plane and the cluster
* Exposing development workspaces and training workloads via subdomains
* Exposing inference workloads via dedicated subdomains

You must configure domain names for each of the following communication types:

* Control plane ↔ cluster communication\
  Example: `runai.mycorp.local`\
  The IP address of this domain must be resolvable within the organization’s private network.
* Workspace and training workloads (external access)\
  Example: `*.runai.mycorp.local`
* Inference workloads (external access)\
  Example: `*.runai-inference.mycorp.local`

Since NVIDIA Run:ai uses host-based routing, wildcard DNS records must be configured to enable external access to workloads.

Configure the following DNS records. Both records should resolve to the same cluster public IP address, or to the cluster’s load balancer IP in on-prem environments. This ensures that each workspace or workload is assigned a unique subdomain under the wildcard domains:

```bash
*.runai.mycorp.local → <cluster IP>
*.runai-inference.mycorp.local → <cluster IP>
```

### NVIDIA Run:ai TLS Certificates

TLS certificates secure communication between NVIDIA Run:ai components and enable HTTPS access to exposed services.

NVIDIA Run:ai requires three TLS certificates, each aligned with a specific domain:

* Cluster domain certificate
* Workspaces and training workload certificate
* Inference certificate (wildcard)

#### Cluster Domain Certificates (Single-Domain)

* **Kubernetes** - To enable secure communication between the NVIDIA Run:ai control plane and the cluster, configure a TLS certificate associated with the cluster’s main domain (e.g. `runai.mycorp.local`). This certificate should be stored as a secret named `runai-cluster-domain-tls-secret` in the `runai` namespace.

  * Replace `/path/to/fullchain.pem` with the actual path to your TLS certificate.
  * Replace `/path/to/private.pem` with the actual path to your private key.

  ```bash
  kubectl create secret tls runai-cluster-domain-tls-secret -n runai \
    --cert /path/to/fullchain.pem \
    --key /path/to/private.pem
  ```
* **OpenShift** - NVIDIA Run:ai uses the OpenShift default Ingress router for serving. The TLS certificate configured for this router must be issued by a trusted CA. For more details, see the OpenShift documentation on [configuring certificates](https://docs.redhat.com/en/documentation/openshift_container_platform/4.18/html/security_and_compliance/configuring-certificates#replacing-default-ingress).

#### Workspaces & Training Workload Wildcard Certificate

{% hint style="info" %}
**Note**

For path-based routing, ignore this configuration and move to the next step.
{% endhint %}

* **Kubernetes** - To allow secure access to workspace and training workloads via subdomains, configure a wildcard TLS certificate that matches the cluster domain (e.g. `*.runai.mycorp.local`). This certificate should be stored as a secret named `runai-cluster-domain-star-tls-secret` in the `runai` namespace.
  * Replace `/path/to/fullchain.pem` with the actual path to your TLS certificate.
  * Replace `/path/to/private.pem` with the actual path to your private key.

    ```bash
    kubectl create secret tls runai-cluster-domain-star-tls-secret -n runai \
      --cert /path/to/fullchain.pem \
      --key /path/to/private.pem
    ```
* **OpenShift** - A wildcard TLS certificate for Workspace and Training workloads is not required. OpenShift Routes handle TLS termination for inference endpoints using the platform’s built-in routing and certificate management.

#### Inference Wildcard Certificate

* **Kubernetes** - To securely expose inference services over HTTPS, configure a wildcard TLS certificate for the inference domain (e.g. `*.runai-inference.mycorp.local`). This certificate should be stored as a secret named `runai-cluster-inference-tls-secret` in the `knative-serving` namespace.

  * Replace `/path/to/fullchain.pem` with the actual path to your TLS certificate.
  * Replace `/path/to/private.pem` with the actual path to your private key.

  ```bash
  kubectl create secret tls runai-cluster-inference-tls-secret -n knative-serving \
      --cert /path/to/fullchain.pem \
      --key /path/to/private.pem
  ```
* **OpenShift** - A wildcard TLS certificate for Inference workloads is not required. OpenShift Routes handle TLS termination for inference endpoints using the platform’s built-in routing and certificate management.

### Host-Based Routing (Default)

{% hint style="info" %}
**Note**

* The following steps are required for Kubernetes only. For OpenShift, no additional configuration is required.
* NVIDIA Run:ai also support path-based routing. If you prefer to use it instead of the default host-based routing, disable host-based routing by setting `clusterConfig.global.subdomainSupport: false` during the Helm installation. See [Advanced cluster configurations](/self-hosted/infrastructure-setup/advanced-setup/cluster-config.md).
* If you choose path-based routing, skip the below steps.
  {% endhint %}

Host-based routing binds together the configured domains (FQDN), TLS certificates, and ingress rules to expose workloads externally. With NVIDIA Run:ai host-based routing, workloads are exposed using subdomains, so each workload is assigned its own URL. For example:

```bash
https://<project>-<workload>.<CLUSTER_URL>
```

Host-based routing relies on:

* The FQDN structure defined earlier
* The TLS certificates configured for those domains

This section describes how to connect these components to enable workload exposure.

1. Ensure that:
   * Wildcard DNS records are configured (see [FQDN](#fully-qualified-domain-name-fqdn) section)
   * TLS certificates are created and stored as Kubernetes secrets (see [TLS certificates](#nvidia-run-ai-tls-certificates) section)
2. Create the ingress resource

   ```yaml
   apiVersion: networking.k8s.io/v1
   kind: Ingress
   metadata:
     name: runai-cluster-domain-star-ingress
     namespace: runai
   spec:
     rules:
     - host: '*.<CLUSTER_URL>'
     tls:
     - hosts:
       - '*.<CLUSTER_URL>'
       secretName: runai-cluster-domain-star-tls-secret
   ```
3. Run the following:

   ```bash
   kubectl apply -f <filename>
   ```

### Local Certificate Authority

A local certificate authority serves as the root certificate for organizations that cannot use **publicly trusted certificate authority**. Follow the steps below to configure the local certificate authority.

In air-gapped environments, you **must** configure and install the local CA's public key in the Kubernetes cluster. This is required for the installation to succeed:

1\. Add the public key to the required namespace:

{% tabs %}
{% tab title="Kubernetes" %}

```bash
kubectl -n runai create secret generic runai-ca-cert \
    --from-file=runai-ca.pem=<ca_bundle_path>
kubectl label secret runai-ca-cert -n runai run.ai/cluster-wide=true run.ai/name=runai-ca-cert --overwrite
```

{% endtab %}

{% tab title="OpenShift" %}

```bash
oc -n runai create secret generic runai-ca-cert \
    --from-file=runai-ca.pem=<ca_bundle_path>
oc -n openshift-monitoring create secret generic runai-ca-cert \
    --from-file=runai-ca.pem=<ca_bundle_path>
oc label secret runai-ca-cert -n runai run.ai/cluster-wide=true run.ai/name=runai-ca-cert --overwrite
```

{% endtab %}
{% endtabs %}

2. When installing the cluster, make sure the following flag is added to the helm command `--set global.customCA.enabled=true`. See [Install the cluster](/self-hosted/getting-started/installation/install-using-helm/helm-install.md#installation).

{% hint style="info" %}
**Note**

For Git and S3 data source integrations, NVIDIA Run:ai supports the following options:

* Use the same custom CA defined during cluster installation by setting:\
  `--set global.customCAGit.enabled=true` or\
  `--set global.customCAS3.enabled=true`.
* Use a different CA certificate specifically for Git or S3 by enabling the setting and providing a custom secret name:\
  `--set global.customCAGit.enabled=true`\
  `--set global.customCAGit.secret.name=<git-ca-cert>` or\
  `--set global.customCAS3.enabled=true`\
  `--set global.customCAS3.secret.name=<s3-ca-cert>`

For more details, see [Advanced cluster configurations](/self-hosted/infrastructure-setup/advanced-setup/cluster-config.md).
{% endhint %}

## Additional Software Requirements

To enable NVIDIA Run:ai capabilities such as Distributed Training and Inference, additional Kubernetes applications (frameworks) must be installed on the cluster.

### Distributed Training

Distributed training enables training of AI models over multiple nodes. This requires installing a distributed training framework on the cluster. The following frameworks are supported:

* [TensorFlow](https://www.tensorflow.org/)
* [PyTorch](https://pytorch.org/)
* [XGBoost](https://xgboost.readthedocs.io/)
* [MPI v2](https://docs.open-mpi.org/)
* [JAX](https://docs.jax.dev/en/latest/index.html)

There are several ways to install each framework. A simple method of installation example is the [Kubeflow Training Operator](https://www.kubeflow.org/docs/components/training/installation/) which includes TensorFlow, PyTorch, XGBoost and JAX.

It is recommended to use **Kubeflow Training Operator v1.9.2**, and **MPI Operator v0.6.0 or later** for compatibility with advanced workload capabilities, such as [Stopping a workload](/self-hosted/workloads-in-nvidia-run-ai/workloads.md) and [Scheduling rules](/self-hosted/platform-management/policies/scheduling-rules.md).

* To install the Kubeflow Training Operator for TensorFlow, PyTorch, XGBoost and JAX frameworks, run the following command:

  ```bash
  kubectl apply --server-side -k "github.com/kubeflow/training-operator.git/manifests/overlays/standalone?ref=v1.9.2"
  ```
* To install the MPI Operator for MPI v2, run the following command:

  ```bash
  kubectl apply --server-side -f https://raw.githubusercontent.com/kubeflow/mpi-operator/v0.6.0/deploy/v2beta1/mpi-operator.yaml
  ```

{% hint style="info" %}
**Note**

If you require both the MPI Operator and Kubeflow Training Operator, follow the steps below:

* Install the Kubeflow Training Operator as described above.
* Disable and delete MPI v1 in the Kubeflow Training Operator by running:

  ```bash
  kubectl patch deployment training-operator -n kubeflow --type='json' -p='[{"op": "add", "path": "/spec/template/spec/containers/0/args", "value": ["--enable-scheme=tfjob", "--enable-scheme=pytorchjob", "--enable-scheme=xgboostjob", "--enable-scheme=jaxjob"]}]'
  kubectl delete crd mpijobs.kubeflow.org
  ```
* Install the MPI Operator as described above.
  {% endhint %}

### Inference

Inference enables serving of AI models. This requires the [Knative Serving](https://knative.dev/docs/serving/) framework to be installed on the cluster and supports Knative versions 1.19 to 1.21.

{% tabs %}
{% tab title="Kubernetes" %}
Follow the [Installing Knative](https://knative.dev/docs/install/operator/knative-with-operators/) instructions or run:

```bash
helm repo add knative-operator https://knative.github.io/operator
helm install knative-operator --create-namespace --namespace knativeoperator --version 1.18.2 knative-operator/knative-operator
```

Once installed, follow the steps below:

1. Create the `knative-serving` namespace:

   ```bash
   kubectl create ns knative-serving
   ```
2. Create a YAML file named `knative-serving.yaml` and replace the placeholder FQDN with your wildcard inference domain (for example, `runai-inference.mycorp.local`):

   ```yaml
   apiVersion: operator.knative.dev/v1beta1
   kind: KnativeServing
   metadata:
     name: knative-serving
     namespace: knative-serving
   spec:
     config:
       config-autoscaler:
         enable-scale-to-zero: "true"
       config-features:
         kubernetes.podspec-affinity: enabled
         kubernetes.podspec-init-containers: enabled
         kubernetes.podspec-persistent-volume-claim: enabled
         kubernetes.podspec-persistent-volume-write: enabled
         kubernetes.podspec-schedulername: enabled
         kubernetes.podspec-securitycontext: enabled
         kubernetes.podspec-tolerations: enabled
         kubernetes.podspec-volumes-emptydir: enabled
         kubernetes.podspec-fieldref: enabled
         kubernetes.containerspec-addcapabilities: enabled
         kubernetes.podspec-nodeselector: enabled
         multi-container: enabled
         kubernetes.podspec-hostipc: enabled
         kubernetes.podspec-hostnetwork: enabled
       domain:
         runai-inference.mycorp.local: "" # replace with the wildcard FQDN for Inference
       network:
         domainTemplate: '{{.Name}}-{{.Namespace}}.{{.Domain}}'
         ingress-class: kourier.ingress.networking.knative.dev
         default-external-scheme: https
     high-availability:
       replicas: 2
     ingress:
       kourier:
         enabled: true
   ```
3. Apply the changes:

   ```bash
   kubectl apply -f knative-serving.yaml
   ```
4. Configure HAProxy to proxy requests to Kourier / Knative and handle TLS termination using the wildcard certificate. Create a YAML file named `knative-ingress.yaml` and replace the FQDN placeholders with your wildcard inference domain:

   ```yaml
   apiVersion: networking.k8s.io/v1
   kind: Ingress
   metadata:
     name: knative-serving
     namespace: knative-serving
   spec:
     ingressClassName: haproxy
     rules:
     - host: '*.runai-inference.mycorp.local' # replace with the wildcard FQDN for Inference
       http:
         paths:
         - backend:
             service:
               name: kourier
               port:
                 number: 80
           path: /
           pathType: Prefix
     tls:
     - hosts:
       - '*.runai-inference.mycorp.local' # replace with the wildcard FQDN for Inference
       secretName: runai-cluster-inference-tls-secret
   ```
5. Apply the changes:

   ```bash
   kubectl apply -f knative-ingress.yaml
   ```

{% endtab %}

{% tab title="OpenShift" %}
Follow the [Installing the OpenShift Serverless Operator](https://docs.redhat.com/en/documentation/red_hat_openshift_serverless/1.37/html/installing_openshift_serverless/install-serverless-operator) instructions. Once installed, follow the steps below:

1. Create the `knative-serving` project:

   ```bash
   oc new-project knative-serving
   ```
2. Create a YAML file named `knative-serving.yaml`:

   ```yaml
   apiVersion: operator.knative.dev/v1beta1
   kind: KnativeServing
   metadata:
     finalizers:
       - knative-serving-openshift
       - knativeservings.operator.knative.dev
     name: knative-serving
     namespace: knative-serving
   spec:
     config:
       config-features:
         kubernetes.podspec-tolerations: enabled
         kubernetes.podspec-volumes-emptydir: enabled
         kubernetes.podspec-persistent-volume-claim: enabled
         multi-container: enabled
         kubernetes.podspec-persistent-volume-write: enabled
         kubernetes.podspec-fieldref: enabled
         kubernetes.podspec-schedulername: enabled
         kubernetes.podspec-nodeselector: enabled
         kubernetes.podspec-init-containers: enabled
         kubernetes.podspec-securitycontext: enabled
         kubernetes.podspec-affinity: enabled
         kubernetes.containerspec-addcapabilities: enabled
     controller-custom-certs:
       name: ''
       type: ''
     registry: {}
   ```
3. Apply the changes:

   ```bash
   oc apply -f knative-serving.yaml
   ```

{% endtab %}
{% endtabs %}

### Autoscaling

NVIDIA Run:ai allows for autoscaling a deployment according to the metrics below:

* Latency (milliseconds)
* Throughput (requests/sec)
* Concurrency (requests)

Using a custom metric (for example, Latency) requires installing the [Kubernetes Horizontal Pod Autoscaler (HPA)](https://knative.dev/docs/install/yaml-install/serving/install-serving-with-yaml/#install-optional-serving-extensions). Use the following command to install. Make sure to update the {VERSION} in the below command with a [supported Knative version](#inference).

```bash
kubectl apply -f https://github.com/knative/serving/releases/download/knative-{VERSION}/serving-hpa.yaml
```

### Distributed Inference

NVIDIA Run:ai supports distributed inference (multi-node) deployments using the Leader Worker Set (LWS). To enable this capability, you must install the [LWS Helm chart](https://lws.sigs.k8s.io/docs/installation/#install-by-helm) in version 0.7.0 or higher on your cluster:

```bash
CHART_VERSION=0.7.0
helm install lws oci://registry.k8s.io/lws/charts/lws \
  --version=$CHART_VERSION \
  --namespace lws-system \
  --create-namespace \
  --wait --timeout 300s
```

## Integrations

Integrations are Kubernetes components and external tools that can be used with NVIDIA Run:ai for development, training, orchestration, data access, and monitoring.

In many cases, the integration is “out of the box” from the NVIDIA Run:ai side. Once the component is installed in the cluster, you can submit its custom resource definitions (CRDs) and still benefit from NVIDIA Run:ai scheduling, resource management, and visibility. Examples include NVIDIA components such as the **NIM Operator** and **Dynamo Operator**. See [Integrations](/self-hosted/infrastructure-setup/advanced-setup/integrations.md) for more details.


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://run-ai-docs.nvidia.com/self-hosted/getting-started/installation/install-using-helm/system-requirements.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
