# Integrations

Integrations are Kubernetes components and external tools that can be used with NVIDIA Run:ai for development, training, orchestration, data access, and monitoring.

Integrations fall into two support levels:

* **Supported integrations (out of the box)** - NVIDIA Run:ai includes built-in support and documentation. You may still need cluster-side installation (for example, install an operator and its CRDs) before you can use the integration.
* **Community Support integrations** - Not supported out of the box, but commonly used with prior customer support experience and reference guides.

## Supported Integrations

### Frameworks

<table><thead><tr><th width="110.7734375">Framework</th><th width="127.54296875">Category</th><th>Supported Version</th><th width="500.12109375">Additional Information</th></tr></thead><tbody><tr><td>Dynamo operator</td><td>Distributed inference</td><td>1.0.1</td><td><p>Dynamo operator is a Kubernetes operator that simplifies the deployment, configuration, and lifecycle management of DynamoGraphs.</p><p>NVIDIA Run:ai provides out of the box support for submitting Dynamo workloads <a href="/pages/KKrO2XsA4frD47Ef0mNg">via YAML</a>. See <a href="https://docs.nvidia.com/dynamo/latest/">Dynamo operator</a> documentation for more details.</p></td></tr><tr><td>NIM operator</td><td>Model Serving</td><td>3.0.x</td><td><p>The NVIDIA NIM Operator enables Kubernetes cluster administrators to operate the software components and services necessary to deploy NVIDIA NIMs and NVIDIA NeMo microservices in Kubernetes.</p><p>NVIDIA Run:ai provides out of the box support for submitting NIM operator workloads <a href="/pages/KKrO2XsA4frD47Ef0mNg">via YAML</a>. See <a href="https://docs.nvidia.com/nim-operator/latest/">NIM operator</a> documentation for more details.</p></td></tr><tr><td>LeaderWorkerSet (LWS)</td><td>Distributed inference</td><td>0.6.0 or higher</td><td>NVIDIA Run:ai provides out of the box support for submitting <a href="https://github.com/kubernetes-sigs/lws">LWS</a> workloads <a href="/pages/KKrO2XsA4frD47Ef0mNg">via YAML</a> and NVIDIA Run:ai native <a href="/pages/vI3gSzBeMN1y20qLc1kk">distributed inference</a> workloads using LWS.</td></tr><tr><td>Kubeflow MPI</td><td>Distributed training</td><td>MPI Operator v0.6.0 or higher</td><td>NVIDIA Run:ai provides out of the box support for submitting MPI workloads via API, CLI or UI. See <a href="/pages/2FK3NdOgMsyGeuEv4UCr">Distributed training</a> for more details.</td></tr><tr><td>PyTorch</td><td>Distributed training</td><td>Kubeflow Training Operator v1.9.2</td><td>NVIDIA Run:ai provides out of the box support for submitting PyTorch workloads via API, CLI or UI. See <a href="/pages/2FK3NdOgMsyGeuEv4UCr">Distributed training</a> for more details.</td></tr><tr><td>TensorFlow</td><td>Distributed training</td><td>Kubeflow Training Operator v1.9.2</td><td>NVIDIA Run:ai provides out of the box support for submitting TensorFlow workloads via API, CLI or UI. See <a href="/pages/2FK3NdOgMsyGeuEv4UCr">Distributed training</a> for more details.</td></tr><tr><td>XGBoost</td><td>Distributed training</td><td>Kubeflow Training Operator v1.9.2</td><td>NVIDIA Run:ai provides out of the box support for submitting XGBoost via API, CLI or UI. See <a href="/pages/2FK3NdOgMsyGeuEv4UCr">Distributed training</a> for more details.</td></tr><tr><td>JAX</td><td>Distributed training</td><td>Kubeflow Training Operator v1.9.2</td><td>NVIDIA Run:ai provides out of the box support for submitting JAX workloads via API, CLI or UI. See <a href="/pages/2FK3NdOgMsyGeuEv4UCr">Distributed training</a> for more details.</td></tr><tr><td>Triton</td><td>Orchestration</td><td>Any version</td><td>Usage via docker base image</td></tr></tbody></table>

### Development Tools

<table><thead><tr><th width="110.7734375">Tool</th><th width="127.54296875">Category</th><th width="502.9609375">Additional Information</th></tr></thead><tbody><tr><td>Jupyter Notebook</td><td>Development</td><td>NVIDIA Run:ai provides integrated support with Jupyter Notebooks. See <a href="/pages/CO4emu3ivhfKCGa3nit0">Jupyter Notebook quick start</a> example.</td></tr><tr><td>PyCharm</td><td>Development</td><td>Containers created by NVIDIA Run:ai can be accessed via PyCharm.</td></tr><tr><td>VScode</td><td>Development</td><td>Containers created by NVIDIA Run:ai can be accessed via Visual Studio Code. You can automatically launch Visual Studio code web from the NVIDIA Run:ai console.</td></tr></tbody></table>

### Storage and Registries

