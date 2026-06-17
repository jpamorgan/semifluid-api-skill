# Semifluid API Reference

Source: `https://api.semifluid.ai/api-reference/spec.json`

Last refreshed from source: `2026-06-17`

OpenAPI: `3.1.1`

API version: `0.1.114`

Base URL: `https://api.semifluid.ai`

JSON spec: `https://api.semifluid.ai/api-reference/spec.json`

YAML spec: `https://api.semifluid.ai/api-reference/spec.yaml`

Auth: send the API key as `x-api-key: <key>`. The helper also supports `Authorization: Bearer <key>` with `--auth-header bearer`, but prefer `x-api-key`.

The helper reports each API request duration to stderr as `Timing: METHOD /path -> HTTP status in N.N ms`, while response bodies remain on stdout.

## Current Naming

The current API uses `collections` and collection-scoped paths. Older docs, examples, or code may use `tables`, `tableId`, or `table-scoped`; prefer `collections`, `collectionId`, and the endpoint paths below.

Record endpoints still use `/rows` in the URL and `rowId` in request/response bodies. Use "records" for user-facing language, but keep `rows`/`rowId` when calling the API.

## Common Commands

```bash
python3 scripts/semifluid_api.py health
python3 scripts/semifluid_api.py operations
python3 scripts/semifluid_api.py get /collections
python3 scripts/semifluid_api.py get /collections/{collectionId}
python3 scripts/semifluid_api.py get /collections/{collectionId}/rows --query limit=50 --query fields='*'
python3 scripts/semifluid_api.py post /collections/{collectionId}/row-queries --json @query.json
python3 scripts/semifluid_api.py post /collections/{collectionId}/row-aggregations --json @aggregate.json
python3 scripts/semifluid_api.py patch /collections/{collectionId}/rows --json @rows-update.json
python3 scripts/semifluid_api.py get /collections/{collectionId}/rows/{rowId}/activity --query limit=20
python3 scripts/semifluid_api.py post /collections/{collectionId}/attachments --json @attachment.json
python3 scripts/semifluid_api.py put /collections/{collectionId}/file --json @file.json
python3 scripts/semifluid_api.py get /collections/{collectionId}/files --query limit=50
python3 scripts/semifluid_api.py get /collections/{collectionId}/intake-forms
python3 scripts/semifluid_api.py post /collections/{collectionId}/csv-imports --json @csv-import.json
python3 scripts/semifluid_api.py post /changes/list --json '{"limit":10,"direction":"desc"}'
python3 scripts/semifluid_api.py get /webhooks
python3 scripts/semifluid_api.py post /webhooks --json @webhook.json
```

## Operations

