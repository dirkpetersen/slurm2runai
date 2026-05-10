# Vertical Pod Autoscaling (VPA)

Vertical Pod Autoscaling (VPA) automatically adjusts CPU and memory requests and limits for pods based on observed usage. Unlike horizontal scaling which adds replicas, vertical scaling right-sizes existing pods. NVIDIA Run:ai supports configuring VPA on cluster-level services to ensure they have adequate resources as your environment grows. For more information, see [Kubernetes' documentation](https://kubernetes.io/docs/concepts/workloads/autoscaling/vertical-pod-autoscale/).

As clusters scale in nodes and workloads, NVIDIA Run:ai services may benefit from resource adjustments beyond the static defaults. VPA helps identify services that are over-provisioned or under-provisioned and can automatically apply right-sized resource recommendations - reducing the need for manual tuning.

{% hint style="info" %}
**Note**

VPA can be configured on NVIDIA Run:ai cluster components only, not the control plane. For more information about NVIDIA Run:ai service groups and manual scaling recommendations, see [NVIDIA Run:ai at scale](/self-hosted/infrastructure-setup/procedures/scaling.md).
{% endhint %}

### Update Modes

VPA can operate in the following modes:

| Mode                | Description                                                                                                                                       |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Off`               | VPA only generates recommendations and does not apply them. Useful for safely observing suggested values before enabling automatic scaling.       |
| `Initial`           | VPA applies recommendations only when pods are created. Existing pods are not modified.                                                           |
| `Auto`              | VPA applies recommendations by evicting and recreating pods when needed. This may cause restarts.                                                 |
| `InPlaceOrRecreate` | VPA updates resources in-place without restarting pods when supported. If in-place updates are not possible, it falls back to recreating the pod. |

{% hint style="warning" %}
**Important**

VPA does not replace static resource configuration. Your existing static resource settings remain active and in effect regardless of the VPA mode. For static resource configuration, see [NVIDIA Run:ai services resource management](/self-hosted/infrastructure-setup/advanced-setup/cluster-config.md#nvidia-runai-services-resource-management).
{% endhint %}

## Installing VPA

VPA is an external component that does not come preinstalled in most Kubernetes clusters. If it is not installed in your cluster, run the following:

```bash
git clone https://github.com/kubernetes/autoscaler.git
cd autoscaler/vertical-pod-autoscaler
./hack/vpa-up.sh
```

## Configuring VPA

VPA is configured via the `runaiconfig` object and supports multiple levels of configuration. This allows you to define defaults globally, override them per scaling group, and fine-tune behavior for specific components.

The configuration hierarchy is:

1. **Global** - applies to all services
2. **Scaling group** - overrides global for a group of services
3. **Component** - overrides both group and global

When the same service is configured at multiple levels, the most specific level takes precedence. Component-level configuration overrides scaling group, and scaling group overrides global.

VPA is disabled by default. The syntax for configuring VPA follows [Kubernetes' documentation](https://kubernetes.io/docs/concepts/workloads/autoscaling/vertical-pod-autoscale/#resource-policies). There is no need to set `targetRef`, as that is already configured by NVIDIA Run:ai.

### Examples and Recommendations

NVIDIA Run:ai recommends starting with a **global** configuration in **Off** mode, which generates recommendations in the background without applying any changes. After running for 1-2 days, review VPA's resource suggestions. If it recommends higher resources than expected, you can set VPA to `InPlaceOrRecreate` for that specific component to dynamically apply the suggestions.

#### Global Configuration

Use global configuration to define a default VPA policy for all NVIDIA Run:ai cluster services.

{% tabs %}
{% tab title="Helm" %}

```yaml
clusterConfig:
  global:
    vpa:
      enabled: true
      updatePolicy:
        updateMode: "Off"
      resourcePolicy:
        containerPolicies:
          - containerName: "*"
            minAllowed:
              cpu: "100m"
              memory: "128Mi"
            maxAllowed:
              cpu: "4"
              memory: "8Gi"
```

{% endtab %}

{% tab title="runaiconfig" %}

```yaml
spec:
  global:
    vpa:
      enabled: true
      updatePolicy:
        updateMode: "Off"
      resourcePolicy:
        containerPolicies:
          - containerName: "*"
            minAllowed:
              cpu: "100m"
              memory: "128Mi"
            maxAllowed:
              cpu: "4"
              memory: "8Gi"
```

{% endtab %}
{% endtabs %}

To inspect VPA objects and their recommendations, run:

```bash
kubectl get vpa -n runai
```

#### Scaling Group Configuration

Use scaling group configuration to override the global setting for one of the built-in service groups: `workloadServices`, `syncServices`, or `schedulingServices`. For a description of each group and sizing recommendations, see [NVIDIA Run:ai services resource management](/self-hosted/infrastructure-setup/advanced-setup/cluster-config.md#nvidia-runai-services-resource-management) and [NVIDIA Run:ai at scale](/self-hosted/infrastructure-setup/procedures/scaling.md).

{% tabs %}
{% tab title="Helm" %}

```yaml
clusterConfig:
  global:
    workloadServices: # Replace with the relevant service group
      vpa:
        enabled: true
        updatePolicy:
          updateMode: "Auto"
        resourcePolicy:
          containerPolicies:
            - containerName: "*"
              minAllowed:
                cpu: "100m"
                memory: "128Mi"
              maxAllowed:
                memory: "8Gi"
```

{% endtab %}

{% tab title="runaiconfig" %}

```yaml
spec:
  global:
    workloadServices: # Replace with the relevant service group
      vpa:
        enabled: true
        updatePolicy:
          updateMode: "Auto"
        resourcePolicy:
          containerPolicies:
            - containerName: "*"
              minAllowed:
                cpu: "100m"
                memory: "128Mi"
              maxAllowed:
                memory: "8Gi"
```

{% endtab %}
{% endtabs %}

#### Component Configuration

Use component configuration to override both global and scaling group settings for a specific service.

{% tabs %}
{% tab title="Helm" %}

```yaml
clusterConfig:
  workload-controller: # Replace with the relevant component name
    vpa:
      enabled: true
      updatePolicy:
        updateMode: "Off"
      resourcePolicy:
        containerPolicies:
          - containerName: "workload-controller"
            minAllowed:
              cpu: "100m"
              memory: "128Mi"
            maxAllowed:
              cpu: "2"
              memory: "4Gi"
```

{% endtab %}

{% tab title="runaiconfig" %}

```yaml
spec:
  workload-controller: # Replace with the relevant component name
    vpa:
      enabled: true
      updatePolicy:
        updateMode: "Off"
      resourcePolicy:
        containerPolicies:
          - containerName: "workload-controller"
            minAllowed:
              cpu: "100m"
              memory: "128Mi"
            maxAllowed:
              cpu: "2"
              memory: "4Gi"
```

{% endtab %}
{% endtabs %}


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://run-ai-docs.nvidia.com/self-hosted/infrastructure-setup/advanced-setup/vpa.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
