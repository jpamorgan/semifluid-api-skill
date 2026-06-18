# Semifluid API Reference

Source: `https://api.semifluid.ai/api-reference/spec.json`

Last refreshed from source: `2026-06-18`

OpenAPI: `3.1.1`

API version: `0.1.115`

Base URL: `https://api.semifluid.ai`

JSON spec: `https://api.semifluid.ai/api-reference/spec.json`

YAML spec: `https://api.semifluid.ai/api-reference/spec.yaml`

Auth: send the API key as `x-api-key: <key>`. The helper also supports `Authorization: Bearer <key>` with `--auth-header bearer`, but prefer `x-api-key`.

The helper reports each API request duration to stderr as `Timing: METHOD /path -> HTTP status in N.N ms`, while response bodies remain on stdout.

## Current Naming

Current API paths are rooted under `/v1`.

The current API uses `collections` and collection-scoped paths. Older docs, examples, or code may use `tables`, `tableId`, or `table-scoped`; prefer `collections`, `collectionId`, and the endpoint paths below.

Record endpoints now use `/records` in the URL and `recordId` in request/response bodies. Older docs or code may use `/rows`, `rowId`, row queries, or row activity; prefer `/records`, `recordId`, `record-queries`, and record events.

Forms are under `/forms` and public forms under `/public/forms`. Older docs may call these intake forms or use `/intake-forms`.

Public shares are managed through `/collections/{collectionId}/shares` and `/v1/shares/{shareId}`. Public read endpoints are under `/v1/public/shares/{publicShareToken}`.

## Common Commands

```bash
python3 scripts/semifluid_api.py health
python3 scripts/semifluid_api.py operations
python3 scripts/semifluid_api.py get /v1/collections
python3 scripts/semifluid_api.py get /v1/collections/{collectionId}
python3 scripts/semifluid_api.py get /v1/collections/{collectionId}/records --query limit=50 --query fields='*'
python3 scripts/semifluid_api.py post /v1/collections/{collectionId}/record-queries --json @query.json
python3 scripts/semifluid_api.py post /v1/collections/{collectionId}/record-mutations --json @mutation.json
python3 scripts/semifluid_api.py get /v1/collections/{collectionId}/records/{recordId}/events --query limit=20
python3 scripts/semifluid_api.py post /v1/collections/{collectionId}/attachments --json @attachment.json
python3 scripts/semifluid_api.py get /v1/collections/{collectionId}/forms
python3 scripts/semifluid_api.py get /v1/collections/{collectionId}/shares
python3 scripts/semifluid_api.py get /v1/events --query limit=10 --query direction=desc
python3 scripts/semifluid_api.py get /v1/webhooks
python3 scripts/semifluid_api.py post /v1/webhooks --json @webhook.json
```

Public form and share endpoints do not require API key auth:

```bash
python3 scripts/semifluid_api.py get /v1/public/forms/{intakeFormToken} --no-auth
python3 scripts/semifluid_api.py post /v1/public/forms/{intakeFormToken}/submissions --json @submission.json --no-auth
python3 scripts/semifluid_api.py get /v1/public/shares/{publicShareToken}/records --query limit=50 --query fields='*' --no-auth
```

## Operations