| Method | Path | Operation | Purpose |
| --- | --- | --- | --- |
| GET | `/health` | `HealthCheck` | Health check |
| GET | `/api-keys` | `ListApiKeys` | List workspace API keys |
| POST | `/api-keys` | `CreateApiKey` | Create workspace API key |
| DELETE | `/api-keys/{apiKeyId}` | `DeleteApiKey` | Delete workspace API key |
| PATCH | `/api-keys/{apiKeyId}` | `RenameApiKey` | Rename workspace API key |
| PATCH | `/api-keys/{apiKeyId}/access` | `UpdateApiKeyAccess` | Update workspace API key access |
| POST | `/api-keys/{apiKeyId}/rotations` | `RollApiKey` | Roll workspace API key |
| GET | `/agent-workspaces/{agentWorkspaceId}/files` | `ListLegacyAgentWorkspaceFiles` | List agent workspace files |
| GET | `/agent-workspaces/{agentWorkspaceId}/files/{fileId}` | `GetLegacyAgentWorkspaceFile` | Get agent workspace file |
| DELETE | `/agent-workspaces/{agentWorkspaceId}/files/{fileId}` | `DeleteLegacyAgentWorkspaceFile` | Delete agent workspace file |
| PUT | `/agent-workspaces/{agentWorkspaceId}/file` | `PutLegacyAgentWorkspaceFile` | Create or replace agent workspace file |
| POST | `/collections/{collectionId}/attachments` | `UploadAttachment` | Upload attachment |
| POST | `/changes/list` | `changes.list` | List changes |
| GET | `/collections/{collectionId}/files` | `ListAgentWorkspaceFiles` | List collection files |
| GET | `/collections/{collectionId}/files/{fileId}` | `GetAgentWorkspaceFile` | Get collection file |
| DELETE | `/collections/{collectionId}/files/{fileId}` | `DeleteAgentWorkspaceFile` | Delete collection file |
| PUT | `/collections/{collectionId}/file` | `PutAgentWorkspaceFile` | Create or replace collection file |
| POST | `/collections/{collectionId}/fields` | `CreateCollectionField` | Create field |
| PATCH | `/collections/{collectionId}/fields/{fieldId}` | `UpdateCollectionField` | Update field |
| DELETE | `/collections/{collectionId}/fields/{fieldId}` | `DeleteCollectionField` | Soft-delete field |
| PATCH | `/collections/{collectionId}/fields/reorder` | `ReorderCollectionFields` | Reorder fields |
| GET | `/collections/{collectionId}/intake-forms` | `ListIntakeForms` | List intake forms |
| POST | `/collections/{collectionId}/intake-forms` | `CreateIntakeForm` | Create intake form |
| GET | `/collections/{collectionId}/intake-forms/{intakeFormId}` | `GetIntakeForm` | Get intake form |
| PATCH | `/collections/{collectionId}/intake-forms/{intakeFormId}` | `UpdateIntakeForm` | Update intake form |
| DELETE | `/collections/{collectionId}/intake-forms/{intakeFormId}` | `DeleteIntakeForm` | Delete intake form |
| GET | `/intake-forms/{intakeFormToken}` | `GetPublicIntakeForm` | Get public intake form |
| POST | `/intake-forms/{intakeFormToken}/submissions` | `SubmitIntakeForm` | Submit intake form response |
| GET | `/share/{publicShareToken}/resolve` | `ResolvePublicShare` | Resolve public share |
| GET | `/share/{publicShareToken}` | `GetPublicShareCollection` | Get public share collection |
| GET | `/share/{publicShareToken}/rows` | `ListPublicShareRecords` | List public share records |
| POST | `/share/{publicShareToken}/row-queries` | `QueryPublicShareRecords` | Query public share records |
| POST | `/share/{publicShareToken}/row-aggregations` | `AggregatePublicShareRecords` | Aggregate public share records |
| GET | `/share/{publicShareToken}/rows/{rowId}` | `GetPublicShareRecord` | Get public share record |
| POST | `/collections/{collectionId}/rows` | `CreateCollectionRecords` | Create records |
| GET | `/collections/{collectionId}/rows` | `ListCollectionRecords` | List records |
| PATCH | `/collections/{collectionId}/rows` | `UpdateCollectionRecords` | Update record values |
| DELETE | `/collections/{collectionId}/rows` | `DeleteCollectionRecords` | Soft-delete records |
| POST | `/collections/{collectionId}/row-queries` | `QueryCollectionRecords` | Query records |
| POST | `/collections/{collectionId}/row-aggregations` | `AggregateCollectionRecords` | Aggregate records |
| POST | `/collections/{collectionId}/missing-row-values` | `FindMissingCollectionRecords` | Find records with missing values |
| GET | `/collections/{collectionId}/rows/{rowId}` | `GetCollectionRecord` | Get record |
| GET | `/collections/{collectionId}/rows/{rowId}/activity` | `GetCollectionRecordActivity` | Get record activity |
| POST | `/collections/{collectionId}/row-lookups` | `LookupCollectionRecords` | Look up records |
| POST | `/collections/{collectionId}/csv-imports` | `ImportCollectionRecordsCsv` | Import records from CSV |
| POST | `/collections/{collectionId}/external-id-rows` | `UpsertCollectionRecords` | Upsert records by external ID |
| PATCH | `/collections/{collectionId}/rows/locks` | `SetCollectionRecordLocks` | Lock or unlock records |
| POST | `/collections/{collectionId}/suggestions` | `CreateCollectionSuggestion` | Suggest a record change |
| GET | `/collections/{collectionId}/suggestions` | `ListCollectionSuggestions` | List suggestions |
| GET | `/collections/{collectionId}/suggestions/{suggestionId}` | `GetCollectionSuggestion` | Get suggestion |
| POST | `/collections/{collectionId}/suggestions/{suggestionId}/approvals` | `ApproveCollectionSuggestion` | Approve suggestion |
| POST | `/collections/{collectionId}/suggestions/{suggestionId}/rejections` | `RejectCollectionSuggestion` | Reject suggestion |
| POST | `/collections` | `CreateCollection` | Create collection |
| GET | `/collections` | `ListCollections` | List collections |
| GET | `/collections/{collectionId}` | `GetCollectionDefinition` | Get collection |
| PATCH | `/collections/{collectionId}` | `UpdateCollection` | Update collection |
| DELETE | `/collections/{collectionId}` | `DeleteCollection` | Soft-delete collection |
| POST | `/collections/{collectionId}/copies` | `DuplicateCollection` | Duplicate collection |
| PATCH | `/collections/{collectionId}/view` | `UpdateCollectionView` | Update collection view preferences |
| GET | `/collections/{collectionId}/views` | `ListCollectionViews` | List collection views |
| POST | `/collections/{collectionId}/views` | `CreateCollectionView` | Create collection view |
| PATCH | `/collections/{collectionId}/views` | `ReorderCollectionViews` | Reorder collection views |
| PATCH | `/collections/{collectionId}/views/{viewId}` | `UpdateSavedCollectionView` | Update collection view |
| DELETE | `/collections/{collectionId}/views/{viewId}` | `DeleteCollectionView` | Delete collection view |
| POST | `/collections/{collectionId}/views/{viewId}/copies` | `DuplicateCollectionView` | Duplicate collection view |
| PATCH | `/collections/{collectionId}/views/{viewId}/default` | `SetDefaultCollectionView` | Set default collection view |
| GET | `/collections/{collectionId}/public-share` | `GetCollectionPublicShareState` | Get collection public share state |
| POST | `/collections/{collectionId}/public-share` | `EnableCollectionPublicShare` | Enable or rotate collection public share |
| DELETE | `/collections/{collectionId}/public-share` | `DisableCollectionPublicShare` | Disable collection public share |
| GET | `/webhooks` | `ListWebhooks` | List workspace webhooks |
| POST | `/webhooks` | `CreateWebhook` | Create webhook |
| PATCH | `/webhooks/{webhookId}` | `UpdateWebhook` | Update webhook |
| DELETE | `/webhooks/{webhookId}` | `DeleteWebhook` | Delete webhook |
| POST | `/webhooks/{webhookId}/tests` | `TestWebhook` | Send test event |
| GET | `/webhooks/{webhookId}/deliveries` | `ListWebhookDeliveries` | List webhook deliveries |

