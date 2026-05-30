# Semifluid API Reference

Source: `https://api.semifluid.ai/api-reference/spec.json`

OpenAPI: `3.1.1`

API version: `0.1.81`

Base URL: `https://api.semifluid.ai`

Auth: send the API key as `x-api-key: <key>`. The helper also supports `Authorization: Bearer <key>` with `--auth-header bearer`, but prefer `x-api-key`.

The helper reports each API request duration to stderr as `Timing: METHOD /path -> HTTP status in N.N ms`, while response bodies remain on stdout.

## Common Commands

```bash
python3 scripts/semifluid_api.py health
python3 scripts/semifluid_api.py operations
python3 scripts/semifluid_api.py get /tables
python3 scripts/semifluid_api.py get /tables/{tableId}
python3 scripts/semifluid_api.py get /tables/{tableId}/rows --query limit=50 --query properties='*'
python3 scripts/semifluid_api.py post /tables/{tableId}/rows/query --json @query.json
python3 scripts/semifluid_api.py post /tables/{tableId}/rows/aggregate --json @aggregate.json
python3 scripts/semifluid_api.py patch /tables/{tableId}/rows --json @rows-update.json
```

## Operations

| Method | Path | Operation | Purpose |
| --- | --- | --- | --- |
| GET | `/health` | `healthCheck` | Health check |
| GET | `/api-keys` | `apiKeys.list` | List workspace API keys |
| POST | `/api-keys` | `apiKeys.create` | Create workspace API key |
| DELETE | `/api-keys/{apiKeyId}` | `apiKeys.delete` | Delete workspace API key |
| PATCH | `/api-keys/{apiKeyId}` | `apiKeys.rename` | Rename workspace API key |
| POST | `/api-keys/{apiKeyId}/roll` | `apiKeys.roll` | Roll workspace API key |
| POST | `/tables/{tableId}/attachments` | `UploadAttachment` | Upload attachment |
| GET | `/changes` | `ListWorkspaceChanges` | List workspace changes |
| POST | `/tables/{tableId}/properties` | `properties.create` | Create property |
| PATCH | `/tables/{tableId}/properties/{propertyId}` | `properties.update` | Update property |
| DELETE | `/tables/{tableId}/properties/{propertyId}` | `properties.delete` | Soft-delete property |
| PATCH | `/tables/{tableId}/properties/reorder` | `properties.reorder` | Reorder properties |
| POST | `/tables/{tableId}/rows` | `CreateTableRows` | Create rows |
| GET | `/tables/{tableId}/rows` | `ListTableRows` | List rows |
| PATCH | `/tables/{tableId}/rows` | `UpdateTableRows` | Update row values |
| DELETE | `/tables/{tableId}/rows` | `DeleteTableRows` | Soft-delete rows |
| POST | `/tables/{tableId}/rows/query` | `QueryTableRows` | Query rows |
| POST | `/tables/{tableId}/rows/aggregate` | `AggregateTableRows` | Aggregate rows |
| POST | `/tables/{tableId}/rows/missing` | `FindMissingTableRows` | Find rows with missing values |
| GET | `/tables/{tableId}/rows/{rowId}` | `GetTableRow` | Get row |
| POST | `/tables/{tableId}/rows/upsert` | `UpsertTableRows` | Upsert rows by external ID |
| POST | `/tables` | `tables.create` | Create table |
| GET | `/tables` | `tables.list` | List tables |
| GET | `/tables/{tableId}` | `GetTableDefinition` | Get table |
| PATCH | `/tables/{tableId}` | `tables.update` | Update table |
| DELETE | `/tables/{tableId}` | `tables.delete` | Soft-delete table |
| POST | `/tables/{tableId}/duplicate` | `tables.duplicate` | Duplicate table |
| PATCH | `/tables/{tableId}/view` | `tables.updateView` | Update table view preferences |

## Parameters

- `tableId`, `rowId`, and `propertyId` path parameters are UUID strings.
- `apiKeyId` is a non-empty string.
- List endpoints generally default `limit` to `50` and cap `limit` at `100`.
- `GET /tables/{tableId}/rows`, `GET /tables/{tableId}/rows/{rowId}`, `POST /tables/{tableId}/rows`, `PATCH /tables/{tableId}/rows`, `POST /tables/{tableId}/rows/query`, and `POST /tables/{tableId}/rows/missing` support `properties: "*"` or an array of up to 100 property keys. For GET query strings, pass `--query properties='*'`; for POST/PATCH requests, include `properties` in the JSON body.
- `GET /changes` supports `limit`, `cursor`, `includePayload`, `direction=asc|desc`, `operation`, `entityType`, and `entityId`.

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

