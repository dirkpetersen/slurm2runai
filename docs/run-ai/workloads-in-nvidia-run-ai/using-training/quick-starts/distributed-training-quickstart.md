# Run Your First Distributed Training

This quick start provides a step-by-step walkthrough for running a PyTorch distributed training workload.

Distributed training is the ability to split the training of a model among multiple processors. Each processor is called a worker. Worker nodes work in parallel to speed up model training. There is also a master which coordinates the workers.

{% hint style="info" %}
**Note**

Multi-GPU training and distributed training are two distinct concepts. Multi-GPU training uses multiple GPUs within a single node, whereas distributed training spans multiple nodes and typically requires coordination between them.
{% endhint %}

## Prerequisites

Before you start, make sure:

* You have created a [project](/self-hosted/platform-management/aiinitiatives/organization/projects.md) or have one created for you.
* The project has an assigned quota of at least 1 GPU.

{% hint style="info" %}
**Note**

Flexible workload submission is enabled by default. If unavailable, contact your administrator to enable it under **General settings** → Workloads → Flexible workload submission.
{% endhint %}

## Step 1: Logging In

{% tabs %}
{% tab title="UI" %}
Browse to the provided NVIDIA Run:ai user interface and log in with your credentials.
{% endtab %}

{% tab title="CLI v2" %}
Run the below --help command to obtain the login options and log in according to your setup:

```sh
runai login --help
```

{% endtab %}