## Parameters

- `collectionId`, `rowId`, `fieldId`, `fileId`, `viewId`, `intakeFormId`, `suggestionId`, `webhookId`, and `agentWorkspaceId` path parameters are UUID strings.
- `apiKeyId` is a non-empty string.
- `publicShareToken` is a 43-character URL-safe token matching `^[A-Za-z0-9_-]{43}$`; `intakeFormToken` is a public token string from 32 to 256 characters.
- List endpoints generally default `limit` to `50` and cap `limit` at `100`; webhook deliveries default to `20` and cap at `50`.
- Record read and write endpoints support `fields: "*"` or an array of up to 100 field keys. For GET query strings, pass `--query fields='*'`; for POST/PATCH requests, include `fields` in the JSON body.
- Field keys in record values must match `^[A-Za-z_][A-Za-z0-9_]*$`.
- `POST /collections/{collectionId}/attachments` accepts `name`, optional `mimeType`, and `dataBase64` up to 34,952,536 characters.
- File list endpoints accept `limit`, `cursor`, `prefix`, and `q`. File upsert endpoints accept `path` and optional `content` up to 10,000 characters.
- `POST /changes/list` supports `limit`, `cursor`, `includePayload`, `direction=asc|desc`, `collectionId`, `operation`, `entityType`, and `entityId`; `direction` defaults to `asc`.
- `GET /webhooks` accepts optional `collectionId`; `GET /webhooks/{webhookId}/deliveries` accepts optional `limit`.

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

