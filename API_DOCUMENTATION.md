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
- **Content Type**: `multipart/form-data`
- **Form Fields**:
  - `name`: string (required)
  - `description`: string (optional)
  - `direction`: string, default: "ltr" (optional)
  - `language`: string, default: "English" (optional)
  - `price`: float, default: 0.0 (optional)
  - `is_free`: boolean, default: true (optional)
  - `is_enabled`: boolean, default: true (optional)
  - `category`: string (optional)
  - `sort_order`: integer, default: 0 (optional)
  - `template_file`: file (required) - The HTML template file
  - `preview_file`: file (optional) - The preview image file
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
- **Content Type**: `multipart/form-data`
- **Form Fields** (all optional):
  - `name`: string
  - `description`: string
  - `direction`: string
  - `language`: string
  - `price`: float
  - `is_free`: boolean
  - `is_enabled`: boolean
  - `category`: string
  - `sort_order`: integer
  - `template_file`: file - The HTML template file
  - `preview_file`: file - The preview image file
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


## Admin Auth Endpoints

### Admin Login

- **Route**: `/admin/login`
- **Method**: POST
- **Description**: Authenticate admin and retrieve access token
- **Authentication**: Not required
- **Request Body (JSON)**:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **Response Model**: `Token`
  ```json
  {
    "access_token": "string",
    "token_type": "bearer"
  }
  ```

## Admin Wallet Endpoints

### List Wallet Charges (Admin)

- **Route**: `/admin/wallet/charges`
- **Method**: GET
- **Description**: List wallet charge requests with optional status filter
- **Authentication**: Required (Admin)
- **Query Parameters**:
  - `status` (optional): string (e.g., `PENDING`, `ACCEPTED`, `REJECTED`)
  - `skip` (optional): integer, default: 0
  - `limit` (optional): integer, default: 100, max: 1000
- **Response Model**: List of `WalletChargeResponse`
  ```json
  [
    {
      "id": 0,
      "user_id": 0,
      "amount": 0.0,
      "receipt_path": "uploads/wallet_receipts/receipt_1_file.png",
      "time": "2024-01-01T00:00:00Z",
      "status": "PENDING"
    }
  ]
  ```

### Get Wallet Charge by ID (Admin)

- **Route**: `/admin/wallet/charges/{charge_id}`
- **Method**: GET
- **Description**: Get details of a wallet charge by ID
- **Authentication**: Required (Admin)
- **Path Parameters**:
  - `charge_id`: integer
- **Response Model**: `WalletChargeResponse`
  ```json
  {
    "id": 1,
    "user_id": 42,
    "amount": 100.0,
    "receipt_path": "uploads/wallet_receipts/receipt_42_invoice.jpg",
    "time": "2024-01-01T00:00:00Z",
    "status": "PENDING"
  }
  ```

### Accept Wallet Charge (Admin)

- **Route**: `/admin/wallet/charges/{charge_id}/accept`
- **Method**: POST
- **Description**: Accept a pending wallet charge and credit user balance
- **Authentication**: Required (Admin)
- **Path Parameters**:
  - `charge_id`: integer
- **Response Model**: `WalletChargeResponse`
  ```json
  {
    "id": 1,
    "user_id": 42,
    "amount": 100.0,
    "receipt_path": "uploads/wallet_receipts/receipt_42_invoice.jpg",
    "time": "2024-01-01T00:00:00Z",
    "status": "ACCEPTED"
  }
  ```

### Reject Wallet Charge (Admin)

- **Route**: `/admin/wallet/charges/{charge_id}/reject`
- **Method**: POST
- **Description**: Reject a pending wallet charge
- **Authentication**: Required (Admin)
- **Path Parameters**:
  - `charge_id`: integer
- **Response Model**: `WalletChargeResponse`
  ```json
  {
    "id": 1,
    "user_id": 42,
    "amount": 100.0,
    "receipt_path": "uploads/wallet_receipts/receipt_42_invoice.jpg",
    "time": "2024-01-01T00:00:00Z",
    "status": "REJECTED"
  }
  ```

## Template Endpoints (User)

### Get All Templates (with purchase flag)

- **Route**: `/template/options`
- **Method**: GET
- **Description**: Get all templates with `purchased` flag relative to current user
- **Authentication**: Required
- **Response Model**: List of `TemplateListResponse`
  ```json
  [
    {
      "id": 10,
      "name": "Modern CV",
      "description": "string",
      "direction": "ltr",
      "language": "English",
      "price": 5.0,
      "is_free": false,
      "is_enabled": true,
      "preview_path": "string",
      "category": "string",
      "sort_order": 0,
      "purchased": false
    }
  ]
  ```

### Purchase Template

- **Route**: `/template/purchase`
- **Method**: POST
- **Description**: Purchase a paid template; deducts from wallet balance
- **Authentication**: Required
- **Request Body (JSON)**:
  ```json
  {
    "template_id": 10
  }
  ```
- **Response Model**: `TemplateListResponse`
  ```json
  {
    "id": 10,
    "name": "Modern CV",
    "description": "string",
    "direction": "ltr",
    "language": "English",
    "price": 5.0,
    "is_free": false,
    "is_enabled": true,
    "preview_path": "string",
    "category": "string",
    "sort_order": 0,
    "purchased": true
  }
  ```

### List My Purchased Templates

- **Route**: `/template/my`
- **Method**: GET
- **Description**: List templates the current user has purchased
- **Authentication**: Required
- **Response Model**: List of `TemplateListResponse`
  ```json
  [
    {
      "id": 10,
      "name": "Modern CV",
      "description": "string",
      "direction": "ltr",
      "language": "English",
      "price": 5.0,
      "is_free": false,
      "is_enabled": true,
      "preview_path": "string",
      "category": "string",
      "sort_order": 0,
      "purchased": true
    }
  ]
  ```

## Wallet Endpoints (User)

### Get Wallet Balance

- **Route**: `/wallet/balance`
- **Method**: GET
- **Description**: Retrieve current user's wallet balance
- **Authentication**: Required
- **Response**:
  ```json
  25.5
  ```

### Create Wallet Charge Request

- **Route**: `/wallet/charges`
- **Method**: POST
- **Description**: Create a pending wallet charge with receipt upload
- **Authentication**: Required
- **Content Type**: `multipart/form-data`
- **Form Fields**:
  - `amount`: float (> 0) (required)
  - `receipt`: file (required)
- **Response Model**: `WalletChargeResponse`
  ```json
  {
    "id": 5,
    "user_id": 42,
    "amount": 100.0,
    "receipt_path": "uploads/wallet_receipts/receipt_42_invoice.jpg",
    "time": "2024-01-01T00:00:00Z",
    "status": "PENDING"
  }
  ```

### List My Wallet Charges

- **Route**: `/wallet/charges`
- **Method**: GET
- **Description**: List wallet charges created by the current user
- **Authentication**: Required
- **Query Parameters**:
  - `skip` (optional): integer, default: 0
  - `limit` (optional): integer, default: 100, max: 1000
- **Response Model**: List of `WalletChargeResponse`
  ```json
  [
    {
      "id": 5,
      "user_id": 42,
      "amount": 100.0,
      "receipt_path": "uploads/wallet_receipts/receipt_42_invoice.jpg",
      "time": "2024-01-01T00:00:00Z",
      "status": "PENDING"
    }
  ]
  ```