{% tab title="API" %}
To use the API, you will need to obtain a token as shown in [API authentication](https://run-ai-docs.nvidia.com/api/2.25/getting-started/how-to-authenticate-to-the-api).
{% endtab %}
{% endtabs %}

## Step 2: Submitting a Distributed Training Workload

{% tabs %}
{% tab title="UI - Flexible" %}

1. Go to the Workload manager → Workloads
2. Click **+NEW WORKLOAD** and select **Training**
3. Select under which **cluster** to create the workload
4. Select the **project** in which your workload will run
5. Under **Workload architecture,** select **Distributed**
6. Select **PyTorch** as the distributed framework and the distributed training configuration to **Worker & master**
7. Select **Start from scratch** to launch a new workload quickly
8. Enter a **name** for the training workload (if the name already exists in the project, you will be requested to submit a different name)
9. Click **CONTINUE**

   In the next step:
10. Under **Environment**, enter the **Image URL** - `kubeflow/pytorch-dist-mnist:latest`
11. Under **Compute resources**, click the **load** icon. A side pane appears, displaying a list of available compute resources. Select the **‘small-fraction’** compute resource for your workload.
    * If ‘small-fraction’ is not displayed, follow the below steps to create a one-time compute resource configuration:
      * Set **GPU devices** per pod - 1
      * Enable **GPU fractioning** to set the GPU memory per device:
        * Select **% (of device)** - Fraction of a GPU device’s memory
        * Set the memory **Request** - 10 (the workload will allocate 10% of the GPU memory)
      * Optional: set the **CPU compute per pod** - 0.1 cores (default)
      * Optional: set the **CPU memory per pod** - 100 MB (default)
12. Click **CONTINUE**
13. Click **CREATE TRAINING**
    {% endtab %}

{% tab title="UI - Original" %}

1. Go to the Workload manager → Workloads
2. Click **+NEW WORKLOAD** and select **Training**
3. Select under which **cluster** to create the workload
4. Select the **project** in which your workload will run
5. Under **Workload architecture,** select **Distributed**
6. Select **PyTorch** as the distributed framework and the distributed training configuration to **Worker & master**
7. Select **Start from scratch** to launch a new workload quickly
8. Enter a **name** for the training workload (if the name already exists in the project, you will be requested to submit a different name)
9. Click **CONTINUE**

   In the next step:
10. Create an environment for your workload

    * Click **+NEW ENVIRONMENT**
    * Enter pytorch-dt as the **name** for the environment. The name must be unique.
    * Enter `kubeflow/pytorch-dist-mnist:latest` as the **Image URL**
    * Click **CREATE ENVIRONMENT**

    The newly created environment will be selected automatically
11. Select the **‘small-fraction’** compute resource for your workload

    * If ‘small-fraction’ is not displayed in the gallery, follow the below steps:
      * Click **+NEW COMPUTE RESOURCE**
      * Enter small-fraction as the **name** for the compute resource. The name must be unique.
      * Set **GPU devices** per pod - 1
      * Enable **GPU fractioning** to set the GPU memory per device:
        * Select **% (of device)** - Fraction of a GPU device’s memory
        * Set the memory **Request** - 10 (the workload will allocate 10% of the GPU memory)
      * Optional: set the **CPU compute per pod** - 0.1 cores (default)
      * Optional: set the **CPU memory per pod** - 100 MB (default)
      * Click **CREATE COMPUTE RESOURCE**

    The newly created compute resource will be selected automatically
12. Click **CONTINUE**
13. Click **CREATE TRAINING**
    {% endtab %}

{% tab title="CLI v2" %}
Copy the following command to your terminal. Make sure to update the below with the name of your project and workload. For more details, see [CLI reference](/self-hosted/reference/cli/runai.md):

<pre class="language-sh"><code class="lang-sh">runai project set "project-name"
<strong>runai training pytorch submit "workload-name" \
</strong>-i kubeflow/pytorch-dist-mnist:latest --workers 2 \
--gpu-request-type portion --gpu-portion-request 0.1 \
--gpu-devices-request 1 --cpu-memory-request 100M
</code></pre>

{% endtab %}

{% tab title="API" %}
Copy the following command to your terminal. Make sure to update the following parameters. For more details, see [Distributed](https://run-ai-docs.nvidia.com/api/2.25/workloads/distributed) API:

```bash
curl -L 'https://<COMPANY-URL>/api/v1/workloads/distributed' \
-H 'Content-Type: application/json' \ 
-H 'Authorization: Bearer <TOKEN>' \   
-d '{  
    "name": "workload-name",  
    "projectId": "<PROJECT-ID>",
    "clusterId": "<CLUSTER-UUID>",  
    "spec": {  
        "compute": { 
            "cpuCoreRequest": 0.1,
            "gpuRequestType": "portion",
            "cpuMemoryRequest": "100M",
            "gpuDevicesRequest": 1,
            "gpuPortionRequest": 0.1
        },
        "image": "kubeflow/pytorch-dist-mnist:latest",  
        "numWorkers": 2, 
        "distributedFramework": "PyTorch" 
    } 
}
```

* `<COMPANY-URL>` - The link to the NVIDIA Run:ai user interface
* `<TOKEN>` - The API access token obtained in [Step 1](#step-1-logging-in)
* `<PROJECT-ID>` - The ID of the Project the workload is running on. You can get the Project ID via the [Get Projects](https://run-ai-docs.nvidia.com/api/2.25/organizations/projects#get-api-v1-org-unit-projects) API.
* `<CLUSTER-UUID>` - The unique identifier of the Cluster. You can get the Cluster UUID via the [Get Clusters](https://run-ai-docs.nvidia.com/api/2.25/organizations/clusters#get-api-v1-clusters) API.

{% hint style="info" %}
**Note**

The above API snippet runs with NVIDIA Run:ai clusters of 2.18 and above only.
{% endhint %}
{% endtab %}
{% endtabs %}

## Next Steps

* Manage and monitor your newly created workload using the [Workloads](/self-hosted/workloads-in-nvidia-run-ai/workloads.md) table.
* After validating your training performance and results, deploy your model using [inference](/self-hosted/workloads-in-nvidia-run-ai/using-inference.md).


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://run-ai-docs.nvidia.com/self-hosted/workloads-in-nvidia-run-ai/using-training/quick-starts/distributed-training-quickstart.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