Update API key access with `PATCH /api-keys/{apiKeyId}/access`:

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

The `access` property is required. `preset` is optional and must be 1 to 64 characters. `reason` is optional and must be 1 to 500 characters.

Roll an API key with `POST /api-keys/{apiKeyId}/rotations`.

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
          "value": "open"
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
  "projectName": "Operations",
  "visibility": "primary"
}
```

`PATCH /collections/{collectionId}` accepts any subset of `name`, `icon`, `description`, `isLocked`, `projectName`, `visibility`, and `metadata`.

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

Reorder fields:

```json
{
  "fieldIds": ["00000000-0000-0000-0000-000000000000"]
}
```

Duplicate a collection:

```json
{
  "duplicateMode": "structure"
}
```

Duplicate modes: `structure`, `data`.

## Records

Create, update, delete, lock, or upsert records. Record write batches require 1 to 1000 rows. External IDs must be 1 to 191 characters.

Create records:

```json
{
  "rows": [
    {
      "externalId": "external-id",
      "values": {
        "field_key": "value"
      }
    }
  ],
  "fields": "*",
  "returning": "rows",
  "mutationMode": "partial"
}
```

Update records by `rowId` or `externalId`:

```json
{
  "rows": [
    {
      "rowId": "00000000-0000-0000-0000-000000000000",
      "values": {
        "field_key": "new value"
      }
    }
  ],
  "fields": "*",
  "returning": "rows",
  "mutationMode": "partial"
}
```

Delete records by `rowId` or `externalId`:

```json
{
  "rows": [
    {
      "externalId": "external-id"
    }
  ],
  "mutationMode": "all_or_nothing"
}
```

Lock or unlock records:

```json
{
  "rows": [
    {
      "rowId": "00000000-0000-0000-0000-000000000000"
    }
  ],
  "isLocked": true,
  "mutationMode": "partial"
}
```

Batch write modes: `partial` attempts each record independently and returns per-item results. `all_or_nothing` applies the whole batch transactionally.

Create and update record calls default to `returning: "ids"` and `fields: []`. Use `returning: "rows"` plus `fields: "*"` or a field-key array when the response should include record values. Upsert-by-external-ID calls do not accept `fields` or `returning`.

Upload an attachment before storing it in an attachment field:

```json
{
  "name": "file.pdf",
  "mimeType": "application/pdf",
  "dataBase64": "<base64 file contents>"
}
```

Attachment field values use arrays of attachment metadata returned by `POST /collections/{collectionId}/attachments`:

```json
{
  "attachment_field": [
    {
      "id": "00000000-0000-0000-0000-000000000000",
      "name": "file.pdf",
      "mimeType": "application/pdf",
      "size": 12345,
      "url": "https://api.semifluid.ai/...",
      "createdAt": "2026-06-17T00:00:00.000Z"
    }
  ]
}
```

## Collection Files

Collection files are text files associated with a collection. They are separate from attachment uploads used in attachment field values.

List collection files:

```bash
python3 scripts/semifluid_api.py get /collections/{collectionId}/files --query limit=50 --query prefix=/
```

List endpoints accept `limit` from 1 to 100, optional `cursor`, optional `prefix` defaulting to `/`, and optional `q` search text up to 256 characters.

Create or replace a collection file:

```json
{
  "path": "/notes/summary.md",
  "content": "# Summary\n"
}
```

Use `PUT /collections/{collectionId}/file`. `path` is required, must be 1 to 191 characters, and `content` is optional with a 10,000 character limit. The response is either `{ "mode": "applied", "file": ... }` or `{ "mode": "suggested", "suggestion": ... }` depending on the caller's permissions.

Get or delete a file by ID with `GET /collections/{collectionId}/files/{fileId}` and `DELETE /collections/{collectionId}/files/{fileId}`.

Legacy agent-workspace file endpoints have the same request and response shapes under `/agent-workspaces/{agentWorkspaceId}/files`, `/agent-workspaces/{agentWorkspaceId}/files/{fileId}`, and `/agent-workspaces/{agentWorkspaceId}/file`.

Look up records by ID:

```json
{
  "rowIds": ["00000000-0000-0000-0000-000000000000"],
  "fields": "*"
}
```

Upsert records by external ID with `POST /collections/{collectionId}/external-id-rows`:

```json
{
  "rows": [
    {
      "externalId": "external-id",
      "values": {
        "field_key": "value"
      }
    }
  ],
  "mutationMode": "partial"
}
```

Import CSV rows with `POST /collections/{collectionId}/csv-imports`:

```json
{
  "csv": "name,status\nFirst task,Open\n",
  "headerRow": true,
  "columns": ["name", "status"],
  "validateOnly": false
}
```

CSV imports are atomic: if any cell fails validation, no records are created. Requests accept at most 1000 data rows and raw CSV text up to 5,242,880 characters. If `columns` is omitted, `headerRow` must be true and headers are auto-mapped to fields by key or name case-insensitively. Use `null` in `columns` to skip a CSV column.

## Row Activity

Read row-level activity with `GET /collections/{collectionId}/rows/{rowId}/activity`. It returns paginated changes for that row.

```bash
python3 scripts/semifluid_api.py get /collections/{collectionId}/rows/{rowId}/activity --query limit=20
```

Query parameters:

- `limit`: 1 to 100, default 50.
- `cursor`: pass the previous response `pageInfo.nextCursor` for the next page.

Each activity item includes:

- `kind`: `created`, `updated`, or `deleted`.
- `occurredAt` and `requestId`.
- `actor`: `{ "type": "user" | "api_key", "name": string | null }`.
- `changes`: field-level `fieldKey`, `before`, and `after` values.

## Query Records

Use `POST /collections/{collectionId}/row-queries`:

```json
{
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

Filter operators: `eq`, `neq`, `is_empty`, `is_not_empty`, `gt`, `gte`, `lt`, `lte`, `contains`, `starts_with`, `in`, `not_in`, `between`.

Query limits: `limit` is 1-100, `search` is at most 256 characters, filters are capped at 25, sort entries are capped at 10, and explicit `fields` arrays are capped at 100 field keys.

`search` performs case-insensitive broad record search over searchable text-like values, including text, markdown, email, phone, URL, select/status labels, multi-select labels, and attachment file names.

## Aggregate Records

Use `POST /collections/{collectionId}/row-aggregations`:

```json
{
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

Aggregate metric operations: `count`, `count_values`, `count_empty`, `count_unique`, `count_true`, `count_false`, `count_items`, `count_unique_items`, `sum`, `avg`, `min`, `max`.

Aggregate requests default to one metric: `{ "key": "count", "operation": "count" }`. Requests accept 1 to 10 metrics. Metric keys must be 1 to 128 characters and match `^[A-Za-z0-9][A-Za-z0-9_.:-]*$`. `limit` applies to grouped aggregate results only; ungrouped aggregate queries always return one row.

`countLimit` can cap count-like ungrouped metrics from 1 to 1,000,000. Responses return `countLimit + 1` when more records or values exist.

Date buckets: `day`, `week`, `month`, `year`. Week buckets start on Monday and date buckets use UTC.

## Missing Values

Use `POST /collections/{collectionId}/missing-row-values`:

```json
{
  "fields": ["summary", "owner"],
  "contextFields": ["name"],
  "matchMode": "any",
  "limit": 50
}
```

Use `fields: "*"` to inspect all fields. Missing match modes: `any`, `all`.

## Suggestions

Suggestions let a caller propose record creates, updates, or deletes for later review. Use `POST /collections/{collectionId}/suggestions`.

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

List suggestions with `GET /collections/{collectionId}/suggestions`. Optional query parameters: `limit`, `cursor`, and `status=pending|approved|rejected`.

Approve or reject a suggestion:

```json
{
  "note": "Reviewed and accepted"
}
```

Use `POST /collections/{collectionId}/suggestions/{suggestionId}/approvals` or `POST /collections/{collectionId}/suggestions/{suggestionId}/rejections`.

## Intake Forms

Manage forms with collection-authenticated endpoints:

- `GET /collections/{collectionId}/intake-forms`
- `POST /collections/{collectionId}/intake-forms`
- `GET /collections/{collectionId}/intake-forms/{intakeFormId}`
- `PATCH /collections/{collectionId}/intake-forms/{intakeFormId}`
- `DELETE /collections/{collectionId}/intake-forms/{intakeFormId}`

Create an intake form:

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
python3 scripts/semifluid_api.py get /intake-forms/{intakeFormToken} --no-auth
python3 scripts/semifluid_api.py post /intake-forms/{intakeFormToken}/submissions --json @submission.json --no-auth
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

Submission values are keyed by public field keys. Attachment fields use attachment metadata arrays.

## Collection View

`PATCH /collections/{collectionId}/view` updates collection view preferences. `PATCH /collections/{collectionId}` can also update collection metadata, including `metadata.collectionView`. In `PATCH /collections/{collectionId}/view` and saved view updates, collection-view preference properties can be set to `null` to clear them.

```json
{
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

Field calculations: `count_all`, `count_values`, `count_unique`, `count_empty`, `count_not_empty`, `count_true`, `count_false`, `percent_true`, `percent_false`, `count_items`, `count_unique_items`, `percent_empty`, `percent_not_empty`, `sum`, `average`, `min`, `max`, `earliest`, `latest`.

Collection-view filters are capped at 25, sort entries at 10, field order and hidden field IDs at 100, and field widths at 96 to 1600 pixels.

## Saved Views

Create a saved view:

```json
{
  "name": "Open tasks",
  "type": "table",
  "config": {}
}
```

Saved view create defaults to `name: "Table"` and `type: "table"` when omitted. Saved view names must be 1 to 120 characters. View types: `table`, `grid`, `board`, `map`, `calendar`, `list`, `form`, `dashboard`.

Reorder saved views:

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
    "filterMode": "all"
  }
}
```

Duplicate a saved view:

```json
{
  "name": "Open tasks copy"
}
```

Set the default saved view with `PATCH /collections/{collectionId}/views/{viewId}/default`.

## Public Shares

Public share management endpoints use collection auth:

- `GET /collections/{collectionId}/public-share`
- `POST /collections/{collectionId}/public-share`
- `DELETE /collections/{collectionId}/public-share`

Enable or rotate a public share:

```json
{
  "publicShareToken": "optional-43-character-url-safe-token"
}
```

Public share read endpoints use a `publicShareToken` and do not require the workspace API key when the share is enabled:

- `GET /share/{publicShareToken}/resolve`
- `GET /share/{publicShareToken}`
- `GET /share/{publicShareToken}/rows`
- `GET /share/{publicShareToken}/rows/{rowId}`
- `POST /share/{publicShareToken}/row-queries`
- `POST /share/{publicShareToken}/row-aggregations`

When using the helper for public read endpoints, pass `--no-auth` unless the user explicitly wants to send an API key. Public share record query and aggregation request bodies match the authenticated collection record query and aggregation bodies.

## Webhooks

Webhook endpoints use workspace API key auth. Treat webhook secrets and delivery payloads as sensitive; do not include them in final answers, logs, or files unless the user explicitly asks and the destination is appropriate. `POST /webhooks` returns the webhook `secret` only in the create response.

List all webhooks, or filter by collection:

```bash
python3 scripts/semifluid_api.py get /webhooks
python3 scripts/semifluid_api.py get /webhooks --query collectionId=00000000-0000-0000-0000-000000000000
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

Delete a webhook with `DELETE /webhooks/{webhookId}`.

Send a test event:

```bash
python3 scripts/semifluid_api.py post /webhooks/{webhookId}/tests
```

List recent deliveries:

```bash
python3 scripts/semifluid_api.py get /webhooks/{webhookId}/deliveries --query limit=20
```

Webhook delivery results include `eventType`, `status` (`success` or `failed`), `attempts`, `responseStatus`, `errorMessage`, `durationMs`, `payload`, and `createdAt`.

## Changes

List workspace changes with `POST /changes/list`:

```json
{
  "limit": 50,
  "cursor": "next-cursor",
  "includePayload": false,
  "direction": "desc",
  "collectionId": "00000000-0000-0000-0000-000000000000",
  "operation": "rows.create",
  "entityType": "row",
  "entityId": "00000000-0000-0000-0000-000000000000"
}
```

For exact schemas, run:

```bash
python3 scripts/semifluid_api.py spec --output /tmp/semifluid-spec.json
```
