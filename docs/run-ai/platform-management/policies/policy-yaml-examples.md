# Policy YAML Examples

This guide provides examples of:

1. Creating a new rule within a policy
2. Best practices for adding sections to a policy
3. A full example of a whole policy

### Creating a New Rule Within a Policy

This example shows how to add a new limitation to the GPU usage for workloads of type workspace:

1. Check the [workload API](https://run-ai-docs.nvidia.com/api/2.25/policies/policy) fields documentation and select the field(s) that are most relevant for GPU usage.

   ```json
   {
   "spec": {
       "compute": {
       "gpuDevicesRequest": 1,
       "gpuRequestType": "portion",
       "gpuPortionRequest": 0.5,
       "gpuPortionLimit": 0.5,
       "gpuMemoryRequest": "10M",
       "gpuMemoryLimit": "10M",
       "migProfile": "1g.5gb",
       "cpuCoreRequest": 0.5,
       "cpuCoreLimit": 2,
       "cpuMemoryRequest": "20M",
       "cpuMemoryLimit": "30M",
       "largeShmRequest": false,
       "extendedResources": [
           {
           "resource": "hardware-vendor.example/foo",
           "quantity": 2,
           "exclude": false
           }
       ]
       },
   }
   }
   ```
2. Search the field in the [Policy YAML fields - reference table](/self-hosted/platform-management/policies/policy-yaml-reference.md). For example, gpuDevicesRequest appears under the **Compute fields** sub-table and appears as follow:

| Fields           | Description                                                                                                                           | Value type | Supported NVIDIA Run:ai workload type |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------- | ---------- | ------------------------------------- |
| gpuDeviceRequest | Specifies the number of GPUs to allocate for the created workload. Only if `gpuDeviceRequest = 1`, the gpuRequestType can be defined. | integer    | Workspace & Training                  |

3. Use the value type of the gpuDevicesRequest field indicated in the table - “integer” and navigate to the **Value types** table to view the possible rules that can be applied to this value type -

   for integer, the options are:

   * canEdit
   * required
   * min
   * max
   * step
4. Proceed to the [Rule Type](/self-hosted/platform-management/policies/policy-yaml-reference.md#rule-types) table, select the required rule for the limitation of the field - for example “max” and use the examples syntax to indicate the maximum GPU device requested.

```yaml
compute:
    gpuDevicesRequest:
        max: 2
```

### Policy YAML Best Practices

<details>

<summary>Create a policy that has multiple defaults and rules</summary>

**Best practices description**

Presentation of the syntax while adding a set of defaults and rules

**Example**

```yaml
defaults:
  createHomeDir: true
  environmentVariables:
    instances:
      - name: MY_ENV
        value: my_value
  security:
    allowPrivilegeEscalation: false

rules:
  storage:
    s3:
      attributes:
        url:
          options:
            - value: https://www.google.com
              displayed: https://www.google.com
            - value: https://www.yahoo.com
              displayed: https://www.yahoo.com
```

</details>

<details>

<summary>Allow only single selection out of many</summary>

**Best practices description**

Blocking the option to create all types of data sources except the one that is allowed is the solution

**Example**

```yaml
rules:
  storage:
    dataVolume:
      instances:
        canAdd: false
    hostPath:
      instances:
        canAdd: false
    pvc:
      instances:
        canAdd: false
    git:
      attributes:
        repository:
          required: true
        branch:
          required: true
        path:
          required: true
    nfs:
      instances:
        canAdd: false
    s3:
      instances:
        canAdd: false
```

</details>

<details>

<summary>Create a robust set of guidelines</summary>

**Best practices description**

Set rules for specific compute resource usage, addressing most relevant spec fields

**Example**

```yaml
compute:
    cpuCoreRequest:
      required: true
      min: 0
      max: 8
    cpuCoreLimit:
      min: 0
      max: 8
    cpuMemoryRequest:
      required: true
      min: '0'
      max: 16G
    cpuMemoryLimit:
      min: '0'
      max: 8G
    migProfile:
      canEdit: false
    gpuPortionRequest:
      min: 0
      max: 1
    gpuMemoryRequest:
      canEdit: false
    extendedResources:
      instances:
        canAdd: false
```

</details>

<details>

<summary>Policy for distributed training workloads</summary>

**Best practices description**

Set rules and defaults for a distributed training workload with different setting for master and workers

**Example**

```yaml
defaults:
  worker:
    command: my-command-worker-1
    environmentVariables:
      instances:
        - name: LOG_DIR
          value: policy-worker-to-be-ignored
        - name: ADDED_VAR
          value: policy-worker-added
    security:
      runAsUid: 500
    storage:
      s3:
        attributes:
          bucket: bucket1-worker
  master:
    command: my-command-master-2
    environmentVariables:
      instances:
        - name: LOG_DIR
          value: policy-master-to-be-ignored
        - name: ADDED_VAR
          value: policy-master-added
    security:
      runAsUid: 800
    storage:
      s3:
        attributes:
          bucket: bucket1-master
rules:
  worker:
    command:
      options:
        - value: my-command-worker-1
          displayed: command1
        - value: my-command-worker-2
          displayed: command2
    storage:
      nfs:
        instances:
          canAdd: false
      s3:
        attributes:
          bucket:
            options:
              - value: bucket1-worker
              - value: bucket2-worker
  master:
    command:
      options:
        - value: my-command-master-1
          displayed: command1
        - value: my-command-master-2
          displayed: command2
    storage:
      nfs:
        instances:
          canAdd: false
      s3:
        attributes:
          bucket:
            options:
              - value: bucket1-master
              - value: bucket2-maste
```

</details>

<details>

<summary>Examples for specific sections in the policy</summary>

**Best practices description**

Environment creation

**Example**

```yaml
rules:
  imagePullPolicy:
    required: true
    options:
      - value: Always
        displayed: Always
      - value: Never
        displayed: Never
  createHomeDir:
    canEdit: false
```

**Best practices description**

Setting security measures

**Example**

```yaml
rules:
  security:
    runAsUid:
      min: 1
      max: 32700
    allowPrivilegeEscalation:
      canEdit: false
```

**Best practices description**

Impose an asset

**Example**

<pre class="language-yaml"><code class="lang-yaml"><strong>defaults: null
</strong>rules: null
imposedAssets:
  - f12c965b-44e9-4ff6-8b43-01d8f9e630cc
</code></pre>

</details>

### Example of a Whole Policy

```yaml
defaults:
  createHomeDir: true
  imagePullPolicy: IfNotPresent
  nodePools:
    - node-pool-a
    - node-pool-b
  environmentVariables:
    instances:
      - name: WANDB_API_KEY
        value: REPLACE_ME!
      - name: WANDB_BASE_URL
        value: https://wandb.mydomain.com
  compute:
    cpuCoreRequest: 0.1
    cpuCoreLimit: 20
    cpuMemoryRequest: 10G
    cpuMemoryLimit: 40G
    largeShmRequest: true
  security:
    allowPrivilegeEscalation: false
  storage:
    git:
      attributes:
        repository: https://git-repo.my-domain.com
        branch: master
    hostPath:
      instances:
        - name: vol-data-1
          path: /data-1
          mountPath: /mount/data-1
        - name: vol-data-2
          path: /data-2
          mountPath: /mount/data-2
rules:
  createHomeDir:
    canEdit: false
  imagePullPolicy:
    canEdit: false
  environmentVariables:
    instances:
      locked:
        - WANDB_BASE_URL
  compute:
    cpuCoreRequest:
      max: 32
    cpuCoreLimit:
      max: 32
    cpuMemoryRequest:
      min: 1G
      max: 20G
    cpuMemoryLimit:
      min: 1G
      max: 40G
    largeShmRequest:
      canEdit: false
    extendedResources:
      instances:
        canAdd: false
  security:
    allowPrivilegeEscalation:
      canEdit: false
    runAsUid:
      min: 1
  storage:
    hostPath:
      instances:
        locked:
          - vol-data-1
          - vol-data-2
imposedAssets:
  - 4ba37689-f528-4eb6-9377-5e322780cc27

```


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://run-ai-docs.nvidia.com/self-hosted/platform-management/policies/policy-yaml-examples.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
