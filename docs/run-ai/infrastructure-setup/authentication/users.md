# Users

Users can be managed locally, or via the identity provider (Idp), while assigned with [access rules](/self-hosted/infrastructure-setup/authentication/accessrules.md) to manage permissions. For example, user **<user@domain.com>** is a **department admin** in **department A**.

## Users Table

The Users table can be found under **Access** in the NVIDIA Run:ai platform.

The users table provides a list of all the users in the platform.\
You can manage users and user permissions (access rules) for both local and [SSO users](/self-hosted/infrastructure-setup/authentication/overview.md#single-sign-on-sso).

{% hint style="info" %}
**Single Sign-On Users**

SSO users are managed by the identity provider and appear once they have signed in to NVIDIA Run:ai.
{% endhint %}

<figure><img src="/files/VxCM6b7PFIRq5zgZDUJa" alt=""><figcaption></figcaption></figure>

The Users table consists of the following columns:

| Column         | Description                                        |
| -------------- | -------------------------------------------------- |
| User           | The unique identity of the user (email address)    |
| Type           | The type of the user - SSO / local                 |
| Last login     | The timestamp for the last time the user signed in |
| Access rule(s) | The access rule assigned to the user               |
| Created By     | The user who created the user                      |
| Creation time  | The timestamp for when the user was created        |
| Last updated   | The last time the user was updated                 |

### Customizing the Table View

* Filter - Click ADD FILTER, select the column to filter by, and enter the filter values
* Search - Click SEARCH and type the value to search by
* Sort - Click each column header to sort by
* Column selection - Click COLUMNS and select the columns to display in the table
* Download table - Click MORE and then Click Download as CSV. Export to CSV is limited to 20,000 rows.

## Creating a Local User

To create a local user:

1. Click **+NEW LOCAL USER**
2. Enter the user’s **Email address**
3. (Optional) Select the checkbox to send an email invitation to the new user. The invitation allows the user to sign in and get started. To enable email invitations, make sure email notifications are configured under [**General settings**](/self-hosted/settings/general-settings/notifications.md).
4. Click **CREATE**
5. Review and copy the user’s credentials:
   * **User Email**
   * **Temporary password** to be used on first sign-in
6. Click **DONE** or click **ADD ACCESS RULES** to proceed to the **Access rules** step
7. In the **Access rules** step:
   * Select a **role**
   * Select up to 10 **scopes** where the access rule will apply
   * Click **SAVE RULE**
   * Click **CLOSE**

{% hint style="info" %}
**Note**

The temporary password is visible only at the time of user’s creation and must be changed after the first sign-in.
{% endhint %}

## Adding an Access Rule to a User

To create an access rule:

1. Select the user you want to add an access rule for
2. Click **ACCESS RULES**
3. Click **+ACCESS RULE**
4. Select a **role**
5. Select up to 10 **scopes** where the access rule will apply
6. Click **SAVE RULE**
7. Click **CLOSE**

## Deleting User’s Access Rule

To delete an access rule:

1. Select the user you want to remove an access rule from
2. Click **ACCESS RULES**
3. Find the access rule assigned to the user you would like to delete
4. Click on the trash icon
5. Click **CLOSE**

## Resetting a User Password

To reset a user’s password:

1. Select the user you want to reset it’s password
2. Click **RESET PASSWORD**
3. Click **RESET**
4. Review and copy the user’s credentials:
   * **User Email**
   * **Temporary password** to be used on next sign-in
5. Click **DONE**

## Deleting a User

1. Select the user you want to delete
2. Click **DELETE**
3. In the dialog, click **DELETE** to confirm

{% hint style="info" %}
**Note**

To ensure administrative operations are always available, at least one local user with System Administrator role should exist.
{% endhint %}

## Using API

Go to the [Users](https://run-ai-docs.nvidia.com/api/2.25/authentication-and-authorization/users), [Access rules](https://run-ai-docs.nvidia.com/api/2.25/authentication-and-authorization/access-rules) API reference to view the available actions.


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://run-ai-docs.nvidia.com/self-hosted/infrastructure-setup/authentication/users.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
