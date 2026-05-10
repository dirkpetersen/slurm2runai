# Upgrade

## Before Upgrade

Before proceeding with the upgrade, it's crucial to apply the specific prerequisites associated with your current version of NVIDIA Run:ai and every version in between up to the version you are upgrading to. If your current version is **2.17 or higher**, you can upgrade directly to the required version.

To ensure a smooth and supported upgrade process:

* **Align control plane and cluster versions** - For best results, upgrade the control plane and cluster components to the same NVIDIA Run:ai version during the same maintenance window. Keeping versions aligned helps avoid unexpected behavior caused by version mismatches and ensures full compatibility across platform components.
* **Upgrade order** - When performing an upgrade:
  * Upgrade the control plane Helm chart first
  * Upgrade the cluster Helm chart only after the control plane upgrade completes successfully

## Helm

NVIDIA Run:ai requires [Helm](https://helm.sh/) 3.14 or later (verified by `helm version --short`) . Before you continue, validate your installed helm client version. To install or upgrade Helm, see [Installing Helm](https://helm.sh/docs/intro/install/). If you are installing an air-gapped version of NVIDIA Run:ai, the NVIDIA Run:ai tar file contains the helm binary.

{% hint style="info" %}
**Note**

Helm 4 defaults to [server-side apply](https://helm.sh/docs/overview/#server-side-apply) when installing a new chart release, which can conflict with resources managed by the NVIDIA Run:ai operator. Append `--server-side=false` to your `helm upgrade` command. NVIDIA Run:ai clusters originally installed with Helm 3.x are unaffected.
{% endhint %}

## Software Files

NVIDIA Run:ai artifacts are available on both NVIDIA NGC and JFrog. Deployments that were originally installed using JFrog can also be upgraded using NGC. As JFrog support is deprecated, upgrading via NGC is the recommended approach, provided that you have an NGC API key.

Use the tab that matches your environment:

* **NGC (Recommended)** - To upgrade using NGC, complete the [Preparations](/self-hosted/getting-started/installation/install-using-helm/preparations.md) section first and make sure you have NGC API key.
* **JFrog** - Existing customers may chose to continue upgrading from JFrog or to upgrade from NGC.

{% tabs %}
{% tab title="Connected (NGC)" %}
Before upgrading, complete the steps in the [Preparations](/self-hosted/getting-started/installation/install-using-helm/preparations.md) section to set up your image pull secret.

Run the following commands to add the NVIDIA Run:ai Helm repository and browse the available versions:

```bash
helm repo add runai https://helm.ngc.nvidia.com/nvidia/runai --force-update \
  --username='$oauthtoken' \
  --password=<NGC_API_KEY>
helm repo update
helm search repo -l runai/control-plane
```

{% endtab %}

{% tab title="Connected (JFrog)" %}
Run the following commands to add the NVIDIA Run:ai Helm repository and browse the available versions:

```bash
helm repo add runai-backend https://runai.jfrog.io/artifactory/cp-charts-prod
helm repo update
helm search repo -l runai-backend
```

{% endtab %}

{% tab title="Air-gapped (NGC)" %}
To download and extract a specific version, and to upload the container images to your private registry using NGC, see the [Preparations](/self-hosted/getting-started/installation/install-using-helm/preparations.md) section.
{% endtab %}

{% tab title="Air-gapped (JFrog)" %}
Run the following command to browse all available air-gapped packages using the token provided by NVIDIA Run:ai.

To download and extract a specific version, and to upload the container images to your private registry, see the [Preparations](/self-hosted/getting-started/installation/install-using-helm/preparations.md) section.

```bash
curl -H "Authorization: Bearer <token>" "https://runai.jfrog.io/artifactory/api/storage/runai-airgapped-prod/?list"
```

{% endtab %}
{% endtabs %}

## Upgrade the Control Plane

### System and Network Requirements

Before upgrading the NVIDIA Run:ai control plane, validate that the latest [system requirements](/self-hosted/getting-started/installation/install-using-helm/cp-system-requirements.md) and [network requirements](/self-hosted/getting-started/installation/install-using-helm/network-requirements.md) are met:

### Upgrade

If your current version is 2.17 or higher, you can upgrade directly to the required version:

{% tabs %}
{% tab title="Connected (NGC)" %}

```bash
helm get values runai-backend -n runai-backend > runai_control_plane_values.yaml
helm upgrade runai-backend -n runai-backend runai/control-plane --version "<VERSION>" -f runai_control_plane_values.yaml --reset-then-reuse-values
```

{% endtab %}

{% tab title="Connected (JFrog)" %}

```bash
helm get values runai-backend -n runai-backend > runai_control_plane_values.yaml
helm upgrade runai-backend -n runai-backend runai-backend/control-plane --version "<VERSION>" -f runai_control_plane_values.yaml --reset-then-reuse-values
```

{% endtab %}

{% tab title="Air-gapped" %}
The following command applies whether you downloaded the package via NGC or JFrog:

```bash
helm get values runai-backend -n runai-backend > runai_control_plane_values.yaml
helm upgrade runai-backend control-plane-<VERSION>.tgz -n runai-backend -f runai_control_plane_values.yaml --reset-then-reuse-values
```

{% endtab %}
{% endtabs %}

## Upgrade the Cluster

### System and Network Requirements

Before upgrading the NVIDIA Run:ai cluster, validate that the latest [system requirements](/self-hosted/getting-started/installation/install-using-helm/system-requirements.md) and [network requirements](/self-hosted/getting-started/installation/install-using-helm/network-requirements.md) are met:

{% hint style="info" %}
**Note**

It is highly recommended to upgrade the Kubernetes version together with the NVIDIA Run:ai cluster version, to ensure compatibility with latest supported version of your [Kubernetes distribution](/self-hosted/getting-started/installation/install-using-helm/system-requirements.md#kubernetes-distribution).
{% endhint %}

### Getting Installation Instructions

Follow the setup and installation instructions below to get the installation instructions to upgrade the NVIDIA Run:ai cluster.

{% hint style="info" %}
**Note**

If your control plane was upgraded using NGC, the cluster must also be upgraded using NGC. See the NGC tab in the [Installation instructions](#installation-instructions) section below.
{% endhint %}

#### Setup

1. In the NVIDIA Run:ai UI, go to Resources -> Clusters
2. Select the cluster you want to upgrade
3. Click **INSTALLATION INSTRUCTIONS**
4. Optional: Select the NVIDIA Run:ai cluster version (latest, by default)
5. Click **CONTINUE**

#### Installation Instructions

{% tabs %}
{% tab title="NGC" %}

1. The NVIDIA Run:ai platform displays the Helm upgrade command in the cluster wizard.
2. Modify the UI-generated command as follows:

   * Replace `<NGC_API_KEY>` with your NGC API key.
   * If you are using a local certificate authority, add `--set global.customCA.enabled=true` to the Helm command as described in the [Local certificate authority](/self-hosted/getting-started/installation/install-using-helm/cp-system-requirements.md#local-certificate-authority) section.
   * The recommended ingress controller is HAProxy. If you are using a different ingress controller, update the ingress class to match the ingress controller configured during the [control plane installation](/self-hosted/getting-started/installation/install-using-helm/install-control-plane.md#connected).
   * Keep the remaining `--set` values exactly as generated by the UI.

   <pre class="language-bash"><code class="lang-bash">helm repo add runai https://helm.ngc.nvidia.com/nvidia/runai --force-update \
   <strong>  --username='$oauthtoken' \
   </strong>  --password=&#x3C;NGC_API_KEY>
   helm repo update
   helm upgrade -i runai-cluster runai/runai-cluster -n runai \
     --set controlPlane.url=... \
     --set controlPlane.clientSecret=... \
     --set cluster.uid=... \
     --set cluster.url=... --version="&#x3C;VERSION>" --create-namespace
     --set clusterConfig.global.ingress.ingressClass=haproxy
   </code></pre>
3. Click **DONE**

Once installation is complete, validate the cluster is **Connected** and listed with the new cluster version. Once you have done this, the cluster is upgraded to the latest version. If the cluster does not appear as expected, see the [cluster troubleshooting scenarios](/self-hosted/infrastructure-setup/procedures/clusters.md#troubleshooting-scenarios).
{% endtab %}

{% tab title="JFrog" %}

1. The NVIDIA Run:ai platform displays the NGC-based Helm upgrade command in the cluster wizard.\
   \&#xNAN;**— Do not run the command exactly as shown in the UI —**
2. Update the UI-generated Helm command as follows:

   * Replace the `helm repo add` command with the following:

     ```bash
     helm repo add runai https://runai.jfrog.io/artifactory/api/helm/run-ai-charts --force-update
     helm repo update
     ```
   * If you are using a local certificate authority, add `--set global.customCA.enabled=true` to the Helm command as described in the [Local certificate authority](/self-hosted/getting-started/installation/install-using-helm/cp-system-requirements.md#local-certificate-authority) section. See the below if [installation fails](#installation-fails).
   * The recommended ingress controller is HAProxy. If you are using a different ingress controller, update the ingress class to match the ingress controller configured during the [control plane installation](/self-hosted/getting-started/installation/install-using-helm/install-control-plane.md#connected).
   * Keep the remaining `--set` values exactly as generated by the UI.

   ```bash
   helm repo add runai https://runai.jfrog.io/artifactory/api/helm/run-ai-charts --force-update
   helm repo update
   helm upgrade -i runai-cluster runai/runai-cluster -n runai \
     --set controlPlane.url=... \
     --set controlPlane.clientSecret=... \
     --set cluster.uid=... \
     --set cluster.url=... --version="<VERSION>" --create-namespace
     --set clusterConfig.global.ingress.ingressClass=haproxy
   ```
3. Click **DONE**

Once installation is complete, validate the cluster is **Connected** and listed with the new cluster version. Once you have done this, the cluster is upgraded to the latest version. If the cluster does not appear as expected, see the [cluster troubleshooting scenarios](/self-hosted/infrastructure-setup/procedures/clusters.md#troubleshooting-scenarios).
{% endtab %}

{% tab title="Air-gapped" %}
The following instructions apply whether you downloaded the package via NGC or JFrog.

1. The NVIDIA Run:ai platform displays the Helm upgrade command in the cluster wizard.\
   \&#xNAN;**— Do not run the command exactly as shown in the UI —**
2. Update the UI-generated Helm command as follows:

   * Do not add the Helm repository — skip `helm repo add` and `helm repo update`.
   * Replace `runai/runai-cluster` with `runai-cluster-<VERSION>.tgz`.
   * Add `--set global.image.registry=<DOCKER_REGISTRY_ADDRESS>` where `<DOCKER_REGISTRY_ADDRESS>` is the Docker registry address configured in the [Preparations](/self-hosted/getting-started/installation/install-using-helm/preparations.md) section.
   * Add `--set clusterConfig.prometheus.spec.baseImage=<DOCKER_REGISTRY_ADDRESS>/<FULL_IMAGE_PATH>`.
   * Add `--set global.customCA.enabled=true` as described in the [Local certificate authority](/self-hosted/getting-started/installation/install-using-helm/system-requirements.md#local-certificate-authority) section.
   * The recommended ingress controller is HAProxy. If you are using a different ingress controller, update the ingress class to match the ingress controller configured during the [control plane installation](/self-hosted/getting-started/installation/install-using-helm/install-control-plane.md#connected).
   * Keep the remaining `--set` values exactly as generated by the UI.

   ```bash
   helm upgrade -i runai-cluster runai-cluster-<VERSION>.tgz \
     --set controlPlane.url=... \
     --set controlPlane.clientSecret=... \
     --set cluster.uid=... \
     --set cluster.url=... --create-namespace \
     --set global.image.registry=registry.mycompany.local \
     --set clusterConfig.prometheus.spec.baseImage=registry.mycompany.local/prometheus/prometheus \
     --set global.customCA.enabled=true
     --set clusterConfig.global.ingress.ingressClass=haproxy
   ```
3. Click **DONE**

Once installation is complete, validate the cluster is **Connected** and listed with the new cluster version. Once you have done this, the cluster is upgraded to the latest version. If the cluster does not appear as expected, see the [cluster troubleshooting scenarios](/self-hosted/infrastructure-setup/procedures/clusters.md#troubleshooting-scenarios).
{% endtab %}
{% endtabs %}

## Migrate from NGINX to HAProxy Ingress

{% hint style="info" %}
**Note**

This section applies to Kubernetes only. OpenShift includes a pre-installed ingress controller by default and does not require this migration.
{% endhint %}

NVIDIA Run:ai recommends using HAProxy as the ingress controller. This change aligns with the announced retirement of the upstream NGINX Ingress Controller project. For more details, see the [NGINX Ingress Controller retirement announcement](https://kubernetes.io/blog/2025/11/11/ingress-nginx-retirement/).

Clusters upgraded from earlier versions typically already have NGINX installed. After upgrading follow the steps below to migrate ingress traffic from NGINX to HAProxy.

### Check the Service Type of the Existing Ingress Controller

Before installing the HAProxy ingress controller, identify which ingress controller is currently in use. If your cluster already has an ingress controller installed, verify how it is exposed to avoid port or IP address conflicts.

```bash
kubectl get svc -n <nginx-namespace>
```

* If the existing ingress controller uses **NodePort**, note the HTTP/HTTPS NodePort values to ensure HAProxy is configured with non-overlapping ports.
* If the existing ingress controller uses **LoadBalancer**, no additional action is required.

When running more than one ingress controller in the same cluster, port conflicts are relevant only for NodePort-based setups. LoadBalancer-based controllers automatically receive separate external IP addresses.

{% hint style="info" %}
**Note**

If your setup differs from the examples above, adjust the configuration accordingly. When using external LoadBalancer on top of Ingress with service type NodePort, you may need to update external resources to route traffic to HAProxy’s configured NodePort values.
{% endhint %}

### Install and Configure HAProxy Ingress Controller

Ingress controllers can be installed and configured in different ways depending on your Kubernetes distribution and how you expose services (for example, NodePort vs. LoadBalancer).

The sections below provide environment-specific Helm installation examples. Select the option that matches your deployment environment.

{% hint style="info" %}
**Note**

OpenShift and RKE2 include a pre-installed ingress controller by default.
{% endhint %}

<details>

<summary>Vanilla Kubernetes</summary>

If your cluster already has an ingress controller installed (for example, NGINX) and it is exposed via NodePort, configure HAProxy to use different NodePort values so both controllers can run simultaneously.

**Ensure the selected NodePort values do not overlap with ports already used by the existing ingress controller.**

<pre class="language-bash"><code class="lang-bash"><strong>helm repo add haproxytech https://haproxytech.github.io/helm-charts
</strong>helm repo update
helm install haproxy-kubernetes-ingress haproxytech/kubernetes-ingress \
 --create-namespace \
 --namespace haproxy-controller \
 --set controller.ingressClassResource.enabled=true \
 --set controller.service.type=NodePort \
 --set controller.service.nodePorts.http=32080 \
 --set controller.service.nodePorts.https=32443
</code></pre>

</details>

<details>

<summary>Managed Kubernetes (EKS, GKE, AKS)</summary>

When using a LoadBalancer, each ingress controller automatically receives its own external IP address from the cloud provider. This allows multiple ingress controllers to run in the same cluster without additional configuration.

<pre class="language-bash"><code class="lang-bash">helm repo add haproxytech https://haproxytech.github.io/helm-charts
helm repo update
helm install haproxy-kubernetes-ingress haproxytech/kubernetes-ingress \
 --create-namespace \
 --namespace haproxy-controller \
<strong> --set controller.service.type=LoadBalancer \
</strong></code></pre>

</details>

<details>

<summary>Oracle Kubernetes Engine (OKE)</summary>

When using a LoadBalancer, each ingress controller automatically receives its own external IP address from the cloud provider. This allows multiple ingress controllers to run in the same cluster without additional configuration.

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

### Verify HAProxy Ingress

After installing the HAProxy ingress controller, verify that HAProxy ingresses are reachable before switching NVIDIA Run:ai components to use it. You can do this by deploying a simple hello-world application.

To run the test, identify the IP address that should reach the cluster’s nodes in your environment.

1. Create a local `haproxy-test.yml` file:

   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: hello
   spec:
     replicas: 1
     selector:
       matchLabels:
         app: hello
     template:
       metadata:
         labels:
           app: hello
       spec:
         containers:
         - name: hello
           image: hashicorp/http-echo:1.0
           args:
             - "-text=hello from haproxy-ingress"
           ports:
             - containerPort: 5678
   ---
   apiVersion: v1
   kind: Service
   metadata:
     name: hello
   spec:
     selector:
       app: hello
     ports:
     - port: 80
       targetPort: 5678
   ---
   apiVersion: networking.k8s.io/v1
   kind: Ingress
   metadata:
     name: hello
   spec:
     ingressClassName: haproxy
     rules:
     - http:
         paths:
         - path: /
           pathType: Prefix
           backend:
             service:
               name: hello
               port:
                 number: 80
   ```
2. Run the following command:

   ```yaml
   kubectl apply -f ha-proxy-test.yml
   ```

Once the application is deployed, access the cluster’s IP address in a browser. If the page displays **“hello from haproxy-ingress”**, HAProxy is functioning correctly and you can proceed with upgrading NVIDIA Run:ai.

### Upgrade the Control Plane with HAProxy

Run the following Helm command to update the NVIDIA Run:ai control plane to use HAProxy instead of NGINX.

{% tabs %}
{% tab title="NGC" %}

```bash
helm upgrade runai-backend -n runai-backend runai/control-plane \
  --version "~2.25.0" \
  --reuse-values \
  --set-string global.ingress.ingressClass=haproxy
```

{% endtab %}

{% tab title="JFrog" %}

```bash
helm upgrade runai-backend -n runai-backend runai-backend/control-plane \
  --version "~2.25.0" \
  --reuse-values \
  --set-string global.ingress.ingressClass=haproxy
```

{% endtab %}
{% endtabs %}

### Upgrade the Cluster with HAProxy

#### Setup

1. In the NVIDIA Run:ai UI, go to Resources -> Clusters
2. Select the cluster you want to upgrade
3. Click **INSTALLATION INSTRUCTIONS**
4. Click **CONTINUE**

#### Installation Instructions

1. Follow the installation instructions. Run the Helm commands provided on your Kubernetes cluster.
2. If not present, add the following flag to the helm install command:

   ```bash
   --set clusterConfig.global.ingress.ingressClass=haproxy
   ```
3. Click **DONE**
4. Once installation is complete, validate the cluster is **Connected** and listed with the new cluster version (see the [cluster troubleshooting scenarios](/self-hosted/infrastructure-setup/procedures/clusters.md#troubleshooting-scenarios)). Once you have done this, the cluster is upgraded and the workloads in this cluster will now use HAProxy instead of NGINX.

## Troubleshooting

If you encounter an issue with the cluster upgrade, use the troubleshooting scenarios below.

### Installation Fails

If the NVIDIA Run:ai cluster installation failed, check the installation logs to identify the issue. Run the following script to print the installation logs:

{% file src="/files/MqckgdW2v7HB4rKj98sU" %}

### Cluster Status

If the NVIDIA Run:ai cluster upgrade completes, but the cluster status does not show as **Connected**, refer to [Troubleshooting scenarios](/self-hosted/infrastructure-setup/procedures/clusters.md#troubleshooting-scenarios).


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://run-ai-docs.nvidia.com/self-hosted/getting-started/installation/install-using-helm/upgrade.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
