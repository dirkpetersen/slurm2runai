# Access Rules

Access rules provide users, groups, or service accounts privileges to system entities. An access rule is the assignment of a [role ](/self-hosted/infrastructure-setup/authentication/roles.md)to a [subject in a scope](/self-hosted/platform-management/aiinitiatives/adapting-ai-initiatives.md#scopes-in-an-organization): `<Subject>` is a `<Role>` in a `<Scope>`. For example, user **<user@domain.com>** is a **department admin** in **department A**.

## Access Rules Table

The Access rules table can be found under **Access** in the NVIDIA Run:ai platform.

The Access rules table provides a list of all the access rules defined in the platform and allows you to manage them.

{% hint style="info" %}
**Flexible management**

It is also possible to manage access rules directly for a specific [user](/self-hosted/infrastructure-setup/authentication/users.md), [service account](/self-hosted/infrastructure-setup/authentication/service-accounts.md), [project](/self-hosted/platform-management/aiinitiatives/organization/projects.md), or [department](/self-hosted/platform-management/aiinitiatives/organization/departments.md).
{% endhint %}

<figure><img src="/files/BRXJY97LPhnQVX0l27yQ" alt=""><figcaption></figcaption></figure>

The Access rules table consists of the following columns:

| Column        | Description                                                                                                  |
| ------------- | ------------------------------------------------------------------------------------------------------------ |
| Type          | The type of subject assigned to the access rule (user, SSO group, or service account).                       |
| Subject       | The user, SSO group, or service account assigned with the role                                               |
| Role          | The role assigned to the subject                                                                             |
| Scope         | The scope to which the subject has access. Click the name of the scope to see the scope and its subordinates |
| Status        | The access rule creation status.                                                                             |
| Authorized by | The user who granted the access rule                                                                         |
| Creation time | The timestamp for when the rule was created                                                                  |
| Last updated  | The last time the access rule was updated                                                                    |

### Access Rule Status

The following table describes the condition of access rules and whether they were successfully created for the selected scope. The status indicates whether the access rule is synced in the cluster.

| Status          | Description                                                                                                                                                        |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| No issues found | No issues were found while creating the access rule                                                                                                                |
| Issues found    | Issues were found while enforcing the access rule in the cluster(s). [Contact NVIDIA Run:ai support](https://www.nvidia.com/en-eu/support/enterprise/#contact-us). |
| Creating…       | The access rule is being created in the cluster                                                                                                                    |
| No status       | Status cannot be displayed because the current version of the cluster is not up to date or unknown                                                                 |

### Customizing the Table View

* Filter - Click ADD FILTER, select the column to filter by, and enter the filter values
* Search - Click SEARCH and type the value to search by
* Sort - Click each column header to sort by
* Column selection - Click COLUMNS and select the columns to display in the table
* Download table - Click MORE and then Click Download as CSV. Export to CSV is limited to 20,000 rows.

## Adding New Access Rules

To add a new access rule:

1. Click **+NEW ACCESS RULE**
2. Select a subject - **User, SSO Group**, or **Service Account**
3. Select or enter the subject identifier. You can define up to 10 subjects of the selected type:
   * **User Email** for a local user created in NVIDIA Run:ai or for SSO user as recognized by the IDP
   * **Group name** as recognized by the IDP
   * **Service account name** as created in NVIDIA Run:ai
4. Select a **role**
5. Select up to 10 **scopes** where the access rule will apply
6. Click **SAVE RULE**

## Editing an Access Rule

Access rules cannot be edited. To change an access rule, you must delete the rule, and then create a new rule to replace it.

## Deleting an Access Rule

1. Select one or more access rules you want to delete
2. Click **DELETE**
3. On the dialog, click **DELETE** to confirm

## Viewing Your User Access Rule

To view the assigned roles and scopes you have access to:

1. Click the user avatar at the top right corner, then select **Settings**
2. Click **User details**

The list of assigned roles and scopes will be displayed.

## Using API

Go to the [Access rules](https://run-ai-docs.nvidia.com/api/2.25/authentication-and-authorization/access-rules) API reference to view the available actions.


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://run-ai-docs.nvidia.com/self-hosted/infrastructure-setup/authentication/accessrules.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
