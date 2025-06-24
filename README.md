# ServiceTitan MCP Integration

A comprehensive Model Context Protocol (MCP) integration for ServiceTitan APIs, organized into focused domain-specific servers.

## Architecture

This integration is split into multiple specialized MCP servers to improve performance, reduce context window usage, and enable focused functionality:

### 🔧 Core Server (`servicetitan-core`)
**File**: `servicetitan_core.py`

Basic ServiceTitan functionality:
- Customer management
- Call tracking and summarization
- Appointment scheduling
- Core CRM operations

**Use cases**: Customer service, basic scheduling, call center operations

### 📦 Pricebook Server (`servicetitan-pricebook`)
**File**: `servicetitan_pricebook.py`

Complete pricebook management:
- Materials (CRUD operations)
- Services (CRUD operations)
- Equipment (CRUD operations)
- Categories and hierarchies
- Discounts and fees
- Images and assets
- Materials markup
- Client-specific pricing
- Export functionality

**Use cases**: Inventory management, pricing updates, catalog maintenance

### 🏭 Inventory Server (`servicetitan-inventory`)
**File**: `servicetitan_inventory.py`

Inventory and supply chain management:
- Inventory adjustments
- Purchase orders and requests
- Receipts and receiving
- Returns processing
- Transfers between locations
- Vendor management
- Warehouse operations
- Truck inventory

**Use cases**: Supply chain, purchasing, warehouse management

### 📊 Job Project Management Server (`servicetitan-jpm`)
**File**: `servicetitan_jpm.py`

Job and project operations:
- Job lifecycle management (create, update, complete, cancel, hold)
- Project management (CRUD, job attachment/detachment)
- Appointment scheduling and management (reschedule, hold, confirmation)
- Job types and configuration management
- Notes, history, and messaging
- Export capabilities for all JPM data

**Use cases**: Project coordination, job scheduling, workflow management, technician dispatch

### 👥 CRM Server (`servicetitan-crm`)
**File**: `servicetitan_crm.py`

Customer relationship management:
- Customer management (enhanced from core with filtering)
- Contact management (CRUD operations)
- Lead management and tracking
- Location management
- Booking and booking provider tags
- Tag management and organization
- Export capabilities for all CRM data

**Use cases**: Customer relationship management, lead tracking, contact organization, booking management

### 🚚 Dispatch Server (`servicetitan-dispatch`)
**File**: `servicetitan_dispatch.py`

Scheduling, routing, and technician management:
- Appointment assignments (assign/unassign technicians)
- Arrival windows management
- Business hours configuration
- Capacity planning and scheduling
- Team management
- Technician shifts and scheduling
- Zone management and routing
- Non-job appointments
- Technician tracking
- GPS provider integration
- Export capabilities for dispatch data

**Use cases**: Technician scheduling, route optimization, capacity planning, dispatch operations

### 💰 Accounting Server (`servicetitan-accounting`)
**File**: `servicetitan_accounting.py`

Financial management and accounting operations:
- Accounts payable credits and payments
- General ledger accounts and account types
- Inventory bills with custom fields and export
- Invoices with adjustment support and item management
- Journal entries with full CRUD operations
- Payments with deposit tracking and custom fields
- Export feeds for all financial data

**Use cases**: Financial management, accounting operations, invoice processing, payment tracking

### ⭐ Customer Interactions Server (`servicetitan-customer-interactions`)
**File**: `servicetitan_customer_interactions.py`

Customer feedback and technician rating management:
- Technician rating system (add, update, set ratings)
- Job-specific technician performance tracking
- Standard rating levels (excellent, good, average, poor, very poor)
- Batch rating operations for multiple technicians
- Customer satisfaction tracking

**Use cases**: Performance management, customer satisfaction tracking, technician evaluation, quality assurance

### 🔧 Equipment Systems Server (`servicetitan-equipment-systems`)
**File**: `servicetitan_equipment_systems.py`

Installed equipment lifecycle management:
- Equipment CRUD operations (create, read, update, delete)
- Warranty tracking (manufacturer & service provider)
- Location-based equipment management
- Serial number and barcode tracking
- Attachment management for equipment documentation
- Advanced search capabilities (by location, manufacturer, serial number)
- Warranty status analysis and expiration tracking
- Equipment replacement predictions and planning
- Export functionality for external system integration