| Method | Path | Operation | Purpose |
| --- | --- | --- | --- |
| GET | `/v1/health` | `HealthCheck` | Health check |
| GET | `/v1/api-keys` | `ListApiKeys` | List workspace API keys |
| POST | `/v1/api-keys` | `CreateApiKey` | Create workspace API key |
| GET | `/v1/api-keys/{apiKeyId}` | `GetApiKey` | Get workspace API key |
| PATCH | `/v1/api-keys/{apiKeyId}` | `UpdateApiKey` | Update workspace API key |
| DELETE | `/v1/api-keys/{apiKeyId}` | `DeleteApiKey` | Delete workspace API key |
| POST | `/v1/api-keys/{apiKeyId}/secret-rotations` | `CreateApiKeySecretRotation` | Rotate workspace API key secret |
| POST | `/v1/collections/{collectionId}/attachments` | `UploadAttachment` | Upload attachment |
| POST | `/v1/collections` | `CreateCollection` | Create collection |
| GET | `/v1/collections` | `ListCollections` | List collections |
| GET | `/v1/collections/{collectionId}` | `GetCollectionDefinition` | Get collection |
| PATCH | `/v1/collections/{collectionId}` | `UpdateCollection` | Update collection |
| DELETE | `/v1/collections/{collectionId}` | `DeleteCollection` | Soft-delete collection |
| GET | `/v1/collections/{collectionId}/views` | `ListCollectionViews` | List collection views |
| POST | `/v1/collections/{collectionId}/views` | `CreateCollectionView` | Create collection view |
| PATCH | `/v1/collections/{collectionId}/views` | `UpdateCollectionViews` | Bulk update collection views |
| PATCH | `/v1/collections/{collectionId}/views/{viewId}` | `UpdateSavedCollectionView` | Update collection view |
| DELETE | `/v1/collections/{collectionId}/views/{viewId}` | `DeleteCollectionView` | Delete collection view |
| GET | `/v1/collections/{collectionId}/shares` | `ListCollectionShares` | List collection shares |
| POST | `/v1/collections/{collectionId}/shares` | `CreateCollectionShare` | Create collection share |
| GET | `/v1/shares/{shareId}` | `GetCollectionShare` | Get collection share |
| PATCH | `/v1/shares/{shareId}` | `UpdateCollectionShare` | Update collection share |
| DELETE | `/v1/shares/{shareId}` | `DeleteCollectionShare` | Delete collection share |
| GET | `/v1/events` | `ListEvents` | List events |
| POST | `/v1/collections/{collectionId}/fields` | `CreateCollectionField` | Create field |
| PATCH | `/v1/collections/{collectionId}/fields` | `UpdateCollectionFields` | Bulk update fields |
| PATCH | `/v1/collections/{collectionId}/fields/{fieldId}` | `UpdateCollectionField` | Update field |
| DELETE | `/v1/collections/{collectionId}/fields/{fieldId}` | `DeleteCollectionField` | Soft-delete field |
| GET | `/v1/collections/{collectionId}/forms` | `ListForms` | List forms |
| POST | `/v1/collections/{collectionId}/forms` | `CreateForm` | Create form |
| GET | `/v1/collections/{collectionId}/forms/{intakeFormId}` | `GetForm` | Get form |
| PATCH | `/v1/collections/{collectionId}/forms/{intakeFormId}` | `UpdateForm` | Update form |
| DELETE | `/v1/collections/{collectionId}/forms/{intakeFormId}` | `DeleteForm` | Delete form |
| GET | `/v1/public/forms/{intakeFormToken}` | `GetPublicForm` | Get public form |
| POST | `/v1/public/forms/{intakeFormToken}/submissions` | `SubmitForm` | Submit form response |
| GET | `/v1/public/shares/{publicShareToken}` | `GetPublicShareCollection` | Get public share collection |
| GET | `/v1/public/shares/{publicShareToken}/records` | `ListPublicShareRecords` | List public share records |
| POST | `/v1/public/shares/{publicShareToken}/record-queries` | `QueryPublicShareRecords` | Query public share records |
| GET | `/v1/public/shares/{publicShareToken}/records/{recordId}` | `GetPublicShareRecord` | Get public share record |
| POST | `/v1/collections/{collectionId}/records` | `CreateCollectionRecords` | Create records |
| GET | `/v1/collections/{collectionId}/records` | `ListCollectionRecords` | List records |
| POST | `/v1/collections/{collectionId}/record-queries` | `QueryCollectionRecords` | Query records |
| GET | `/v1/collections/{collectionId}/records/{recordId}` | `GetCollectionRecord` | Get record |
| PATCH | `/v1/collections/{collectionId}/records/{recordId}` | `UpdateCollectionRecord` | Update record |
| DELETE | `/v1/collections/{collectionId}/records/{recordId}` | `DeleteCollectionRecord` | Soft-delete record |
| GET | `/v1/collections/{collectionId}/records/{recordId}/events` | `ListCollectionRecordEvents` | List record events |
| POST | `/v1/collections/{collectionId}/record-imports` | `ImportCollectionRecordsCsv` | Import records from CSV |
| PUT | `/v1/collections/{collectionId}/records/external/{externalId}` | `UpsertCollectionRecordByExternalId` | Upsert record by external ID |
| POST | `/v1/collections/{collectionId}/record-mutations` | `MutateCollectionRecords` | Mutate records |
| POST | `/v1/collections/{collectionId}/suggestions` | `CreateCollectionSuggestion` | Suggest a record change |
| GET | `/v1/collections/{collectionId}/suggestions` | `ListCollectionSuggestions` | List suggestions |
| GET | `/v1/collections/{collectionId}/suggestions/{suggestionId}` | `GetCollectionSuggestion` | Get suggestion |
| PATCH | `/v1/collections/{collectionId}/suggestions/{suggestionId}` | `ReviewCollectionSuggestion` | Review suggestion |
| GET | `/v1/webhooks` | `ListWebhooks` | List workspace webhooks |
| POST | `/v1/webhooks` | `CreateWebhook` | Create webhook |
| PATCH | `/v1/webhooks/{webhookId}` | `UpdateWebhook` | Update webhook |
| DELETE | `/v1/webhooks/{webhookId}` | `DeleteWebhook` | Delete webhook |
| GET | `/v1/webhooks/{webhookId}/deliveries` | `ListWebhookDeliveries` | List webhook deliveries |
| POST | `/v1/webhooks/{webhookId}/deliveries` | `CreateWebhookDelivery` | Create webhook delivery |

