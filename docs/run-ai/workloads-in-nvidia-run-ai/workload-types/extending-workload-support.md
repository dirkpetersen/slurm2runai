# Extending Workload Support with Resource Interface

The Resource Interface (RI) in NVIDIA Run:ai provides a declarative way to extend platform support for new workload types. It enables organizations to quickly incorporate emerging ML frameworks, tools, or Kubernetes resources without requiring platform updates or code changes. Administrators can introduce new workload types at any time through the [Workload Types](https://run-ai-docs.nvidia.com/api/2.25/workloads/workload-properties#post-api-v1-workload-types) API.

Once registered, these workloads become available across the organization, enabling teams to innovate and collaborate. Practitioners can then submit them using the [via YAML](/self-hosted/workloads-in-nvidia-run-ai/submit-via-yaml.md) submission and manage them with the same orchestration, monitoring, and scheduling capabilities as native workloads. For details on feature support, see [Supported features](/self-hosted/workloads-in-nvidia-run-ai/workload-types/supported-features.md).

{% hint style="info" %}
**Note**

NVIDIA Run:ai supports a broad range of workloads from the ML and Kubernetes ecosystem that are already registered as workload types in the platform and ready to use. See [Supported workload types](/self-hosted/workloads-in-nvidia-run-ai/workload-types/supported-workload-types.md).
{% endhint %}

## Resource Interface <a href="#resource-interface-overview" id="resource-interface-overview"></a>

The Resource Interface provides a YAML-based interface for defining how NVIDIA Run:ai should interpret, optimize, and monitor new workload types, without requiring platform updates or code changes. For more details on the the Resource Interface structure, see [Defining a resource interface](/self-hosted/workloads-in-nvidia-run-ai/workload-types/extending-workload-support/defining-a-resource-interface.md#resource-interface-structure).

### Core Functions <a href="#core-functions-of-rid" id="core-functions-of-rid"></a>

* **Structure Awareness** - Allow NVIDIA Run:ai to interpret the full composition of a workload, including component hierarchy, dependencies, and scaling logic. This ensures the platform can organize and optimize any supported workload, independent of framework or origin.
* **Monitoring and Status Mapping** - Defines how to track workload health by mapping specific status conditions from the framework to standard, abstract states (such as running, succeeded, failed). This mapping supports robust monitoring and lifecycle automation across diverse workload types.
* **Optimization Directives** - Encodes optimization strategies such as gang scheduling. These directives help ensure that workloads are utilized efficiently and reliably in any infrastructure environment.

### Structure Overview <a href="#rid-structure-overview" id="rid-structure-overview"></a>

A typical Resource Interface manifest includes the following primary sections:

* **structureDefinition** - Specifies all components (root, children), their types, hierarchical relationships, and how to interpret their specs within the overall workload.
* **optimizationInstructions** - Encapsulates how workloads should be scheduled and optimized (e.g., using gang scheduling).
* **scaleDefinition** - Explains how workload components can be scaled (manual, auto-scaling boundaries).
* **statusDefinition** - Maps resource-specific conditions to standard running/completed/failed states for unified monitoring.

## Registering New Workload Types

The [Workload Types](https://run-ai-docs.nvidia.com/api/2.25/workloads/workload-properties#post-api-v1-workload-types) API allows administrators to register and manage new workload types by providing the required details, such as workload name, supported CRD versions, category, priority, and Kubernetes group. For more details on registering new workload types, see [Defining a resource interface](/self-hosted/workloads-in-nvidia-run-ai/workload-types/extending-workload-support/defining-a-resource-interface.md).

`POST /api/v1/workload-types` with the following:

* `categoryId` - The identifier of the workload category.
* `priorityId` - The identifier of the workload priority.
* `preemptibility` - The preemptibility value of the workload - `non-preemptible` / `preemptible`.
* `name` - The unique name of the workload type. This value must exactly match the Kubernetes Kind that represents the workload type.
* `group` - The Kubernetes group associated with the workload resource.
* `resourceInterfaces` - Lists the versions of the custom resource definition (CRD) supported for this workload type, such as `v1`, `v1beta1`, or `v1alpha1`. This enables the platform to correctly parse, interpret, and manage manifests for this workload type according to the specific structure and schema associated with each listed version. On update, you may only add or remove supported versions, modifying existing version entries is not allowed.

**Example POST request body:**

<pre class="language-bash"><code class="lang-bash">{
<strong>  "categoryId": "337f5e5d-288b-40d5-be14-901cc3acacc0",
</strong>  "priorityId": "a57eab25-838b-40cc-a576-57e4056f1d6c",
  "preemptibility": "non-preemptible"
  "name": "Deployment",
<strong>  "group": "apps",
</strong>  "resourceInterfaces": [
    {
      "spec": {
        "structureDefinition": {
          "rootComponent": {
            "kind": {
              "group": "apps",
              "version": "v1",
              "kind": "Deployment"
             }
           }
        }
      }
    }
  ]
}
</code></pre>


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://run-ai-docs.nvidia.com/self-hosted/workloads-in-nvidia-run-ai/workload-types/extending-workload-support.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