**Use cases**: Asset management, warranty tracking, maintenance planning, equipment audits, replacement forecasting

### 📋 Forms Server (`servicetitan-forms`)
**File**: `servicetitan_forms.py`

Form and submission management with job attachment capabilities:
- Form retrieval with advanced filtering (conditional logic, triggers, status)
- Form submission management with comprehensive search
- Job attachment operations (create, retrieve, download)
- Owner type filtering (Job, Call, Customer, Location, Equipment, etc.)
- Status tracking (Started, Completed, Published, Unpublished)
- Date range filtering and pagination support

**Use cases**: Form management, data collection, job documentation, compliance tracking, submission analysis

### 📞 JBCE Server (`servicetitan-jbce`)
**File**: `servicetitan_jbce.py`

Job Booking and Call Entry management:
- Call reasons management and configuration
- Active/inactive reason filtering
- Lead identification tracking
- Creation and modification date filtering
- Sortable results by various fields

**Use cases**: Call center operations, booking workflows, lead management, reason code maintenance

### 📢 Marketing Server (`servicetitan-marketing`)
**File**: `servicetitan_marketing.py`

Comprehensive marketing campaign management:
- Campaign category management (CRUD operations)
- Campaign cost tracking and financial management
- Full marketing campaign lifecycle management
- Email suppression list management for compliance
- DNIS (phone number) tracking and attribution
- Source/medium tracking for campaign analytics
- Business unit integration

**Use cases**: Marketing campaign management, cost tracking, email compliance, attribution tracking, campaign analytics

### 📊 Marketing Ads Server (`servicetitan-marketing-ads`)
**File**: `servicetitan_marketing_ads.py`

Advanced advertising performance and attribution tracking:
- Attributed leads tracking with lead type filtering
- Capacity warnings for advertising awareness
- External call attribution management
- Performance data analysis with segmentation
- Job attribution tracking for ROI analysis
- Web booking attribution monitoring
- Web lead form attribution tracking

**Use cases**: Ad campaign performance analysis, lead attribution, ROI tracking, capacity management, digital marketing optimization

### 🎯 Marketing Reputation Server (`servicetitan-marketing-reputation`)
**File**: `servicetitan_marketing_reputation.py`

Reputation management and review analytics:
- Review platform management and configuration
- Reputation analytics and scoring
- Review response management
- Brand monitoring capabilities
- Sentiment analysis and tracking

**Use cases**: Online reputation management, review monitoring, brand analysis, customer sentiment tracking

### 👤 Memberships Server (`servicetitan-memberships`)
**File**: `servicetitan_memberships.py`

Customer membership program management:
- Membership type configuration and management
- Member enrollment and lifecycle tracking
- Benefits and pricing tier management
- Renewal and billing automation
- Member analytics and reporting

**Use cases**: Membership program administration, customer retention, recurring revenue management

### 💼 Payroll Server (`servicetitan-payroll`)
**File**: `servicetitan_payroll.py`

Comprehensive payroll management system:
- **Payroll Operations**: Complete payroll lifecycle (get payrolls, activity codes, timesheet codes)
- **Gross Pay Items**: CRUD operations for employee compensation items
- **Payroll Adjustments**: Create, retrieve, and update payroll adjustments
- **Job Timesheets**: Manage technician time tracking and job-based timesheets
- **Employee Settings**: Configure payroll settings for employees and technicians
- **Export Operations**: Bulk export of job splits, payroll adjustments, timesheets, activity codes, non-job timesheets, gross pay items, and timesheet codes
- **Time Tracking**: Detailed time management with job association and labor tracking

**Use cases**: Payroll processing, time tracking, compensation management, labor cost analysis, timesheet management

### 📈 Reporting Server (`servicetitan-reporting`)
**File**: `servicetitan_reporting.py`

Business intelligence and analytics platform:
- **Dynamic Value Sets**: Retrieve configurable value sets for reports
- **Report Categories**: Browse and manage report organization structure
- **Report Management**: Access reports within categories with filtering
- **Report Descriptions**: Get detailed metadata and parameter information
- **Report Data**: Execute reports and retrieve formatted data with pagination
- **Custom Parameters**: Support for dynamic report parameters and filters

**Use cases**: Business analytics, performance reporting, data visualization, executive dashboards, KPI tracking

### 💰 Sales & Estimates Server (`servicetitan-sales`)
**File**: `servicetitan_sales.py`

