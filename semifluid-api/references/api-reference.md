# Semifluid API Reference

Source: `https://api.semifluid.ai/api-reference/spec.json`

OpenAPI: `3.1.1`

API version: `0.1.92`

Base URL: `https://api.semifluid.ai`

Auth: send the API key as `x-api-key: <key>`. The helper also supports `Authorization: Bearer <key>` with `--auth-header bearer`, but prefer `x-api-key`.

The helper reports each API request duration to stderr as `Timing: METHOD /path -> HTTP status in N.N ms`, while response bodies remain on stdout.

## Current Naming

The current API uses `fields` and `field` in request parameters and bodies. Older docs, examples, or code may use `properties` and `property`; prefer the current `fields` terminology and endpoint paths below.

## Common Commands

```bash
python3 scripts/semifluid_api.py health
python3 scripts/semifluid_api.py operations
python3 scripts/semifluid_api.py get /tables
python3 scripts/semifluid_api.py get /tables/{tableId}
python3 scripts/semifluid_api.py get /tables/{tableId}/rows --query limit=50 --query fields='*'
python3 scripts/semifluid_api.py post /tables/{tableId}/row-queries --json @query.json
python3 scripts/semifluid_api.py post /tables/{tableId}/row-aggregations --json @aggregate.json
python3 scripts/semifluid_api.py patch /tables/{tableId}/rows --json @rows-update.json
python3 scripts/semifluid_api.py post /changes/list --json '{"limit":10,"direction":"desc"}'
```

## Operations

| Method | Path | Operation | Purpose |
| --- | --- | --- | --- |
| GET | `/health` | `HealthCheck` | Health check |
| GET | `/api-keys` | `ListApiKeys` | List workspace API keys |
| POST | `/api-keys` | `CreateApiKey` | Create workspace API key |
| DELETE | `/api-keys/{apiKeyId}` | `DeleteApiKey` | Delete workspace API key |
| PATCH | `/api-keys/{apiKeyId}` | `RenameApiKey` | Rename workspace API key |
| POST | `/api-keys/{apiKeyId}/rotations` | `RollApiKey` | Roll workspace API key |
| POST | `/tables/{tableId}/attachments` | `UploadAttachment` | Upload attachment |
| POST | `/changes/list` | `changes.list` | List workspace changes |
| POST | `/tables/{tableId}/fields` | `CreateTableField` | Create field |
| PATCH | `/tables/{tableId}/fields/{fieldId}` | `UpdateTableField` | Update field |
| DELETE | `/tables/{tableId}/fields/{fieldId}` | `DeleteTableField` | Soft-delete field |
| PATCH | `/tables/{tableId}/fields/reorder` | `ReorderTableFields` | Reorder fields |
| GET | `/public-shares/{publicShareToken}/resolve` | `ResolvePublicShare` | Resolve public share |
| GET | `/public-shares/{publicShareToken}` | `GetPublicShareTable` | Get public share table |
| GET | `/public-shares/{publicShareToken}/rows` | `ListPublicShareRows` | List public share rows |
| POST | `/public-shares/{publicShareToken}/row-queries` | `QueryPublicShareRows` | Query public share rows |
| POST | `/public-shares/{publicShareToken}/row-aggregations` | `AggregatePublicShareRows` | Aggregate public share rows |
| GET | `/public-shares/{publicShareToken}/rows/{rowId}` | `GetPublicShareRow` | Get public share row |
| POST | `/tables/{tableId}/rows` | `CreateTableRows` | Create rows |
| GET | `/tables/{tableId}/rows` | `ListTableRows` | List rows |
| PATCH | `/tables/{tableId}/rows` | `UpdateTableRows` | Update row values |
| DELETE | `/tables/{tableId}/rows` | `DeleteTableRows` | Soft-delete rows |
| POST | `/tables/{tableId}/row-queries` | `QueryTableRows` | Query rows |
| POST | `/tables/{tableId}/row-aggregations` | `AggregateTableRows` | Aggregate rows |
| POST | `/tables/{tableId}/missing-row-values` | `FindMissingTableRows` | Find rows with missing values |
| GET | `/tables/{tableId}/rows/{rowId}` | `GetTableRow` | Get row |
| POST | `/tables/{tableId}/row-lookups` | `LookupTableRows` | Look up rows by ID |
| POST | `/tables/{tableId}/external-id-rows` | `UpsertTableRows` | Upsert rows by external ID |
| POST | `/tables` | `CreateTable` | Create table |
| GET | `/tables` | `ListTables` | List tables |
| GET | `/tables/{tableId}` | `GetTableDefinition` | Get table |
| PATCH | `/tables/{tableId}` | `UpdateTable` | Update table |
| DELETE | `/tables/{tableId}` | `DeleteTable` | Soft-delete table |
| POST | `/tables/{tableId}/copies` | `DuplicateTable` | Duplicate table |
| PATCH | `/tables/{tableId}/view` | `UpdateTableView` | Update table view preferences |
| GET | `/tables/{tableId}/views` | `ListTableViews` | List table views |
| POST | `/tables/{tableId}/views` | `CreateTableView` | Create table view |
| PATCH | `/tables/{tableId}/views` | `ReorderTableViews` | Reorder table views |
| PATCH | `/tables/{tableId}/views/{viewId}` | `UpdateSavedTableView` | Update table view |
| DELETE | `/tables/{tableId}/views/{viewId}` | `DeleteTableView` | Delete table view |
| POST | `/tables/{tableId}/views/{viewId}/copies` | `DuplicateTableView` | Duplicate table view |
| PATCH | `/tables/{tableId}/views/{viewId}/default` | `SetDefaultTableView` | Set default table view |
| GET | `/tables/{tableId}/public-share` | `GetTablePublicShareState` | Get table public share state |
| POST | `/tables/{tableId}/public-share` | `EnableTablePublicShare` | Enable or rotate table public share |
| DELETE | `/tables/{tableId}/public-share` | `DisableTablePublicShare` | Disable table public share |

