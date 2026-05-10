# Set Up SSO with OpenShift

Single Sign-On (SSO) is an authentication scheme, allowing users to log-in with a single pair of credentials to multiple, independent software systems.

This guide explains the procedure to [configure SSO to NVIDIA Run:ai](/self-hosted/infrastructure-setup/authentication/overview.md#single-sign-on-sso) to NVIDIA Run:ai using the OpenID Connect protocol in OpenShift V4.

## Prerequisites

Before starting, make sure you have the following available from your OpenShift cluster:

* [OpenShift OAuth client](https://docs.openshift.com/container-platform/4.16/authentication/configuring-oauth-clients.html#oauth-register-additional-client_configuring-oauth-clients):
  * ClientID - The ID used to identify the client with the Authorization Server.
  * Client Secret - A secret password that only the Client and Authorization Server know.
* Base URL - The OpenShift API Server endpoint (for example, [https://api.\<cluster-url>:6443](https://api.noa-ocp.runailabs.com:6443/))

## Setup

### Adding the Identity Provider

1. Go to **General settings**
2. Open the Security section and click **+IDENTITY PROVIDER**
3. Select **OpenShift V4**
4. Enter the **Base URL**, Client ID, and **Client Secret** from your OpenShift OAuth client.
5. Copy the Redirect URL to be used in your OpenShift OAuth client
6. Optional: Enter the user attributes and their value in the identity provider as shown in the below table
7. Click **SAVE**
8. Optional: Enable **Auto-Redirect to SSO** to automatically redirect users to your configured identity provider’s login page when accessing the platform.

| Attribute            | Default value in NVIDIA Run:ai | Description                                                                                                                                                                                                  |
| -------------------- | ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| User role groups     | GROUPS                         | If it exists in the IDP, it allows you to assign NVIDIA Run:ai role groups via the IDP. The IDP attribute must be a list of strings.                                                                         |
| Linux User ID        | UID                            | If it exists in the IDP, it allows researcher containers to start with the Linux User UID. Used to map access to network resources such as file systems to users. The IDP attribute must be of type integer. |
| Linux Group ID       | GID                            | If it exists in the IDP, it allows researcher containers to start with the Linux Group GID. The IDP attribute must be of type integer.                                                                       |
| Supplementary Groups | SUPPLEMENTARYGROUPS            | If it exists in the IDP, it allows researcher containers to start with the relevant Linux supplementary groups. The IDP attribute must be a list of integers.                                                |
| Email                | email                          | Defines the user attribute in the IDP holding the user's email address, which is the user identifier in NVIDIA Run:ai                                                                                        |
| User first name      | firstName                      | Used as the user’s first name appearing in the NVIDIA Run:ai platform                                                                                                                                        |
| User last name       | lastName                       | Used as the user’s last name appearing in the NVIDIA Run:ai platform                                                                                                                                         |

### Testing the Setup

1. Open the NVIDIA Run:ai platform as an admin
2. Add [access rules](/self-hosted/infrastructure-setup/authentication/accessrules.md) to an SSO user defined in the IDP
3. Open the NVIDIA Run:ai platform in an incognito browser tab
4. On the sign-in page click **CONTINUE WITH SSO**\
   You are redirected to the OpenShift IDP sign-in page
5. In the identity provider sign-in page, log in with the SSO user who you granted with access rules
6. If you are unsuccessful signing-in to the identity provider, follow the [Troubleshooting](#troubleshooting) section below

### Editing the Identity Provider

You can view the identity provider details and edit its configuration:

1. Go to **General settings**
2. Open the Security section
3. On the identity provider box, click **Edit identity provider**
4. You can edit either the **Base URL**, **Client ID**, **Client Secret**, or the **User attributes**

### Removing the Identity Provider

You can remove the identity provider configuration:

1. Go to **General settings**
2. Open the Security section
3. On the identity provider card, click **Remove identity provider**
4. In the dialog, click **REMOVE** to confirm

{% hint style="info" %}
**Note**

To avoid losing access, removing the identity provider must be carried out by a local user.
{% endhint %}

## Troubleshooting

If testing the setup was unsuccessful, try the different troubleshooting scenarios according to the error you received.

### Troubleshooting Scenarios

<details>

<summary><strong>Error:</strong> "403 - Sorry, we can’t let you see this page. Something about permissions…"</summary>

**Description:** The authenticated user is missing permissions

**Mitigation**:

1. Validate either the user or its related group/s are assigned with [access rules](/self-hosted/infrastructure-setup/authentication/accessrules.md)
2. Validate groups attribute is available in the configured OIDC Scopes
3. Validate the user’s groups attribute is mapped correctly

**Advanced:**

1. Open the Chrome DevTools: Right-click on page → Inspect → Console tab
2. Run the following command to retrieve and copy the user’s token: `localStorage.token;`
3. Paste in [https://jwt.io](https://jwt.io/)
4. Under the Payload section validate the value of the user’s attributes

</details>

<details>

<summary><strong>Error:</strong> "401 - We’re having trouble identifying your account because your email is incorrect or can’t be found."</summary>

**Description:** Authentication failed because email attribute was not found.

**Mitigation**:

1. Validate email attribute is available in the configured OIDC Scopes
2. Validate the user’s email attribute is mapped correctly

</details>

<details>

<summary><strong>Error:</strong> "Unexpected error when authenticating with identity provider"</summary>

**Description:** User authentication failed

<div align="left"><figure><img src="/files/O8GRRjqJFlAG399LVRVl" alt="" width="375"><figcaption></figcaption></figure></div>

**Mitigation**: Validate the the configured OIDC Scopes exist and match the Identity Provider’s available scopes

**Advanced:** Look for the specific error message in the URL address

</details>

<details>

<summary><strong>Error:</strong> "Unexpected error when authenticating with identity provider (SSO sign-in is not available)"</summary>

**Description:** User authentication failed

<div align="left"><figure><img src="/files/cwTmhkvAZlTj4lUKQOLv" alt="" width="375"><figcaption></figcaption></figure></div>

**Mitigation**:

1. Validate the the configured OIDC scope exists in the Identity Provider
2. Validate the configured Client Secret match the Client Secret value in the OAuthclient Kubernetes object.

**Advanced:** Look for the specific error message in the URL address

</details>

<details>

<summary><strong>Error:</strong> "unauthorized_client"</summary>

**Description:** OIDC Client ID was not found in the OpenShift IDP

<img src="/files/UKyvWhOgLO6BpuUk7Uni" alt="" data-size="original">

**Mitigation**: Validate the the configured Client ID matches the value in the OAuthclient Kubernetes object

</details>


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://run-ai-docs.nvidia.com/self-hosted/infrastructure-setup/authentication/sso/openshift.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