Complete sales and estimation workflow:
- **Estimate Management**: Full CRUD operations for estimates with comprehensive filtering
- **Estimate Items**: Add, retrieve, and delete line items from estimates
- **Status Operations**: Send estimates to customers, convert to jobs, mark as sold
- **Export Operations**: Bulk export functionality with continuation tokens
- **Business Integration**: Link estimates to business units and track conversion rates
- **Workflow Management**: Handle estimate lifecycle from creation to completion

**Use cases**: Sales process management, estimate creation, quote-to-job conversion, sales analytics, pricing management

### 📋 Service Agreements Server (`servicetitan-service-agreements`)
**File**: `servicetitan_service_agreements.py`

Service contract and agreement management:
- **Service Agreement Operations**: Retrieve individual agreements with full details
- **Query Operations**: Advanced filtering by customer, location, status, dates
- **Export Operations**: Bulk export with continuation token support for large datasets
- **Contract Management**: Track agreement terms, pricing, and service schedules

**Use cases**: Service contract management, maintenance agreements, recurring service tracking, contract analytics

### 📅 Scheduling Pro Server (`servicetitan-scheduling-pro`)
**File**: `servicetitan_scheduling_pro.py`

Advanced scheduling optimization and routing:
- **Router Operations**: Manage routing sessions and performance analytics
- **Scheduler Operations**: List schedulers, manage sessions, track performance metrics
- **Performance Analytics**: Monitor scheduling efficiency and optimization results
- **Session Management**: Track routing and scheduling session data
- **Date Filtering**: Query operations with comprehensive date range support

**Use cases**: Route optimization, scheduling analytics, dispatcher performance, efficiency tracking

### ⚙️ Settings Server (`servicetitan-settings`)
**File**: `servicetitan_settings.py`

System configuration and user management:
- **Employee Management**: Full CRUD operations, account actions (activate/deactivate), bulk export
- **Technician Management**: Comprehensive technician lifecycle with account management
- **User Role Management**: Configure and assign user permissions and roles
- **Business Unit Management**: Manage organizational structure with external data support
- **Tag Type Management**: Configure and organize tag systems for categorization
- **Security Operations**: User account control and access management

**Use cases**: User administration, organizational setup, security management, system configuration

### 📋 Task Management Server (`servicetitan-task-management`)
**File**: `servicetitan_task_management.py`

Comprehensive task and workflow management:
- **Reference Data**: Access employees, business units, priorities, types, statuses, and categories
- **Task Operations**: Create, retrieve, update tasks with extensive filtering (25+ parameters)
- **Subtask Management**: Handle hierarchical task structures and dependencies
- **Rich Task Data**: Include comments, attachments, assignments, and progress tracking
- **Advanced Filtering**: Search by assignee, creator, priority, status, dates, business unit, and more

**Use cases**: Project management, workflow automation, task tracking, team coordination, process management

### 📞 Telecom Server (`servicetitan-telecom`)
**File**: `servicetitan_telecom.py`

Communication and call management system:
- **Call Management**: Access call logs with v3 and v2 API support
- **Opt-in/Opt-out Management**: Handle customer communication preferences with E.164 format
- **Media Access**: Retrieve call recordings and voicemails as binary data
- **Bulk Export Operations**: Export large datasets with continuation tokens
- **Call Analytics**: Comprehensive call filtering, agent tracking, and performance metrics
- **Communication Compliance**: Manage customer communication preferences and regulations

**Use cases**: Call center operations, communication compliance, call analytics, agent performance, customer preferences

### ⏰ Timesheets Server (`servicetitan-timesheets`)
**File**: `servicetitan_timesheets.py`

Time tracking and labor management:
- **Activity Management**: Track time activities with detailed job association
- **Activity Categories**: Organize and manage time tracking categories
- **Activity Types**: Configure different types of trackable activities
- **Bulk Export Operations**: Export timesheet data for payroll and analysis
- **Rich Activity Data**: Include job association, labor management, and tag support
- **Time Analytics**: Comprehensive time tracking with filtering and reporting

**Use cases**: Time tracking, labor management, payroll integration, productivity analysis, project time allocation

## Setup

### 1. Prerequisites

- Python 3.8 or higher
- ServiceTitan API access credentials
- Git (for cloning the repository)