## Parameters

- `collectionId`, `recordId`, `fieldId`, `viewId`, `shareId`, `intakeFormId`, `suggestionId`, and `webhookId` path parameters are UUID strings.
- `apiKeyId` is a non-empty string.
- `publicShareToken` is a 43-character URL-safe token matching `^[A-Za-z0-9_-]{43}$`; `intakeFormToken` is a public token string from 32 to 256 characters.
- List endpoints generally default `limit` to `50` and cap `limit` at `100`; webhook deliveries default to `20` and cap at `50`.
- Record read endpoints support `fields: "*"` or an array of up to 100 field keys. For GET query strings, pass `--query fields='*'`; for POST/PATCH requests, include `fields` in the JSON body.
- Field keys in record values must match `^[A-Za-z_][A-Za-z0-9_]*$`.
- `POST /v1/collections/{collectionId}/attachments` accepts `name`, optional `mimeType`, and `dataBase64` up to 34,952,536 characters.
- `GET /v1/events` supports `limit`, `cursor`, `includePayload`, `direction=asc|desc`, `collectionId`, `operation`, `entityType`, and `entityId`; `direction` defaults to `asc`.
- `GET /v1/webhooks` accepts optional `collectionId`; `GET /v1/webhooks/{webhookId}/deliveries` accepts optional `limit`.

## API Keys

API key names must be 1 to 64 characters. If `access` is omitted when creating a key, the API creates a workspace-wide key.

Create a workspace-wide key:

```json
{
  "name": "Agent key",
  "access": {
    "kind": "workspace"
  }
}
```

Create a collection-scoped key:

```json
{
  "name": "Readonly collection key",
  "access": {
    "kind": "collection_scoped",
    "grants": [
      {
        "collectionId": "00000000-0000-0000-0000-000000000000",
        "scope": "read_only"
      }
    ]
  }
}
```

Collection-scoped grant scopes: `read_only`, `row_suggester`, `suggestion_reviewer`, `row_editor`, `locked_row_editor`, `collection_admin`.

Collection-scoped grants may include `capabilities`, currently `public_share_manage` and `intake_form_manage`.

Update an API key with `PATCH /v1/api-keys/{apiKeyId}`. The request may include `name`, `access`, optional `preset`, and optional `reason`:

```json
{
  "access": {
    "kind": "collection_scoped",
    "grants": [
      {
        "collectionId": "00000000-0000-0000-0000-000000000000",
        "scope": "collection_admin",
        "capabilities": ["public_share_manage", "intake_form_manage"]
      }
    ]
  },
  "preset": "collection-admin",
  "reason": "Grant admin access for automation"
}
```