<table><thead><tr><th width="110.7734375">Tool</th><th width="127.54296875">Category</th><th width="507.38671875">Additional Information</th></tr></thead><tbody><tr><td>Docker Registry</td><td>Repositories</td><td>NVIDIA Run:ai allows using a docker registry as a <a href="/pages/IN6wqkth0XJsDdduiWL4">Credential</a> asset</td></tr><tr><td>GitHub</td><td>Storage</td><td>NVIDIA Run:ai communicates with GitHub by defining it as a <a href="/pages/K1baT6ooeG2jEej6jY0r">data source</a> asset</td></tr><tr><td>S3</td><td>Storage</td><td>NVIDIA Run:ai communicates with S3 by defining a <a href="/pages/K1baT6ooeG2jEej6jY0r">data source</a> asset</td></tr></tbody></table>

### Experiment Tracking and Monitoring

<table><thead><tr><th width="110.7734375">Tool</th><th width="127.54296875">Category</th><th width="510.625">Additional Information</th></tr></thead><tbody><tr><td>TensorBoard</td><td>Experiment tracking</td><td>NVIDIA Run:ai comes with a preset TensorBoard <a href="/pages/ra7b3yHFnCl3QEZcZ27H">Environment</a> asset</td></tr></tbody></table>

### Infrastructure and Cost Optimization

<table><thead><tr><th width="110.7734375">Tool</th><th width="127.54296875">Category</th><th width="507.65625">Additional Information</th></tr></thead><tbody><tr><td>Karpenter</td><td>Cost Optimization</td><td>NVIDIA Run:ai provides out of the box support for Karpenter to save cloud costs. Integration notes with Karpenter can be found <a href="/pages/JBBTIuioyuYVMAFwaRWT">here</a>.</td></tr></tbody></table>

## Community Support Integrations

Our Customer Success team has prior experience assisting customers with setup. In many cases, the NVIDIA Enterprise Support Portal may include additional reference documentation provided on an as-is basis.

<table><thead><tr><th width="110.7734375">Tool</th><th width="127.54296875">Category</th><th width="509.7734375">Additional Information</th></tr></thead><tbody><tr><td>Apache Airflow</td><td>Orchestration</td><td>It is possible to schedule Airflow workflows with the NVIDIA Run:ai Scheduler. Sample code: <a href="https://enterprise-support.nvidia.com/s/article/How-to-integrate-Run-ai-with-Apache-Airflow">How to integrate NVIDIA Run:ai with Apache Airflow</a>.</td></tr><tr><td>Argo workflows</td><td>Orchestration</td><td>It is possible to schedule Argo workflows with the NVIDIA Run:ai Scheduler. Sample code: <a href="https://enterprise-support.nvidia.com/s/article/How-to-integrate-Run-ai-with-Argo-Workflows">How to integrate NVIDIA Run:ai with Argo Workflows</a>.</td></tr><tr><td>ClearML</td><td>Experiment tracking</td><td>It is possible to schedule ClearML workloads with the NVIDIA Run:ai Scheduler.</td></tr><tr><td>JupyterHub</td><td>Development</td><td>It is possible to submit NVIDIA Run:ai workloads via JupyterHub.</td></tr><tr><td>Kubeflow notebooks</td><td>Development</td><td>It is possible to launch a Kubeflow notebook with the NVIDIA Run:ai Scheduler. Sample code: <a href="https://enterprise-support.nvidia.com/s/article/How-to-integrate-Run-ai-with-Kubeflow">How to integrate NVIDIA Run:ai with Kubeflow</a>.</td></tr><tr><td>Kubeflow Pipelines</td><td>Orchestration</td><td>It is possible to schedule kubeflow pipelines with the NVIDIA Run:ai Scheduler. Sample code: <a href="https://enterprise-support.nvidia.com/s/article/How-to-integrate-Run-ai-with-Kubeflow">How to integrate NVIDIA Run:ai with Kubeflow</a>.</td></tr><tr><td>MLFlow</td><td>Model Serving</td><td>It is possible to use ML Flow together with the NVIDIA Run:ai Scheduler.</td></tr><tr><td>Ray</td><td>Training, inference, data processing</td><td>It is possible to schedule Ray jobs with the NVIDIA Run:ai Scheduler. Sample code: <a href="https://enterprise-support.nvidia.com/s/article/How-to-Integrate-Run-ai-with-Ray">How to Integrate NVIDIA Run:ai with Ray</a>.</td></tr><tr><td>SeldonX</td><td>Orchestration</td><td>It is possible to schedule Seldon Core workloads with the NVIDIA Run:ai Scheduler.</td></tr><tr><td>Spark</td><td>Orchestration</td><td>It is possible to schedule Spark workflows with the NVIDIA Run:ai Scheduler.</td></tr><tr><td>Weights &#x26; Biases</td><td>Experiment tracking</td><td>It is possible to schedule W&#x26;B workloads with the NVIDIA Run:ai Scheduler. Sample code: <a href="https://enterprise-support.nvidia.com/s/article/How-to-integrate-with-Weights-and-Biases">How to integrate with Weights and Biases</a>.</td></tr></tbody></table>


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://run-ai-docs.nvidia.com/self-hosted/infrastructure-setup/advanced-setup/integrations.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