### 2. Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/buildwithbeacon/servicetitan-mcp.git
   cd servicetitan-mcp
   ```

2. **Install Dependencies**:
   
   **Option A: Using pip (traditional)**:
   ```bash
   pip install -r requirements.txt
   ```
   
   **Option B: Using uv (recommended - faster and more reliable)**:
   ```bash
   uv sync
   # or if you don't have a pyproject.toml yet:
   uv pip install -r requirements.txt
   ```

3. **Environment Configuration**:
   Copy the example environment file and configure your credentials:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` with your ServiceTitan credentials:
   ```env
   SERVICE_TITAN_CLIENT_ID=your_client_id_here
   SERVICE_TITAN_CLIENT_SECRET=your_client_secret_here
   SERVICE_TITAN_APP_KEY=your_app_key_here
   SERVICE_TITAN_TENANT_ID=your_tenant_id_here
   ```

### 3. Claude Desktop Configuration

1. **Copy the MCP Configuration**:
   Use the provided configuration template or merge with your existing configuration:
   - `claude_desktop_config.json` - For standard Python execution
   - `claude_desktop_config_uv.json` - For uv execution (recommended)

2. **Configure Individual Servers**:
   Edit your Claude Desktop configuration file (typically at `~/.claude/claude_desktop_config.json`) to include the servers you need:

   **Option A: Using python directly**:
   ```json
   {
     "mcpServers": {
       "servicetitan-core": {
         "command": "python",
         "args": ["/path/to/servicetitan-mcp/servicetitan_core.py"],
         "env": {}
       },
       "servicetitan-accounting": {
         "command": "python", 
         "args": ["/path/to/servicetitan-mcp/servicetitan_accounting.py"],
         "env": {}
       }
     }
   }
   ```

   **Option B: Using uv run (recommended)**:
   ```json
   {
     "mcpServers": {
       "servicetitan-core": {
         "command": "uv",
         "args": ["run", "python", "/path/to/servicetitan-mcp/servicetitan_core.py"],
         "env": {}
       },
       "servicetitan-accounting": {
         "command": "uv",
         "args": ["run", "python", "/path/to/servicetitan-mcp/servicetitan_accounting.py"], 
         "env": {}
       }
     }
   }
   ```

### 4. Running Individual Servers

For testing or development, you can run servers individually:

**Using python directly**:
```bash
# Core functionality
python servicetitan_core.py

# Accounting operations
python servicetitan_accounting.py

# Customer interactions
python servicetitan_customer_interactions.py

# Equipment systems
python servicetitan_equipment_systems.py

# And so on for other servers...
```

**Using uv run (recommended)**:
```bash
# Core functionality
uv run python servicetitan_core.py

# Accounting operations
uv run python servicetitan_accounting.py

# Customer interactions
uv run python servicetitan_customer_interactions.py

# Equipment systems
uv run python servicetitan_equipment_systems.py

# And so on for other servers...
```

## Usage Patterns

### Single Domain Focus
Use one server when working on specific domain tasks:
- **Customer service workflows** → `servicetitan-core`
- **Catalog updates** → `servicetitan-pricebook`  
- **Purchase order processing** → `servicetitan-inventory`
- **Payroll processing** → `servicetitan-payroll`
- **Time tracking** → `servicetitan-timesheets`

### Multi-Domain Operations
For complex workflows spanning multiple domains, configure multiple servers simultaneously in your MCP client:
- **Complete job workflow**: Core + JPM + Dispatch + Timesheets
- **Financial operations**: Accounting + Payroll + Sales
- **Customer management**: Core + CRM + Customer Interactions + Marketing

### Context Window Optimization
Each server contains focused tools instead of 100+ tools, improving:
- AI context understanding
- Response accuracy
- Performance
- Reduced token usage

## Comprehensive Tool Reference

### Core Server Tools (7 tools)
- `get_customer_by_id` - Retrieve specific customer details
- `get_customers` - List customers with filtering
- `summarize_calls` - AI-powered call analysis
- `get_appointments` - Retrieve appointment data
- `create_appointment` - Schedule new appointments
- `update_appointment` - Modify existing appointments
- `cancel_appointment` - Cancel appointments

### Pricebook Server Tools (25+ tools)
**Materials Management:**
- `get_materials`, `create_material`, `update_material`, `delete_material`
- `get_material_by_id`, `get_material_images`, `upload_material_image`

**Services Management:**
- `get_services`, `create_service`, `update_service`, `delete_service`
- `get_service_by_id`

