# Policies and Rules

At NVIDIA Run:ai, administrators can access a suite of tools designed to facilitate efficient account management. This article focuses on two key features: workload policies and workload scheduling rules. These features empower admins to establish default values and implement restrictions allowing enhanced control, assuring compatibility with organizational policies, and optimizing resource usage and utilization.

{% hint style="info" %}
**Note**

[Policies V1](https://docs.run.ai/latest/platform-admin/workloads/policies/old-policies/) are still supported but require additional setup. If you have policies on clusters prior to **NVIDIA Run:ai version 2.18** and upgraded to a newer version, contact [NVIDIA Run:ai Support](https://www.nvidia.com/en-eu/support/enterprise/#contact-us) for assistance in transitioning to the new policies framework.
{% endhint %}

## Workload Policies

A workload policy is an end-to-end solution for AI managers and administrators to control and simplify how workloads are submitted. This solution allows them to set best practices, enforce limitations, and standardize processes for the submission of workloads for AI projects within their organization. It acts as a key guideline for data scientists, researchers, ML & MLOps engineers by standardizing submission practices and simplifying the workload submission process.

### Why Use a Workload Policy?

Implementing workload policies is essential when managing complex AI projects within an enterprise for several reasons:

1. **Resource control and management** - Defining or limiting the use of costly resources across the enterprise via a centralized management system to ensure efficient allocation and prevent overuse.
2. **Setting best practices** - Provide managers with the ability to establish guidelines and standards to follow, reducing errors amongst AI practitioners within the organization.
3. **Security and compliance** - Define and enforce permitted and restricted actions to uphold organizational security and meet compliance requirements.
4. **Simplified setup** - Conveniently allow setting defaults and streamline the workload submission process for AI practitioners.
5. **Scalability and diversity**
   1. Multi-purpose clusters with various workload types that may have different requirements and characteristics for resource usage.
   2. The organization has multiple hierarchies, each with distinct goals, objectives, and degrees of flexibility.
   3. Manage multiple users and projects with distinct requirements and methods, ensuring appropriate utilization of resources.

### Understanding the Mechanism

The following sections provide details of how the workload policy mechanism works.

#### Cross-Interface Enforcement

The policy enforces the workloads regardless of whether they were submitted via UI, CLI, Rest APIs, or Kubernetes YAMLs.

#### Policy Types

NVIDIA Run:ai’s policies enforce NVIDIA Run:ai workloads. The policy type is per [NVIDIA Run:ai workload type](/self-hosted/workloads-in-nvidia-run-ai/workload-types.md). This allows administrators to set different policies for each workload type.

| Policy type           | Workload type         | Kubernetes name      |
| --------------------- | --------------------- | -------------------- |
| Workspace             | Workspace             | Interactive workload |
| Training: Standard    | Training: Standard    | Training workload    |
| Training: Distributed | Training: Distributed | Distributed workload |
| Inference             | Inference             | Inference workload   |

### Policy Structure - Rules, Defaults, and Imposed Assets

A policy consists of rules for limiting and controlling the values of fields of the workload. In addition to rules, some defaults allow the implementation of default values to different workload fields. These default values are not rules, as they simply suggest values that can be overridden during the workload submission.

Furthermore, policies allow the enforcement of workload assets. For example, as an admin, you can impose a data source of type PVC to be used by any workload submitted.

For more information, see [rules](/self-hosted/platform-management/policies/policy-yaml-reference.md#rules), [defaults](/self-hosted/platform-management/policies/policy-yaml-reference.md#defaults) and [imposed assets](/self-hosted/platform-management/policies/policies-and-rules.md).

## Scope of Effectiveness

Numerous teams working on various projects require the use of different tools, requirements, and safeguards. One policy may not suit all teams and their requirements. Hence, administrators can select the scope to cover the effectiveness of the policy. When a scope is selected, all of its subordinate units are also affected. As a result, all workloads submitted within the selected scope are controlled by the policy.

For example, if a policy is set for Department A, all workloads submitted by any of the projects within this department are controlled.

A scope for a policy can be:

![](/files/8CeCaFNbtME11vBapm9h)

{% hint style="info" %}
**Note**

The policy submission to the entire account scope is supported via API only.
{% endhint %}

The different scoping of policies also allows the breakdown of the responsibility between different administrators. This allows delegation of ownership between different levels within the organization. The policies, containing rules and defaults, propagate\* down the organizational tree, forming an “effective” policy that enforces any workload submitted by users within the project.

![](/files/ukWpZaVhHBWFk9pgG67M)

If a field is used by multiple policies at different scopes, the platform applies a reconciliation mechanism to determine which policy takes effect. Defaults of the same field can still be submitted by different organizational policies, as they are considered “soft” rules. In this case, the closest scope to the workload becomes the effective default (project default “wins” vs. department default, department default “wins” vs. cluster default, etc.). For rules, precedence depends on their type: simple rules on non-security and non-compute fields follow the same order as defaults (project > department > cluster), while strict rules on security and compute fields apply in reverse order (cluster > department > project).

<details>

<summary>NVIDIA Run:ai policies vs. Kyverno policies</summary>

Kyverno runs as a dynamic admission controller in a Kubernetes cluster. Kyverno receives validating and mutating admission webhook HTTP callbacks from the Kubernetes API server and applies matching policies to return results that enforce admission policies or reject requests. Kyverno policies can match resources using the resource kind, name, label selectors, and much more. For more information, see [How Kyverno Works](https://kyverno.io/docs/introduction/#how-kyverno-works).

</details>

### System Policies

By default, every account in NVIDIA Run:ai is governed by system policies that establish foundational security controls across all workloads, scopes, and interfaces (UI, CLI, API). These policies ensure consistent workload behavior and prevent unauthorized escalation. They can also be viewed as part of the effective policy for every scop&#x65;**.**

Administrators can create new policies to modify these defaults at any scope. This flexibility allows easing certain API restrictions that were previously enforced more strictly, while ensuring all changes are explicit and audited. Any update requires direct administrative action, adding an additional security layer.

* **Privileged parameter** - By default, the privileged parameter is set to `false` and is not editable (`canEdit: False`). This means containers are prevented from running with full host access, bypassing almost all container isolation, unless an administrator explicitly enables it.
* **Grace period** - Grace period defines how long a workload is allowed to continue running after a preemption request before it is terminated. The default grace period is 30 seconds, which may not always be sufficient for checkpointing or saving state. To support longer checkpointing operations, a maximum grace period of 5 minutes enforced by the system policy, which applies across API, CLI, and UI submissions. This period can be updated at any scope within the policy hierarchy.

## Scheduling Rules

[Scheduling rules](/self-hosted/platform-management/policies/scheduling-rules.md) limit a researcher's access to resources and provides a way for the admin to control resource allocation and prevent the waste of resources. Admins should use the rules to prevent GPU idleness, prevent GPU hogging and allocate specific types of resources to different types of workloads.

Admin can limit the duration of a workload, the duration of the idle time, or the type of nodes the workload can use. Rules are defined for and apply to all workloads in the project or department. In addition, rules can be applied to a specific type of workload in a project or department (workspace, standard training, or inference). When a workload reaches the limitation of the rule, it is stopped if the rule is time-limited. The rule type prevents the workload from being scheduled on nodes that violate the rule limitation.


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://run-ai-docs.nvidia.com/self-hosted/platform-management/policies/policies-and-rules.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
