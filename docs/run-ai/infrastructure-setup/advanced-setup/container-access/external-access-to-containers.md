# External Access to Containers

Researchers may need to access containers remotely during workload execution. Common use cases include:

* Running a Jupyter Notebook inside the container
* Connecting PyCharm for remote Python development
* Viewing machine learning visualizations using TensorBoard

To enable this access, you must expose the relevant container ports.

## Exposing Container Ports

Accessing the containers remotely requires exposing container ports. In Docker, ports are exposed by [declaring](https://docs.docker.com/reference/cli/docker/container/run/) them when launching the container. NVIDIA Run:ai provides similar functionality within a Kubernetes environment.

Since Kubernetes abstracts the container's physical location, exposing ports is more complex. Kubernetes supports multiple methods for exposing container ports. For more details, refer to the [Kubernetes services and networking documentation](https://kubernetes.io/docs/concepts/services-networking/service).

<table><thead><tr><th width="155.71875">Method</th><th width="370.2734375">Description</th><th width="288.94921875">NVIDIA Run:ai Support</th></tr></thead><tbody><tr><td>Port Forwarding</td><td>Simple port forwarding allows access to the container via local and/or remote port.</td><td>Supported natively via Kubernetes</td></tr><tr><td>NodePort</td><td>Exposes the service on each Node’s IP at a static port (the NodePort). You’ll be able to contact the NodePort service from outside the cluster by requesting <code>&#x3C;NODE-IP>:&#x3C;NODE-PORT></code> regardless of which node the container actually resides in.</td><td>Supported</td></tr><tr><td>LoadBalancer</td><td>Exposes the service externally using a cloud provider’s load balancer.</td><td>Supported</td></tr></tbody></table>

## Access to the Running Workload's Container

Many tools used by researchers, such as Jupyter, TensorBoard, or VSCode, require remote access to the running workload's container. In NVIDIA Run:ai, this access is provided through dynamically generated URLs. NVIDIA Run:ai supports two routing models for exposing workloads:

* Host-based routing (default)
* Path-based routing

### Host-Based Routing

By default, NVIDIA Run:ai uses host-based routing to expose workload URLs using subdomains. This allows all workloads to run at the root path, avoiding file path issues and ensuring proper application behavior.

```bash
https://project-name-workload-name.<CLUSTER_URL>/
```

Host-based routing is enabled by default via the `subdomainSupport: true` cluster configuration. For setup instructions, see [Host-based routing](/self-hosted/getting-started/installation/install-using-helm/system-requirements.md#host-based-routing-default) in the system requirements.

### Path-Based Routing

Path-based routing uses the [Cluster URL](/self-hosted/getting-started/installation/install-using-helm/system-requirements.md#fully-qualified-domain-name-fqdn) provided to dynamically create SSL-secured URLs in the following format:

```bash
https://<CLUSTER_URL>/project-name/workload-name
```

To use path-based routing instead, disable host-based routing by setting `subdomainSupport: false` in [Advanced cluster configurations](/self-hosted/infrastructure-setup/advanced-setup/cluster-config.md).

While path-based routing works with applications such as Jupyter Notebooks, it may not be compatible with other applications. Some applications assume they are running at the root file system, so hardcoded file paths and settings within the container may become invalid when running at a path other than the root. For example, if an application expects to access `/etc/config.json` but is served at `/project-name/workspace-name`, the file will not be found. This can cause the container to fail or not function as intended.

{% hint style="info" %}
**Note**

For existing clusters, changing the routing model affects how workload URLs are generated. Administrators should plan this transition accordingly.
{% endhint %}


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://run-ai-docs.nvidia.com/self-hosted/infrastructure-setup/advanced-setup/container-access/external-access-to-containers.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