**Equipment Management:**
- `get_equipment`, `create_equipment`, `update_equipment`, `delete_equipment`
- `get_equipment_by_id`

**Categories & Organization:**
- `get_categories`, `create_category`, `update_category`, `delete_category`
- `get_discounts_and_fees`, `create_discount_fee`, `update_discount_fee`

### Inventory Server Tools (20+ tools)
**Inventory Management:**
- `get_inventory_adjustments`, `create_inventory_adjustment`, `update_inventory_adjustment`
- `get_purchase_orders`, `create_purchase_order`, `update_purchase_order`
- `get_inventory_receipts`, `create_inventory_receipt`, `update_inventory_receipt`
- `get_inventory_returns`, `create_inventory_return`, `update_inventory_return`
- `get_inventory_transfers`, `create_inventory_transfer`

**Vendor & Warehouse:**
- `get_vendors`, `create_vendor`, `update_vendor`
- `get_warehouses`, `get_trucks`

### Payroll Server Tools (34 tools)
**Core Payroll Operations:**
- `get_payrolls` - Retrieve payroll information with filtering
- `get_activity_codes` - Get payroll activity codes
- `get_timesheet_codes` - Retrieve timesheet codes

**Gross Pay Management:**
- `get_gross_pay_items`, `create_gross_pay_item`, `update_gross_pay_item`, `delete_gross_pay_item`

**Payroll Adjustments:**
- `get_payroll_adjustments`, `create_payroll_adjustment`, `update_payroll_adjustment`

**Job Timesheets:**
- `get_job_timesheets`, `create_job_timesheet`, `update_job_timesheet`, `delete_job_timesheet`

**Employee Settings:**
- `get_employee_payroll_settings`, `update_employee_payroll_settings`
- `get_technician_payroll_settings`, `update_technician_payroll_settings`

**Export Operations (7 tools):**
- `export_job_splits`, `export_payroll_adjustments`, `export_timesheets`
- `export_activity_codes`, `export_non_job_timesheets`, `export_gross_pay_items`, `export_timesheet_codes`

### Reporting Server Tools (5 tools)
- `get_dynamic_value_sets` - Retrieve configurable report value sets
- `get_report_categories` - Browse report organization structure
- `get_reports_in_category` - Access reports within specific categories
- `get_report_description` - Get detailed report metadata and parameters
- `get_report_data` - Execute reports and retrieve formatted data

### Sales & Estimates Server Tools (12 tools)
**Estimate Management:**
- `get_estimates` - List estimates with comprehensive filtering
- `get_estimate_by_id` - Retrieve specific estimate details
- `create_estimate` - Create new estimates
- `update_estimate` - Modify existing estimates

**Estimate Items:**
- `get_estimate_items` - Retrieve estimate line items
- `add_estimate_item` - Add items to estimates
- `delete_estimate_item` - Remove items from estimates

**Status Operations:**
- `send_estimate` - Send estimate to customer
- `convert_estimate_to_job` - Convert estimate to job
- `mark_estimate_as_sold` - Mark estimate as sold

**Export:**
- `export_estimates` - Bulk export estimates
- `export_estimate_items` - Bulk export estimate items

### Service Agreements Server Tools (3 tools)
- `get_service_agreements` - Query service agreements with filtering
- `get_service_agreement_by_id` - Retrieve specific agreement details
- `export_service_agreements` - Bulk export with continuation tokens

### Scheduling Pro Server Tools (5 tools)
**Router Operations:**
- `get_routers` - List available routers
- `get_router_sessions` - Retrieve router session data
- `get_router_performance` - Router performance analytics

**Scheduler Operations:**
- `get_schedulers` - List schedulers with filtering
- `get_scheduler_performance` - Scheduler performance metrics

### Settings Server Tools (21 tools)
**Employee Management:**
- `get_employees`, `create_employee`, `get_employee_by_id`, `update_employee`, `delete_employee`
- `activate_employee`, `deactivate_employee`, `export_employees`

**Technician Management:**
- `get_technicians`, `create_technician`, `get_technician_by_id`, `update_technician`, `delete_technician`
- `activate_technician`, `deactivate_technician`, `export_technicians`

**System Configuration:**
- `get_user_roles`, `get_business_units`, `create_business_unit`, `update_business_unit`
- `get_tag_types`, `create_tag_type`