Rotate an API key secret with `POST /v1/api-keys/{apiKeyId}/secret-rotations`.

## Collections And Fields

Create a collection:

```json
{
  "name": "Tasks",
  "icon": {
    "type": "emoji",
    "emoji": "T"
  },
  "description": "Task tracker",
  "isLocked": false,
  "fields": [
    {
      "name": "Status",
      "key": "status",
      "type": "select",
      "options": [
        {
          "label": "Open",
          "value": "open",
          "color": "green"
        }
      ]
    }
  ]
}
```

Collection names are required. Collection descriptions, icons, `isLocked`, and initial `fields` are optional. Initial field lists are capped at 100 fields.

Update a collection:

```json
{
  "name": "Tasks",
  "description": "Tracked tasks",
  "isLocked": false,
  "metadata": {
    "collectionView": {
      "filterMode": "all"
    }
  }
}
```

`PATCH /v1/collections/{collectionId}` accepts any subset of `name`, `icon`, `description`, `isLocked`, and `metadata`.

Create a field:

```json
{
  "name": "Status",
  "key": "status",
  "type": "status",
  "description": "Current workflow state",
  "isRequired": false,
  "isHidden": false,
  "isPrimary": false,
  "position": 0,
  "options": [
    {
      "label": "Open",
      "value": "open",
      "color": "green"
    }
  ]
}
```

Field create requires `name`, `key`, and `type`; it also accepts optional `description`, `config`, `isRequired`, `isHidden`, `isPrimary`, `position`, and `options`. Field update accepts `name`, `description`, `config`, `isRequired`, `isHidden`, `isPrimary`, and `options`. Select/status options use `label`, `value`, optional `color`, and optional `id` when updating. Field option arrays are capped at 100 options, and option values are capped at 128 characters.

Field types from the spec: `text`, `markdown`, `select`, `status`, `multi_select`, `attachment`, `phone`, `number`, `currency`, `auto_number`, `boolean`, `date`, `date_time`, `email`, `url`, `relation`, `lookup`, `rollup`.

Bulk reorder fields:

```json
{
  "fieldIds": ["00000000-0000-0000-0000-000000000000"]
}
```

Use `PATCH /v1/collections/{collectionId}/fields`. The request requires at least one field ID.

## Records

Create records with `POST /v1/collections/{collectionId}/records`. Batch create requests require 1 to 1000 records. External IDs must be 1 to 191 characters.

```json
{
  "records": [
    {
      "externalId": "external-id",
      "values": {
        "field_key": "value"
      }
    }
  ],
  "fields": "*",
  "returning": "records",
  "mutationMode": "partial"
}
```

Update one record with `PATCH /v1/collections/{collectionId}/records/{recordId}`:

```json
{
  "values": {
    "field_key": "new value"
  },
  "fields": "*"
}
```

Delete one record with `DELETE /v1/collections/{collectionId}/records/{recordId}`.

Upsert one record by external ID with `PUT /v1/collections/{collectionId}/records/external/{externalId}`:

```json
{
  "values": {
    "field_key": "value"
  }
}
```

For batch create, update, upsert, delete, lock, and unlock, use `POST /v1/collections/{collectionId}/record-mutations`:

```json
{
  "operation": "update",
  "records": [
    {
      "recordId": "00000000-0000-0000-0000-000000000000",
      "values": {
        "field_key": "new value"
      }
    }
  ],
  "fields": "*",
  "returning": "records",
  "mutationMode": "partial"
}
```

`operation` is `create`, `update`, `upsert`, `delete`, `lock`, or `unlock`. Batch write modes: `partial` attempts each record independently and returns per-item results. `all_or_nothing` applies the whole batch transactionally.

Create and batch mutation calls default to `returning: "ids"` and `fields: []`. Use `returning: "records"` plus `fields: "*"` or a field-key array when the response should include record values.

Upload an attachment before storing it in an attachment field:

```json
{
  "name": "file.pdf",
  "mimeType": "application/pdf",
  "dataBase64": "<base64 file contents>"
}
```

