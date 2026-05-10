# Hugging Face Distributed Inference Deployment

This tutorial demonstrates how to run a distributed inference workload using the Llama-3.1-405B-Instruct model. You can use this workflow as a reference and adapt it for your own models, container images, and hardware configurations.

{% hint style="info" %}
**Note**

Before running the vLLM example, verify that the [CUDA version](https://docs.vllm.ai/en/stable/getting_started/installation/gpu/) supported by vLLM is compatible with your target [GPU hardware](https://developer.nvidia.com/cuda/gpus).
{% endhint %}

In this tutorial, you will learn how to:

* Set up environment prerequisites for Hugging Face-based distributed inference
* Create a user access key for API integrations with NVIDIA Run:ai
* Create a user credential to store your Hugging Face token
* Create a PVC-based data source for model caching
* Deploy a distributed inference workload using the NVIDIA Run:ai REST API
* Access the inference endpoint to send requests

## Prerequisites

Before you start, make sure the following requirements are met:

* Your administrator has:
  * Created a [project](/self-hosted/platform-management/aiinitiatives/organization/projects.md) for you.
  * Installed and configured [LWS](/self-hosted/getting-started/installation/install-using-helm/system-requirements.md#distributed-inference) (Leader-Worker Set) on the cluster.
  * Configured external access if needed. Endpoints ending with `.svc.cluster.local` are accessible only inside the cluster; external access must be enabled by your administrator as described in the [inference requirements](/self-hosted/getting-started/installation/install-using-helm/system-requirements.md#inference) section.
* You have:
  * A Hugging Face account with an active personal access token, available under [Account Settings](https://huggingface.co/) → Access Tokens in your Hugging Face profile.
  * Accepted the model license for the [Llama-3.1-405B-Instruct](https://huggingface.co/meta-llama/Llama-3.1-405B-Instruct) model or for any other model you plan to use.

## Step 1: Logging In

{% tabs %}
{% tab title="UI" %}
Browse to the provided NVIDIA Run:ai user interface and log in with your credentials.
{% endtab %}

{% tab title="API" %}
To use the API, you will need to obtain a token as shown in [Creating a user access key](#step-2-creating-a-user-access-key).
{% endtab %}

{% tab title="CLI v2" %}
Run the below --help command to obtain the login options and log in according to your setup:

```sh
runai login --help
```

{% endtab %}
{% endtabs %}

## Step 2: Creating a User Access Key

{% hint style="info" %}
**Note**

This step is only required if you intend to follow the API steps in this tutorial.
{% endhint %}

Access keys are used for API integrations with NVIDIA Run:ai. An access key contains a client ID and a client secret. With the client credentials, you can obtain a token and use it within subsequent API calls.

In the NVIDIA Run:ai user interface:

1. Click the user avatar at the top right corner, then select **Settings**
2. Click **+ACCESS KEY**
3. Enter the access key's **name** and click **CREATE**
4. Copy the **Client ID** and **Client secret** and store securely
5. Click **DONE**

To request an API access token, use the client credentials to get a token to access NVIDIA Run:ai using the [Tokens](https://run-ai-docs.nvidia.com/api/2.25/authentication-and-authorization/tokens) API. For example:

```bash
curl -X POST \ 
  # Replace <COMPANY_URL> below with:
  # For SaaS, use <tenant-name>.run.ai
  # For self-hosted use the NVIDIA Run:ai user interface URL.
  'https://<COMPANY_URL>/api/v1/token' \ 
  --header 'Accept: */*' \ 
  --header 'Content-Type: application/json' \ 
  --data-raw '{ 
  "grantType":"client_credentials", 
  "clientId":"<CLIENT ID>", 
  "clientSecret" : "<CLIENT SECRET>" 
}'
```

## Step 3: Creating a User Credential

{% hint style="info" %}
**Note**

Creating user credentials is not available via API.
{% endhint %}

User credentials allow users to securely store private authentication secrets, which are accessible only to the user who created them. See [User credentials](/self-hosted/settings/user-settings/user-credentials.md) for more details.

In the NVIDIA Run:ai user interface:

1. Click the user avatar at the top right corner, then select **Settings**
2. Click **+CREDENTIAL** and select **Generic secret** from the dropdown
3. Enter a **name** for the credential. The name must be unique.
4. Optional: Provide a description of the credential
5. Enter the following:
   * **Key** - `HF_TOKEN`
   * **Value -** `<YOUR_HF_TOKEN>`
6. Click **CREATE CREDENTIAL**

## Step 4: Creating a PVC Data Source

To make it easier to reuse code and checkpoints in future workloads, create a data source in the form of a Persistent Volume Claim (PVC). The PVC can be mounted to workloads and will persist after the workload completes, allowing any data it contains to be reused.

{% hint style="info" %}
**Note**

The first time a workload is launched using a new PVC, it will take longer to start as the storage gets provisioned only once the first claim to the PVC is made.
{% endhint %}

{% tabs %}
{% tab title="UI" %}

1. To create a PVC, go to Workload manager → Data sources.
2. Click +**NEW DATA SOURCE** and select **PVC** from the dropdown menu.
3. Within the new form, set the [scope](/self-hosted/workloads-in-nvidia-run-ai/assets/overview.md#asset-scope).

{% hint style="info" %}
**Important**

PVC data sources created at the cluster or department level do not replicate data across projects or namespaces. Each project or namespace will be provisioned as a separate PVC replica with different underlying PVs; therefore, the data in each PVC is not replicated.
{% endhint %}

4. Enter a **name** for the data source. The name must be unique.
5. For the data options, select **New PVC** and the **storage class** that suits your needs:
   * To allow all nodes to read and write from/to the PVC, select **Read-write by many nodes** for the **access mode**.
   * Enter `2 TB` for the **claim size** to ensure we have plenty of capacity for future workloads
   * Select **Filesystem** (default) as the volume mode. The volume will be mounted as a filesystem, enabling the usage of directories and files.
   * Set the **Container path** to `/models` which is where the PVC will be mounted inside containers.
6. Click **CREATE DATA SOURCE**

After creating the data source, wait for the PVC to be provisioned. The PVC claim name (which is displayed in the UI as the Kubernetes name) will appear in the Data sources grid once it’s ready. This claim name is the exact value that will be used for the `<pvc-claim-name>` when submitting the workload.
{% endtab %}

{% tab title="API" %}
Copy the following command to your terminal. Make sure to update the following parameters:

* `<COMPANY-URL>` - The link to the NVIDIA Run:ai user interface.
* `<TOKEN>` - The API access token obtained in [Step 2](#step-2-creating-a-user-access-key).

For all other parameters within the JSON body, refer to the [PVC](https://run-ai-docs.nvidia.com/api/2.25/workload-assets/pvc) API.

After creating the data source, wait for the PVC to be provisioned. Use the [List PVC asset](https://run-ai-docs.nvidia.com/api/2.25/workload-assets/pvc#get-api-v1-asset-datasource-pvc) API to retrieve the claim name. This claim name is the exact value that will be used for the `<pvc-claim-name>` when submitting the workload.

```bash
curl -L 'https://<COMPANY-URL>/api/v1/asset/datasource/pvc' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer <TOKEN>' \
  -d '{
    "meta": {
      "name": "<pvc-name>",
      "scope": "<scope>"
    },
    "spec": {
      "path": "/models",
      "existingPvc": false,
      "claimInfo": {
        "size": "2TB",
        "storageClass": "<my-storage-class>",
        "accessModes": {
          "readWriteMany": true
        },
        "volumeMode": "Filesystem"
      }
    }
  }'
```

{% endtab %}
{% endtabs %}

## Step 5: Creating the Workload

This step launches a multi-node vLLM inference cluster for the Llama-3.1-405B-Instruct model. The configuration below defines how the workload is distributed across nodes, how authentication is applied, and how model assets are cached for reuse.

### How the Configuration Works

* `workers` - Defines the number of worker nodes that participate in the distributed inference. Each worker runs a vLLM process and communicates with the leader node using Ray. In this tutorial, one worker and one leader run across two nodes, each contributing 8 GPUs for a total of 16 GPUs.
* `servingPort.authorizationType` - Controls who can access the inference endpoint. In this tutorial, it’s set to `authenticatedUsers`, meaning only authenticated NVIDIA Run:ai users with valid tokens can send requests. By default, inference endpoints are public; adding authentication ensures that only authorized users can access the deployed model.
* Leader and worker configuration - The leader runs both the Ray head node and the OpenAI-compatible API server. The workers connect to the leader via `$(LWS_LEADER_ADDRESS)` to form a Ray cluster that shares the model state across multiple GPUs and nodes.
* `HF_TOKEN` - Stored securely as a user credential and injected into both leader and worker containers. It authorizes model downloads from Hugging Face.
* PVC mount at `/models` - The shared Persistent Volume Claim (PVC) ensures that downloaded model weights are cached and reused across multiple runs, reducing startup time.
* `largeShmRequest` - Enables allocation of large shared memory, required for high-throughput inference workloads.
* `gpuDevicesRequest` - Specifies the number of GPUs requested by each leader and worker pod, matching the required tensor parallel size.
* `runAsUid`, `runAsGid`, and `runAsNonRoot` - Defines the security context under which the container runs. In OpenShift environments, both the leader and worker pods must run with a non-root user and group (`UID`/`GID 1000`). Without this configuration, pods may encounter permission errors during the model download phase because the mounted cache path is owned by `root`

### Submitting the Workload

{% tabs %}
{% tab title="API" %}
Copy the following command to your terminal. Make sure to update the following parameters. For more details, see [Distributed Inferences](https://run-ai-docs.nvidia.com/api/2.25/workloads/distributed-inferences) API:

* `<COMPANY-URL>` - The link to the NVIDIA Run:ai user interface.
* `<TOKEN>` - The API access token obtained in [Step 2](#step-2-creating-a-user-access-key).
* `<PROJECT-ID>` - The ID of the Project the workload is running on. You can get the Project ID via the [Get Projects](https://run-ai-docs.nvidia.com/api/2.25/organizations/projects#get-api-v1-org-unit-projects) API.
* `<CLUSTER-UUID>` - The unique identifier of the Cluster. You can get the Cluster UUID via the [Get Clusters](https://run-ai-docs.nvidia.com/api/2.25/organizations/clusters#get-api-v1-clusters) API.
* `<genericsecret-name>` - The name of the user credential created in [Step 3](#step-3-creating-a-user-credential). Replace this with the name of the credential preceded by the system prefix `genericsecret-`. For example, if you named your credential `hftoken`, the value here is `genericsecret-hftoken`.
* `<pvc-claim-name>` - The claim name associated with the PVC created in [Step 4](#step-4-creating-a-pvc-data-source).
* `security` - The security parameters are required for OpenShift environments only.

```bash
curl -L 'https://<COMPANY-URL>/api/v1/workloads/distributed-inferences' \ 
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer <TOKEN>' \
-d '{  
    "name": "<workload-name>",
    "projectId": "<PROJECT-ID>",
    "clusterId": "<CLUSTER-UUID>",
    "spec": {
        "workers": 1,
        "replicas": 1,
        "servingPort": {
            "port": 8000,
            "authorizationType": "authenticatedUsers"
        },
        "leader": {
            "image": "vllm/vllm-openai:latest",
            "command": "sh -c \"bash /vllm-workspace/examples/online_serving/multi-node-serving.sh leader --ray_cluster_size=$(LWS_GROUP_SIZE); python3 -m vllm.entrypoints.openai.api_server --port 8000 --model meta-llama/Llama-3.1-405B-Instruct --tensor-parallel-size 8 --pipeline_parallel_size 2\"",
            "environmentVariables": [
                {
                    "name": "HF_HOME",
                    "value": "/models"
                },
                {
                    "name": "HF_TOKEN",
                    "secret": {
                        "name": "<genericsecret-name>",
                        "key": "HF_TOKEN"
                    }
                }
            ],
            "compute": {
                "largeShmRequest": true,
                "gpuDevicesRequest": 8
            },
            "security": { 
                "runAsUid": 1000,
                "runAsGid": 1000,
                "runAsNonRoot": true
            },
            "storage": {
                "pvc": [
                    {
                        "name": "<pvc-name>",
                        "path": "/models",
                        "existingPvc": true,
                        "claimName": "<pvc-claim-name>"
                    }
                ]
            }
        },
        "worker": {
            "image": "vllm/vllm-openai:latest",
            "command": "sh -c \"bash /vllm-workspace/examples/online_serving/multi-node-serving.sh worker --ray_address=$(LWS_LEADER_ADDRESS)\"",
             "environmentVariables": [
                {
                    "name": "HF_HOME",
                    "value": "/models"
                },
                {
                    "name": "HF_TOKEN",
                    "secret": {
                        "name": "<genericsecret-name>",
                        "key": "HF_TOKEN"
                    }
                }
            ],
           "compute": {
                "largeShmRequest": true,
                "gpuDevicesRequest": 8
            },
            "security": {
                "runAsUid": 1000,
                "runAsGid": 1000,
                "runAsNonRoot": true
            },
            "storage": {
                "pvc": [
                    {
                        "name": "<pvc-name>",
                        "path": "/models",
                        "existingPvc": true,
                        "claimName": "<pvc-claim-name>"
                    }
                ]
            }
        }
    }
}
```

{% endtab %}

{% tab title="CLI v2" %}
Copy the following command to your terminal. Make sure to update the below with the name of your project and workload. For more details, see [CLI reference](/self-hosted/reference/cli/runai.md):

```sh
runai inference distributed submit <workload-name> \
    -p <PROJECT-NAME> \
    -i vllm/vllm-openai:latest \
    --workers 1 \
    --replicas 1 \
    -g 8 \
    --large-shm \
    --serving-port "container=8000,authorization-type=authenticatedUsers" \
    --existing-pvc "claimname=<pvc-claim-name>,path=/models" \
    --environment "HF_HOME=/models" \
    --env-secret "HF_TOKEN=<your-secret-name>,key=HF_TOKEN" \
    --command "sh -c \"bash /vllm-workspace/examples/online_serving/multi-node-serving.sh leader --ray_cluster_size=\$(LWS_GROUP_SIZE); python3 -m vllm.entrypoints.openai.api_server --port 8000 --model meta-llama/Llama-3.1-405B-Instruct --tensor-parallel-size 8 --pipeline_parallel_size 2\"" \
    --worker-command "sh -c \"bash /vllm-workspace/examples/online_serving/multi-node-serving.sh worker --ray_address=\$(LWS_LEADER_ADDRESS)\"" \
    --run-as-uid 1000 \ # Required for OpenShift environments only
    --run-as-gid 1000 \ # Required for OpenShift environments only
    --run-as-non-root # Required for OpenShift environments only
```

{% endtab %}
{% endtabs %}

## Step 6: Verifying the Workload Status

After submitting the workload, wait for it to reach the Running status in the [Workloads](/self-hosted/workloads-in-nvidia-run-ai/workloads.md) table. A workload becomes Ready to accept inference requests only after all its pods have fully initialized, including model loading.

Large models may require several minutes to load their weights, especially when the model is stored on a PVC. During this time, the workload may remain in **Initializing** even though pods are already running.

To monitor progress:

* Select the workload and click the SHOW DETAILS button at the upper-right side of the action bar. The details pane appears, presenting the Logs tab to track model-download and model-loading progress. Select the relevant pod from the dropdown and review the pod logs.
* The workload transitions to **Running** only when the leader pod finishes loading the model and all readiness checks pass.

Once the workload reaches **Running** and shows an available **Connection**, you can proceed to access the inference endpoint.

## Step 7: Accessing the Inference Workload

You can programmatically consume an inference workload via API by making direct calls to the serving endpoint, typically from other workloads or external integrations. Once an inference workload is deployed, the serving endpoint URL appears in the **Connections** column of the [Workloads](/self-hosted/workloads-in-nvidia-run-ai/workloads.md) table. To retrieve the service endpoint programmatically, use the [Get Workloads](https://run-ai-docs.nvidia.com/api/2.25/workloads/workloads#get-api-v1-workloads) API. The endpoint URL will be available in the response body under `endpoints`.

{% hint style="info" %}
**Note**

For clusters below version 2.25, the endpoint URL will be available in the response body under `urls`.
{% endhint %}

By default, inference endpoints in NVIDIA Run:ai are configured with public access, meaning no authentication is required to send requests. In this tutorial, the `servingPort` is configured with the `authenticatedUsers` as the `authorizationType`. This means only authenticated users with a valid access token can call the inference endpoint.

Use the token you obtained in [Step 2](#step-2-creating-a-user-access-key) to authenticate your requests, and include it in the request header as shown below:

```bash
#replace <serving-endpoint-url> and <model-name> (e.g. "meta-llama/Llama-3.1-8B-Instruct")
curl <serving-endpoint-url>/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-access-token>" \
  -d '{
    "model": "<model-name>",
    "messages": [{
      "role": "user",
      "content": "Write a short poem on AI"
    }]
  }'
```

## Step 8: Cleaning up the Environment

After the workload finishes, it can be deleted to free up resources for other workloads. To reclaim the disk space used by the PVC, delete the PVC once it is no longer needed.


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://run-ai-docs.nvidia.com/self-hosted/tutorials/inference-tutorials/hugging-face-distributed.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
