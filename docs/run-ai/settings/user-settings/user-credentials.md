# User Credentials

Credentials allow users to securely store private authentication secrets, which are accessible only to the user who created them. These credentials can be used to authorize access to external systems and services. You can create:

* **Docker registry credentials** - Used to authenticate and pull container images from private Docker registries. These credentials are used as image pull secrets during workload submission.
* **Generic secrets** - A flexible option for storing key/value pairs such as API keys or configuration data. These credentials can be injected into workloads as environment variables.
* **NGC API key** - Used to securely store the NGC API key for authenticated access to restricted data in the NGC catalog. These credentials can be injected into workloads to access the NGC catalog and as environment variables.

{% hint style="info" %}
**Note**

User credentials will be propagated to all clusters from versions 2.22 onwards.
{% endhint %}

## Creating a Credential

1. Click the user avatar at the top right corner, then select **Settings**
2. Click **+CREDENTIAL** and select either **Docker registry,** **Generic secret** or **NGC API key** from the dropdown menu
3. Enter a **name** for the credential. The name must be unique.
4. Optional: Provide a description of the credential
5. Enter the following:
   * **Docker registry** - The **username**, **password**, and **Docker registry URL**
   * **Generic secret** - The **key/value** pairs to store in the new secret. You can add multiple key/value pairs.
   * **NGC API key** - Your **NGC API key**. To obtain a key, go to [NGC](https://catalog.ngc.nvidia.com/) → Setup → API Key, then generate or copy an existing key.
6. Click **CREATE CREDENTIAL**

## Deleting a Credential

1. Locate the credential you want to delete
2. Click on the trash icon
3. On the dialog, click **DELETE** to confirm


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://run-ai-docs.nvidia.com/self-hosted/settings/user-settings/user-credentials.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