### Task Management Server Tools (5 tools)
- `get_reference_data` - Access employees, business units, priorities, types, statuses, categories
- `get_tasks` - Retrieve tasks with extensive filtering (25+ parameters)
- `get_task_by_id` - Get specific task details
- `create_task` - Create new tasks
- `get_subtasks` - Retrieve subtasks for a parent task

### Telecom Server Tools (11 tools)
**Call Management:**
- `get_calls_v3` - Retrieve calls using v3 API
- `get_calls_v2` - Retrieve calls using v2 API (legacy)

**Opt-in/Opt-out Management:**
- `opt_in_phone_number` - Add phone to communication list
- `opt_out_phone_number` - Remove phone from communication list
- `get_opt_ins` - Retrieve opt-in records
- `get_opt_outs` - Retrieve opt-out records

**Media Operations:**
- `get_call_recording` - Download call recordings as binary data
- `get_voicemail` - Download voicemails as binary data

**Export Operations:**
- `export_calls` - Bulk export call data
- `export_opt_ins` - Bulk export opt-in data
- `export_opt_outs` - Bulk export opt-out data

### Timesheets Server Tools (10 tools)
**Activity Management:**
- `get_activities` - Retrieve time activities with job association
- `create_activity` - Create new time tracking activities
- `get_activity_by_id` - Get specific activity details
- `update_activity` - Modify existing activities
- `delete_activity` - Remove activities

**Categories & Types:**
- `get_activity_categories` - Retrieve activity organization
- `get_activity_types` - Get types of trackable activities

**Export Operations:**
- `export_activities` - Bulk export activity data
- `export_activity_categories` - Export category structure
- `export_activity_types` - Export activity types

### JPM Server Tools (25+ tools)
**Job Management:**
- `get_job_by_id`, `create_job`, `update_job`, `cancel_job`, `complete_job`, `hold_job`

**Project Management:**
- `get_project_by_id`, `create_project`, `update_project`, `attach_job_to_project`, `detach_job_from_project`

**Appointment Management:**
- `get_appointment_by_id`, `create_appointment`, `reschedule_appointment`, `hold_appointment`

### CRM Server Tools (20+ tools)
**Enhanced Customer Management:**
- `get_customers`, `create_customer`, `update_customer` (with advanced filtering)

**Contact Management:**
- `get_contact_by_id`, `get_contacts`, `create_contact`, `update_contact`, `delete_contact`

**Lead Management:**
- `get_lead_by_id`, `get_leads`, `create_lead`, `update_lead`

### Dispatch Server Tools (20+ tools)
**Appointment Management:**
- `get_appointment_assignments`, `assign_technicians_to_appointment`, `unassign_technicians_from_appointment`

**Scheduling:**
- `get_arrival_windows`, `create_arrival_window`, `update_arrival_window`
- `get_business_hours`, `create_business_hours`
- `get_capacity` - scheduling optimization

**Team & Resource Management:**
- `get_teams`, `create_team`, `get_team_by_id`, `delete_team`
- `get_technician_shifts`, `create_technician_shift`, `update_technician_shift`

### Accounting Server Tools (25+ tools)
**Accounts Payable:**
- `get_ap_credits`, `mark_ap_credits_as_exported`
- `get_ap_payments`, `mark_ap_payments_as_exported`

**General Ledger:**
- `get_gl_accounts`, `create_gl_account`, `update_gl_account`
- `get_gl_account_types`

**Invoicing:**
- `get_invoices`, `create_adjustment_invoice`, `update_invoice`
- `update_invoice_items`, `delete_invoice_item`

### Customer Interactions Server Tools (10 tools)
**Rating System:**
- `add_or_update_technician_rating`, `set_technician_rating`, `update_technician_rating`

**Standard Ratings:**
- `rate_technician_excellent`, `rate_technician_good`, `rate_technician_average`, `rate_technician_poor`, `rate_technician_very_poor`

### Equipment Systems Server Tools (10+ tools)
**Equipment Management:**
- `get_installed_equipment`, `get_installed_equipment_by_id`, `create_installed_equipment`, `update_installed_equipment`

**Advanced Operations:**
- `search_equipment_by_location`, `search_equipment_by_manufacturer`, `get_equipment_warranty_status`

### Forms Server Tools (5 tools)
- `get_forms` - Retrieve forms with advanced filtering
- `get_form_submissions` - Comprehensive submission search
- `create_job_attachment`, `get_job_attachments`, `download_job_attachment`

