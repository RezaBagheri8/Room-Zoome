## Template Endpoints

### Get All Templates

- **Route**: `/template/options`
- **Method**: GET
- **Description**: Get all available templates with comprehensive data
- **Authentication**: Not required
- **Response Model**: List of `TemplateListResponse`
  ```json
  [
    {
      "id": 0,
      "name": "string",
      "description": "string",
      "direction": "ltr",
      "language": "string",
      "price": 0.0,
      "is_free": true,
      "is_enabled": true,
      "preview_path": "string",
      "category": "string",
      "sort_order": 0
    }
  ]
  ```

## Admin Template Endpoints

### Create Template

- **Route**: `/admin/template/`
- **Method**: POST
- **Description**: Create a new template (Admin only)
- **Authentication**: Required (Admin)
- **Request Model**: `TemplateCreate`
  ```json
  {
    "name": "string",
    "description": "string",
    "direction": "ltr",
    "language": "string",
    "price": 0.0,
    "is_free": true,
    "is_enabled": true,
    "template_path": "string",
    "preview_path": "string",
    "category": "string",
    "sort_order": 0
  }
  ```
- **Response Model**: `TemplateResponse`
  ```json
  {
    "id": 0,
    "name": "string",
    "description": "string",
    "direction": "ltr",
    "language": "string",
    "price": 0.0,
    "is_free": true,
    "is_enabled": true,
    "template_path": "string",
    "preview_path": "string",
    "category": "string",
    "sort_order": 0,
    "created_at": "string",
    "updated_at": "string"
  }
  ```

### Get All Templates (Admin)

- **Route**: `/admin/template/`
- **Method**: GET
- **Description**: Get all templates with admin details (Admin only)
- **Authentication**: Required (Admin)
- **Query Parameters**:
  - `skip` (optional): integer, default: 0
  - `limit` (optional): integer, default: 100
  - `category` (optional): string
  - `enabled_only` (optional): boolean, default: false
- **Response Model**: List of `TemplateResponse`

### Get Template by ID (Admin)

- **Route**: `/admin/template/{template_id}`
- **Method**: GET
- **Description**: Get a specific template with admin details (Admin only)
- **Authentication**: Required (Admin)
- **Path Parameters**:
  - `template_id`: integer
- **Response Model**: `TemplateResponse`

### Update Template

- **Route**: `/admin/template/{template_id}`
- **Method**: PUT
- **Description**: Update a template (Admin only)
- **Authentication**: Required (Admin)
- **Path Parameters**:
  - `template_id`: integer
- **Request Model**: `TemplateUpdate`
  ```json
  {
    "name": "string",
    "description": "string",
    "direction": "ltr",
    "language": "string",
    "price": 0.0,
    "is_free": true,
    "is_enabled": true,
    "template_path": "string",
    "preview_path": "string",
    "category": "string",
    "sort_order": 0
  }
  ```
- **Response Model**: `TemplateResponse`

### Delete Template

- **Route**: `/admin/template/{template_id}`
- **Method**: DELETE
- **Description**: Delete a template (Admin only)
- **Authentication**: Required (Admin)
- **Path Parameters**:
  - `template_id`: integer
- **Response**:
  ```json
  {
    "message": "Template deleted successfully"
  }
  ```

### Toggle Template Status

- **Route**: `/admin/template/{template_id}/toggle-status`
- **Method**: PATCH
- **Description**: Toggle template enabled/disabled status (Admin only)
- **Authentication**: Required (Admin)
- **Path Parameters**:
  - `template_id`: integer
- **Response Model**: `TemplateResponse`

### Update Template Sort Order

- **Route**: `/admin/template/{template_id}/sort-order`
- **Method**: PATCH
- **Description**: Update template sort order (Admin only)
- **Authentication**: Required (Admin)
- **Path Parameters**:
  - `template_id`: integer
- **Query Parameters**:
  - `sort_order`: integer
- **Response Model**: `TemplateResponse`