Attachment field values use arrays of attachment metadata returned by `POST /v1/collections/{collectionId}/attachments`:

```json
{
  "attachment_field": [
    {
      "id": "00000000-0000-0000-0000-000000000000",
      "name": "file.pdf",
      "mimeType": "application/pdf",
      "size": 12345,
      "url": "https://api.semifluid.ai/...",
      "createdAt": "2026-06-18T00:00:00.000Z"
    }
  ]
}
```

Import CSV rows with `POST /v1/collections/{collectionId}/record-imports`:

```json
{
  "csv": "name,status\nFirst task,Open\n",
  "headerRow": true,
  "columns": ["name", "status"],
  "validateOnly": false
}
```

CSV imports are atomic: if any cell fails validation, no records are created. Requests accept at most 1000 data rows and raw CSV text up to 5,242,880 characters. If `columns` is omitted, `headerRow` must be true and headers are auto-mapped to fields by key or name case-insensitively. Use `null` in `columns` to skip a CSV column.

## Record Events

Read record-level events with `GET /v1/collections/{collectionId}/records/{recordId}/events`. It returns paginated events for that record.

```bash
python3 scripts/semifluid_api.py get /v1/collections/{collectionId}/records/{recordId}/events --query limit=20
```

Query parameters:

- `limit`: 1 to 100, default 50.
- `cursor`: pass the previous response `pageInfo.nextCursor` for the next page.

## Query Records

Use `POST /v1/collections/{collectionId}/record-queries`. The `mode` property is required.

Query matching records:

```json
{
  "mode": "query",
  "limit": 50,
  "cursor": "next-cursor",
  "search": "search text",
  "fields": "*",
  "filters": [
    {
      "field": "status",
      "operator": "eq",
      "value": "Open"
    }
  ],
  "filterMode": "all",
  "sort": [
    {
      "field": "createdAt",
      "direction": "desc"
    }
  ]
}
```

Aggregate matching records:

```json
{
  "mode": "aggregate",
  "search": "search text",
  "filters": [
    {
      "field": "status",
      "operator": "eq",
      "value": "Open"
    }
  ],
  "filterMode": "all",
  "metrics": [
    {
      "key": "count",
      "operation": "count"
    },
    {
      "key": "total",
      "operation": "sum",
      "field": "amount"
    }
  ],
  "groupBy": {
    "field": "createdAt",
    "dateBucket": "month"
  },
  "sort": {
    "metric": "total",
    "direction": "desc"
  },
  "limit": 100
}
```

Find missing values:

```json
{
  "mode": "missing_values",
  "fields": ["summary", "owner"],
  "contextFields": ["name"],
  "matchMode": "any",
  "limit": 50
}
```

Look up records by ID:

```json
{
  "mode": "lookup",
  "recordIds": ["00000000-0000-0000-0000-000000000000"],
  "fields": "*"
}
```

Filter operators: `eq`, `neq`, `is_empty`, `is_not_empty`, `gt`, `gte`, `lt`, `lte`, `contains`, `starts_with`, `in`, `not_in`, `between`.

Query limits: `limit` is 1-100, `search` is at most 256 characters, filters are capped at 25, sort entries are capped at 10, and explicit `fields` arrays are capped at 100 field keys.

`search` performs case-insensitive broad record search over searchable text-like values, including text, markdown, email, phone, URL, select/status labels, multi-select labels, and attachment file names.

Aggregate metric operations: `count`, `count_values`, `count_empty`, `count_unique`, `count_true`, `count_false`, `count_items`, `count_unique_items`, `sum`, `avg`, `min`, `max`.

Aggregate requests default to one metric: `{ "key": "count", "operation": "count" }`. Requests accept 1 to 10 metrics. Metric keys must be 1 to 128 characters and match `^[A-Za-z0-9][A-Za-z0-9_.:-]*$`. `limit` applies to grouped aggregate results only; ungrouped aggregate queries always return one row.

`countLimit` can cap count-like ungrouped metrics from 1 to 1,000,000. Responses return `countLimit + 1` when more records or values exist.

Date buckets: `day`, `week`, `month`, `year`. Week buckets start on Monday and date buckets use UTC.

