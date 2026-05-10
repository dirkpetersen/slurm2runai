# User Access Keys (formerly applications)

Access keys are used for API integrations with NVIDIA Run:ai. An access key contains a client ID and a client secret. With the client credentials, you can obtain a token as detailed in [API authentication](https://run-ai-docs.nvidia.com/api/2.25/getting-started/how-to-authenticate-to-the-api) and use it within subsequent API calls.

{% hint style="info" %}
**Note**

* All clusters in the tenant must be version 2.20 and onward.
* The token obtained through access keys assumes the [roles and permissions](/self-hosted/infrastructure-setup/authentication/roles.md) of the user.
  {% endhint %}

## Creating Access Key

To create an access key:

1. Click the user avatar at the top right corner, then select **Settings**
2. Click **+ACCESS KEY**
3. Enter the access key's **name**
4. Click **CREATE**
5. Copy the **Client ID** and **Client secret** and store securely
6. Click **DONE**

You can create up to 20 access keys.

{% hint style="info" %}
**Note**

The client secret is visible only at the time of creation. It cannot be recovered but can be regenerated.
{% endhint %}

## Regenerating a Client Secret

To regenerate a client secret:

1. Locate the access key you want to regenerate its client secret
2. Click **Regenerate client secret**
3. Click **REGENERATE**
4. Copy the **New client secret** and store it securely
5. Click **DONE**

{% hint style="warning" %}
**Important**

Regenerating a client secret revokes the previous one.
{% endhint %}

## Deleting an Access Key

1. Locate the access key you want to delete
2. Click on the trash icon
3. On the dialog, click **DELETE** to confirm

## Using API

Go to the [Access Keys](https://run-ai-docs.nvidia.com/api/2.25/authentication-and-authorization/access-keys) API reference to view the available actions.


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://run-ai-docs.nvidia.com/self-hosted/settings/user-settings/user-access-keys.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