## Tables And Properties

Create a table:

```json
{
  "name": "Tasks",
  "slug": "tasks",
  "icon": {
    "type": "emoji",
    "emoji": "T"
  },
  "description": "Task tracker",
  "isLocked": false,
  "properties": [
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

Property create requires `name`, `key`, and `type`. Property update accepts `name`, `description`, `config`, `isRequired`, `isHidden`, and `options`. Select options use `label`, `value`, optional `color`, and optional `id` when updating.

Property types from the spec: `text`, `markdown`, `select`, `multi_select`, `attachment`, `phone`, `number`, `currency`, `auto_number`, `boolean`, `date`, `date_time`, `email`, `url`.

Table duplicate requires:

```json
{
  "mode": "structure"
}
```

Duplicate modes: `structure`, `data`.

## Rows

Create, update, delete, or upsert rows. Row write batches allow 1 to 1000 rows. Property keys must match `^[A-Za-z_][A-Za-z0-9_]*$`.

```json
{
  "rows": [
    {
      "externalId": "external-id",
      "values": {
        "property_key": "value"
      }
    }
  ],
  "properties": "*",
  "returning": "rows",
  "mode": "partial"
}
```

Update rows by `rowId` or `externalId`:

```json
{
  "rows": [
    {
      "rowId": "00000000-0000-0000-0000-000000000000",
      "values": {
        "property_key": "new value"
      }
    }
  ],
  "properties": "*",
  "returning": "rows",
  "mode": "partial"
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
  "mode": "all_or_nothing"
}
```

Batch write modes: `partial` attempts each row independently and returns per-item results. `all_or_nothing` applies the whole batch transactionally.

Create and update row calls default to `returning: "ids"` and `properties: []`. Use `returning: "rows"` plus `properties: "*"` or a property-key array when the response should include row values.

Attachment property values use the attachment metadata returned by `POST /tables/{tableId}/attachments`:

```json
{
  "name": "file.pdf",
  "mimeType": "application/pdf",
  "dataBase64": "<base64 file contents>"
}
```

## Query Rows

```json
{
  "limit": 50,
  "cursor": "next-cursor",
  "q": "search text",
  "properties": "*",
  "filters": [
    {
      "property": "status",
      "operator": "eq",
      "value": "Open"
    }
  ],
  "filterMode": "all",
  "sort": [
    {
      "property": "createdAt",
      "direction": "desc"
    }
  ]
}
```

Filter operators: `eq`, `neq`, `is_empty`, `is_not_empty`, `gt`, `gte`, `lt`, `lte`, `contains`, `starts_with`, `in`.

Query limits: `limit` is 1-100, `q` is at most 256 characters, filters are capped at 25, sort entries are capped at 10, and explicit `properties` arrays are capped at 100 property keys.

`q` searches searchable text-like row values, including text, markdown, email, phone, URL, select labels, multi-select labels, and attachment file names.

## Aggregate Rows

```json
{
  "q": "search text",
  "filters": [
    {
      "property": "status",
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
      "property": "amount"
    }
  ],
  "groupBy": {
    "property": "createdAt",
    "dateBucket": "month"
  },
  "sort": {
    "metric": "total",
    "direction": "desc"
  },
  "limit": 100
}
```

Aggregate metric operations: `count`, `count_values`, `count_empty`, `count_unique`, `sum`, `avg`, `min`, `max`.

Date buckets: `day`, `week`, `month`, `year`. Week buckets start on Monday and date buckets use UTC.

## Missing Values

```json
{
  "properties": ["summary", "owner"],
  "contextProperties": ["name"],
  "mode": "any",
  "limit": 50
}
```

Use `properties: "*"` to inspect all properties. Missing modes: `any`, `all`.

## Table View

```json
{
  "tableView": {
    "filters": [
      {
        "property": "status",
        "operator": "eq",
        "value": "Open"
      }
    ],
    "sort": [
      {
        "property": "createdAt",
        "direction": "desc"
      }
    ],
    "columnOrder": ["00000000-0000-0000-0000-000000000000"],
    "hiddenColumnIds": [],
    "columnSizing": {
      "00000000-0000-0000-0000-000000000000": 240
    },
    "columnCalculations": {
      "00000000-0000-0000-0000-000000000000": "count_values"
    }
  }
}
```

Column calculations: `count_all`, `count_values`, `count_unique`, `count_empty`, `count_not_empty`, `percent_empty`, `percent_not_empty`, `sum`, `average`, `min`, `max`, `earliest`, `latest`.

For exact schemas, run:

```bash
python3 scripts/semifluid_api.py spec --output /tmp/semifluid-spec.json
```