## Parameters

- `tableId`, `rowId`, `fieldId`, and `viewId` path parameters are UUID strings.
- `apiKeyId` is a non-empty string.
- `publicShareToken` is a public share token string.
- List endpoints generally default `limit` to `50` and cap `limit` at `100`.
- Row read and row write endpoints support `fields: "*"` or an array of up to 100 field keys. For GET query strings, pass `--query fields='*'`; for POST/PATCH requests, include `fields` in the JSON body.
- `POST /changes/list` supports `limit`, `cursor`, `includePayload`, `direction=asc|desc`, `tableId`, `operation`, `entityType`, and `entityId`.

## API Keys

Create a workspace-wide key:

```json
{
  "name": "Agent key",
  "access": {
    "kind": "workspace"
  }
}
```

Create a table-scoped key:

```json
{
  "name": "Readonly table key",
  "access": {
    "kind": "table_scoped",
    "grants": [
      {
        "tableId": "00000000-0000-0000-0000-000000000000",
        "scope": "read_only"
      }
    ]
  }
}
```

Table-scoped grant scopes: `read_only`, `row_editor`, `table_admin`.

Roll an API key with `POST /api-keys/{apiKeyId}/rotations`.

## Tables And Fields

Create a table:

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
  "options": [
    {
      "label": "Open",
      "value": "open",
      "color": "green"
    }
  ]
}
```

Field create requires `name`, `key`, and `type`. Field update accepts `name`, `description`, `config`, `isRequired`, `isHidden`, `isPrimary`, and `options`. Select/status options use `label`, `value`, optional `color`, and optional `id` when updating.

Field types from the spec: `text`, `markdown`, `select`, `status`, `multi_select`, `attachment`, `phone`, `number`, `currency`, `auto_number`, `boolean`, `date`, `date_time`, `email`, `url`, `relation`, `lookup`, `rollup`.

Reorder fields:

```json
{
  "fieldIds": ["00000000-0000-0000-0000-000000000000"]
}
```

Duplicate a table:

```json
{
  "duplicateMode": "structure"
}
```

Duplicate modes: `structure`, `data`.

## Rows

Create, update, delete, or upsert rows. Row write batches allow 1 to 1000 rows. Field keys must match `^[A-Za-z_][A-Za-z0-9_]*$`.

Create rows:

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

Update rows by `rowId` or `externalId`:

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

Delete rows by `rowId` or `externalId`:

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

Batch write modes: `partial` attempts each row independently and returns per-item results. `all_or_nothing` applies the whole batch transactionally.

Create and update row calls default to `returning: "ids"` and `fields: []`. Use `returning: "rows"` plus `fields: "*"` or a field-key array when the response should include row values.

Attachment field values use the attachment metadata returned by `POST /tables/{tableId}/attachments`:

```json
{
  "name": "file.pdf",
  "mimeType": "application/pdf",
  "dataBase64": "<base64 file contents>"
}
```

Look up rows by ID:

```json
{
  "rowIds": ["00000000-0000-0000-0000-000000000000"],
  "fields": "*"
}
```

Upsert rows by external ID with `POST /tables/{tableId}/external-id-rows`:

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

## Query Rows

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

`search` performs case-insensitive broad row search over searchable text-like row values, including text, markdown, email, phone, URL, select/status labels, multi-select labels, and attachment file names.

## Aggregate Rows

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

`countLimit` can cap count-like ungrouped metrics from 1 to 1,000,000. Responses return `countLimit + 1` when more rows or values exist.

Date buckets: `day`, `week`, `month`, `year`. Week buckets start on Monday and date buckets use UTC.

## Missing Values

```json
{
  "fields": ["summary", "owner"],
  "contextFields": ["name"],
  "matchMode": "any",
  "limit": 50
}
```

Use `fields: "*"` to inspect all fields. Missing match modes: `any`, `all`.

## Table View

`PATCH /tables/{tableId}/view` updates table view preferences. `PATCH /tables/{tableId}` can also update table metadata, including `metadata.tableView`.

```json
{
  "tableView": {
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

## Saved Views

Create a saved view:

```json
{
  "name": "Open tasks",
  "type": "table",
  "config": {}
}
```

View types: `table`, `grid`, `board`, `map`, `calendar`, `list`, `form`, `dashboard`.

Reorder saved views:

```json
{
  "viewIds": ["00000000-0000-0000-0000-000000000000"]
}
```

Update a saved view:

```json
{
  "name": "Open tasks",
  "config": {},
  "tableView": {
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

Set the default saved view with `PATCH /tables/{tableId}/views/{viewId}/default`.

## Public Shares

Public share management endpoints use table auth:

- `GET /tables/{tableId}/public-share`
- `POST /tables/{tableId}/public-share`
- `DELETE /tables/{tableId}/public-share`

Public share read endpoints use a `publicShareToken` and do not require the workspace API key when the share is enabled:

- `GET /public-shares/{publicShareToken}/resolve`
- `GET /public-shares/{publicShareToken}`
- `GET /public-shares/{publicShareToken}/rows`
- `GET /public-shares/{publicShareToken}/rows/{rowId}`
- `POST /public-shares/{publicShareToken}/row-queries`
- `POST /public-shares/{publicShareToken}/row-aggregations`

Public share row query and aggregation request bodies match the authenticated table row query and aggregation bodies.

## Changes

List workspace changes with `POST /changes/list`:

```json
{
  "limit": 50,
  "cursor": "next-cursor",
  "includePayload": false,
  "direction": "desc",
  "tableId": "00000000-0000-0000-0000-000000000000",
  "operation": "rows.create",
  "entityType": "row",
  "entityId": "00000000-0000-0000-0000-000000000000"
}
```

For exact schemas, run:

```bash
python3 scripts/semifluid_api.py spec --output /tmp/semifluid-spec.json
```
