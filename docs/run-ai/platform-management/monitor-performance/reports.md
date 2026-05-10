# Reports

This section explains the procedure of managing reports in NVIDIA Run:ai.

Reports allow users to access and organize large amounts of data in a clear, CSV-formatted layout. They enable users to monitor resource consumption, analyze trends, and make data-driven decisions to optimize their AI workloads effectively.

## Report Types

Currently, only consumption reports are available, which provides insights into the consumption of resources such as GPU, CPU, and CPU memory across organizational units.

## Reports Table

The Reports table can be found under **Analytics** in the NVIDIA Run:ai platform.

The Reports table provides a list of all the reports defined in the platform and allows you to manage them.

<figure><img src="/files/HIVfUWsOhIC3XJfV2O4x" alt=""><figcaption></figcaption></figure>

Users are able to access the reports they have generated themselves. Users with project viewing permissions throughout the tenant can access all reports within the tenant.

The Reports table comprises the following columns:

| Column            | Description                                                               |
| ----------------- | ------------------------------------------------------------------------- |
| Report            | The name of the report                                                    |
| Description       | The description of the report                                             |
| Status            | The different lifecycle phases and representation of the report condition |
| Type              | The type of the report – e.g., consumption                                |
| Created by        | The user who created the report                                           |
| Creation time     | The timestamp of when the report was created                              |
| Collection period | The period in which the data was collected                                |

### Reports Status

The following table describes the reports' condition and whether they were created successfully:

| Status        | Description                                        |
| ------------- | -------------------------------------------------- |
| Ready         | Report is ready and can be downloaded as CSV       |
| Pending       | Report is in the queue and waiting to be processed |
| Failed        | The report couldn’t be created                     |
| Processing... | The report is being created                        |

### Customizing the Table View

* Filter - Click ADD FILTER, select the column to filter by, and enter the filter values
* Search - Click SEARCH and type the value to search by
* Sort - Click each column header to sort by
* Column selection - Click COLUMNS and select the columns to display in the table

## Creating a New Report

Before you start, make sure you have a project.

To create a new report:

1. Click **+NEW REPORT**
2. Enter a **name** for the report (if the name already exists, you will need to choose a different one)
3. Optional: Provide a description of the report
4. Set the report’s data collection period
   * Start date - The date at which the report data commenced
   * End date - The date at which the report data concluded
5. Set the report segmentation and filters
   * Filters - Filter by project or department name
   * Segment by - Data is collected and aggregated based on the segment
6. Click **CREATE REPORT**

## Deleting a Report

1. Select the report you want to delete
2. Click **DELETE**
3. On the dialog, click **DELETE** to confirm

## Downloading a Report

{% hint style="info" %}
**Note**

To download, the report must be in status “Ready”.
{% endhint %}

1. Select the report you want to download
2. Click **DOWNLOAD CSV**

## Enabling Reports for Self-Hosted Accounts

Reports must be saved in a storage solution compatible with S3. To activate this feature for self-hosted accounts, the storage needs to be linked to the account. The configuration should be incorporated into ConfigMap and Secret objects within the Control Plane.

1. Edit the `runai-backend-org-unit-service` ConfigMap and add the following lines:

   ```bash
   kubectl edit cm runai-backend-org-unit-service -n runai-backend
   ```

   ```bash
   S3_ENDPOINT: <S3_END_POINT_URL>
   S3_ACCESS_KEY_ID: <S3_ACCESS_KEY_ID>
   S3_USE_SSL: "true"
   S3_BUCKET: <BUCKET_NAME>
   ```
2. Edit the `runai-backend-org-unit-service` Secret and add the following to the `data` section (value must be base64-encoded):

   ```bash
   kubectl edit secret runai-backend-org-unit-service -n runai-backend
   ```

   ```bash
   S3.ACCESS_KEY: <base64-encoded S3_ACCESS_KEY>
   ```
3. Edit the `runai-backend-metrics-service` ConfigMap and add the following lines:

   ```bash
   kubectl edit cm runai-backend-metrics-service -n runai-backend
   ```

   ```bash
   S3_ENDPOINT: <S3_END_POINT_URL>
   S3_ACCESS_KEY_ID: <S3_ACCESS_KEY_ID>
   S3_USE_SSL: "true"
   ```
4. In the same ConfigMap, under the `config.yaml` section, add the following right after `log_level: "Info"`:

   ```yaml
   reports:
     s3_config:
       bucket: "<BUCKET_NAME>"
   ```
5. Edit the `runai-backend-metrics-service` Secret and add the following to the `data` section (value must be base64-encoded):

   ```bash
   kubectl edit secret runai-backend-metrics-service -n runai-backend
   ```

   ```bash
   S3.ACCESS_KEY: <base64-encoded S3_ACCESS_KEY>
   ```
6. Restart the deployments:

   ```bash
   kubectl rollout restart deployment runai-backend-metrics-service runai-backend-org-unit-service -n runai-backend
   ```
7. Refresh the page to see **Reports** under Analytics in the NVIDIA Run:ai platform.

## Using API

To view the available actions, go to the [Reports](https://run-ai-docs.nvidia.com/api/2.25/organizations/reports) API reference.


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://run-ai-docs.nvidia.com/self-hosted/platform-management/monitor-performance/reports.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