Public share record queries use `POST /v1/public/shares/{publicShareToken}/record-queries` with the query-mode body shape, but without the `mode` property.

## Suggestions

Suggestions let a caller propose record creates, updates, or deletes for later review. Use `POST /v1/collections/{collectionId}/suggestions`.

Suggest a new record:

```json
{
  "kind": "create",
  "values": {
    "name": "New task",
    "status": "Open"
  },
  "note": "Suggested by import review"
}
```

Suggest an update:

```json
{
  "kind": "update",
  "rowId": "00000000-0000-0000-0000-000000000000",
  "values": {
    "status": "Done"
  },
  "note": "Status should match source system"
}
```

Suggest a delete:

```json
{
  "kind": "delete",
  "rowId": "00000000-0000-0000-0000-000000000000",
  "note": "Duplicate record"
}
```

The suggestion body still uses `rowId` for update/delete targets in the current spec. List suggestions with `GET /v1/collections/{collectionId}/suggestions`. Optional query parameters: `limit`, `cursor`, and `status=pending|approved|rejected`.

Review a suggestion with `PATCH /v1/collections/{collectionId}/suggestions/{suggestionId}`:

```json
{
  "status": "approved",
  "note": "Reviewed and accepted"
}
```

`status` is required and must be `approved` or `rejected`.

## Forms

Manage forms with collection-authenticated endpoints:

- `GET /v1/collections/{collectionId}/forms`
- `POST /v1/collections/{collectionId}/forms`
- `GET /v1/collections/{collectionId}/forms/{intakeFormId}`
- `PATCH /v1/collections/{collectionId}/forms/{intakeFormId}`
- `DELETE /v1/collections/{collectionId}/forms/{intakeFormId}`

Create a form:

```json
{
  "title": "Task intake",
  "description": "Submit a task request",
  "successMessage": "Thanks",
  "isEnabled": true,
  "fields": [
    {
      "fieldId": "00000000-0000-0000-0000-000000000000",
      "required": true,
      "label": "Task name",
      "helpText": "Use a short descriptive title"
    }
  ]
}
```

Create requires `title` and at least one field. Title is capped at 120 characters, description at 2000, success message at 1000, and form field lists at 50 fields. Field labels are capped at 120 characters and help text at 500.

Public form endpoints use a token and do not require API key auth:

```bash
python3 scripts/semifluid_api.py get /v1/public/forms/{intakeFormToken} --no-auth
python3 scripts/semifluid_api.py post /v1/public/forms/{intakeFormToken}/submissions --json @submission.json --no-auth
```

Submit a form:

```json
{
  "values": {
    "name": "New request",
    "status": "Open"
  }
}
```

Submission values are keyed by public field keys. Attachment fields use attachment metadata arrays. Public submissions are rate limited to 10 responses per client per form every 10 minutes and 300 responses per form every hour.

## Collection Views

Saved views are managed through `/v1/collections/{collectionId}/views`.

Create a saved view:

```json
{
  "name": "Open tasks",
  "type": "table",
  "config": {}
}
```

Saved view create defaults to `name: "Table"` and `type: "table"` when omitted. Saved view names must be 1 to 120 characters. View types: `table`, `grid`, `board`, `map`, `calendar`, `list`, `form`, `dashboard`.

Bulk reorder saved views:

```json
{
  "viewIds": ["00000000-0000-0000-0000-000000000000"]
}
```

Saved view reorder accepts 1 to 25 view IDs.

Update a saved view:

```json
{
  "name": "Open tasks",
  "config": {},
  "collectionView": {
    "filters": [
      {
        "field": "status",
        "operator": "eq",
        "value": "Open"
      }
    ],
    "filterMode": "all",
    "sort": [
      {
        "field": "createdAt",
        "direction": "desc"
      }
    ],
    "fieldOrder": ["00000000-0000-0000-0000-000000000000"],
    "hiddenFieldIds": [],
    "fieldSizing": {
      "00000000-0000-0000-0000-000000000000": 240
    },
    "fieldCalculations": {
      "00000000-0000-0000-0000-000000000000": "count_values"
    },
    "stickyFieldId": "00000000-0000-0000-0000-000000000000"
  }
}
```