### JBCE Server Tools (1 tool)
- `get_call_reasons` - Call reason management and configuration

### Marketing Server Tools (15+ tools)
**Campaign Management:**
- `get_campaigns`, `create_campaign`, `update_campaign`
- `get_campaign_costs`, `create_cost`, `update_cost`

**Categories & Organization:**
- `get_categories`, `create_category`, `update_category`

**Compliance:**
- `get_suppressions`, `suppress_emails`, `unsuppress_emails`

### Marketing Ads Server Tools (7 tools)
**Attribution Tracking:**
- `get_attributed_leads` - Lead tracking with filtering
- `create_external_call_attribution` - External call tracking
- `create_job_attribution` - Job ROI tracking
- `create_web_booking_attribution` - Web booking tracking
- `create_web_lead_form_attribution` - Form attribution

**Performance Analytics:**
- `get_performance` - Performance analytics with segmentation
- `get_capacity_warnings` - Advertising capacity awareness

## API Authentication

All servers use OAuth 2.0 client credentials flow for authentication. The authentication is handled automatically using your configured environment variables:

- `SERVICE_TITAN_CLIENT_ID` - Your ServiceTitan application client ID
- `SERVICE_TITAN_CLIENT_SECRET` - Your ServiceTitan application client secret  
- `SERVICE_TITAN_APP_KEY` - Your ServiceTitan application key
- `SERVICE_TITAN_TENANT_ID` - Your ServiceTitan tenant ID

## Error Handling

All servers include comprehensive error handling:
- **Authentication Errors**: Automatic token refresh and retry
- **Rate Limiting**: Intelligent backoff and retry mechanisms
- **Network Errors**: Connection timeout and retry logic
- **API Errors**: Detailed error messages with context

## Performance Considerations

### Server Selection Strategy
- **Light Operations**: Use Core server for basic customer lookups
- **Complex Workflows**: Use multiple specialized servers
- **Bulk Operations**: Use servers with export capabilities (Accounting, Payroll, etc.)

### Pagination Support
Most list operations support pagination:
- **Page Size**: Configurable (typically 50-500 items)
- **Continuation Tokens**: For large datasets (especially exports)
- **Total Count**: Available in most responses

### Caching
- **Authentication Tokens**: Automatically cached and refreshed
- **Reference Data**: Consider caching frequently accessed data like business units, employees

## Benefits

### 🎯 **Focused Functionality**
Each server provides deep functionality in its domain without distraction from unrelated tools.

### 🚀 **Improved Performance**
Smaller tool sets mean faster processing and more accurate AI responses.

### 🔄 **Scalable Architecture**
Easy to add new domains without bloating existing servers.

### 🛠️ **Maintainable Code**
Clear separation of concerns makes updates and debugging simpler.

### 💾 **Reduced Context Usage**
Smaller tool sets use less context window, allowing for more complex conversations.


## Troubleshooting

### Common Issues

**"Missing required ServiceTitan environment variables"**
- Ensure your `.env` file exists and contains all required variables
- Check that variable names match exactly (case-sensitive)

**"Transport closed unexpectedly"**
- Verify the server script runs without syntax errors
- Check that all dependencies are installed (`pip install -r requirements.txt`)
- Ensure the path in Claude Desktop config is correct

**"Authentication failed"**
- Verify your ServiceTitan API credentials are correct
- Check that your ServiceTitan app has the necessary permissions
- Ensure your tenant ID is correct

**"Tool not found"**
- Verify you're using the correct server for the desired functionality
- Check that the server is properly configured in Claude Desktop
- Ensure the server started successfully (check logs)

### Debug Mode
Set environment variable `DEBUG=true` to enable verbose logging:
```bash
export DEBUG=true
python servicetitan_accounting.py
# or with uv:
uv run python servicetitan_accounting.py
```

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review ServiceTitan API documentation
3. Open an issue on GitHub with detailed error messages and steps to reproduce

## Acknowledgments

Built using:
- [FastMCP](https://github.com/modelcontextprotocol/python-sdk) - Model Context Protocol Python SDK
- [httpx](https://www.python-httpx.org/) - HTTP client for Python
- [python-dotenv](https://pypi.org/project/python-dotenv/) - Environment variable management
- ServiceTitan API v2 - Field service management platform 