In saved view updates, collection-view preference properties can be set to `null` to clear them.

Field calculations: `count_all`, `count_values`, `count_unique`, `count_empty`, `count_not_empty`, `count_true`, `count_false`, `percent_true`, `percent_false`, `count_items`, `count_unique_items`, `percent_empty`, `percent_not_empty`, `sum`, `average`, `min`, `max`, `earliest`, `latest`.

Collection-view filters are capped at 25, sort entries at 10, field order and hidden field IDs at 100, and field widths at 96 to 1600 pixels.

## Public Shares

Share management endpoints use collection auth:

- `GET /v1/collections/{collectionId}/shares`
- `POST /v1/collections/{collectionId}/shares`
- `GET /v1/shares/{shareId}`
- `PATCH /v1/shares/{shareId}`
- `DELETE /v1/shares/{shareId}`

Create or update a public share:

```json
{
  "publicShareToken": "optional-43-character-url-safe-token"
}
```

Public share read endpoints use a `publicShareToken` and do not require the workspace API key when the share is enabled:

- `GET /v1/public/shares/{publicShareToken}`
- `GET /v1/public/shares/{publicShareToken}/records`
- `GET /v1/public/shares/{publicShareToken}/records/{recordId}`
- `POST /v1/public/shares/{publicShareToken}/record-queries`

When using the helper for public read endpoints, pass `--no-auth` unless the user explicitly wants to send an API key.

## Webhooks

Webhook endpoints use workspace API key auth. Treat webhook secrets and delivery payloads as sensitive; do not include them in final answers, logs, or files unless the user explicitly asks and the destination is appropriate. `POST /v1/webhooks` returns the webhook `secret` only in the create response.

List all webhooks, or filter by collection:

```bash
python3 scripts/semifluid_api.py get /v1/webhooks
python3 scripts/semifluid_api.py get /v1/webhooks --query collectionId=00000000-0000-0000-0000-000000000000
```

Create a webhook:

```json
{
  "name": "Sync listener",
  "url": "https://example.com/semifluid/webhook",
  "collectionId": "00000000-0000-0000-0000-000000000000",
  "events": ["row.created", "row.updated"]
}
```

Create requires `name` and `url`. `name` is 1 to 64 characters, `url` is 1 to 2048 characters, `collectionId` is optional, and `events` is optional but must contain 1 to 9 event types when supplied.

Webhook event types:

- `row.created`, `row.updated`, `row.deleted`
- `field.created`, `field.updated`, `field.deleted`
- `collection.created`, `collection.updated`, `collection.deleted`

Update a webhook:

```json
{
  "name": "Sync listener",
  "url": "https://example.com/semifluid/webhook",
  "collectionId": null,
  "events": ["row.created"],
  "isActive": true
}
```

Update accepts any subset of `name`, `url`, `collectionId`, `events`, and `isActive`. Set `collectionId` to `null` to make the webhook workspace-wide.

Delete a webhook with `DELETE /v1/webhooks/{webhookId}`.

Create a test delivery:

```json
{
  "kind": "test"
}
```

Use `POST /v1/webhooks/{webhookId}/deliveries`.

List recent deliveries:

```bash
python3 scripts/semifluid_api.py get /v1/webhooks/{webhookId}/deliveries --query limit=20
```

Webhook delivery results include `eventType`, `status` (`success` or `failed`), `attempts`, `responseStatus`, `errorMessage`, `durationMs`, `payload`, and `createdAt`.

## Events

List workspace events with `GET /v1/events`:

```bash
python3 scripts/semifluid_api.py get /v1/events --query limit=50 --query direction=desc
```

Useful query parameters:

- `limit`: 1 to 100, default 50.
- `cursor`: pagination cursor.
- `includePayload`: include event payloads; defaults to false.
- `direction`: `asc` or `desc`; defaults to `asc`.
- `collectionId`, `operation`, `entityType`, `entityId`: optional filters.

For exact schemas, run:

```bash
python3 scripts/semifluid_api.py spec --output /tmp/semifluid-spec.json
```
