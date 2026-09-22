# 🤖 AI Vendor Quotation & Negotiation Agent

A Windows desktop application that automates the vendor procurement
workflow --- from **RFQ creation and Outlook email distribution** to
**quotation collection, price comparison, negotiation, budget-based
stopping, and final Excel reporting**.

The project is built with **Python**, **Tkinter**, **Microsoft Outlook
COM Automation**, **Pandas**, and **OpenPyXL**.

------------------------------------------------------------------------

## 📌 Overview

A typical procurement cycle requires users to manually send RFQs,
monitor vendor responses, download quotations, compare prices, follow up
for revised commercial offers, and prepare a final comparison report.

**AI Vendor Quotation & Negotiation Agent** automates much of this
repetitive workflow in a single desktop application.

The application can:

-   Manage vendors and their email addresses.
-   Create an RFQ for a product or service requirement.
-   Send RFQs automatically through Microsoft Outlook.
-   Monitor Outlook for vendor quotation responses.
-   Read quotation prices from email bodies and supported attachments.
-   Rank quotations according to price.
-   Compare the lowest quotation with the entered budget.
-   Start negotiation when the lowest quotation is above budget.
-   Request higher-priced vendors to beat the current L1 price.
-   Continue monitoring revised vendor responses.
-   Stop automatically when the budget is achieved.
-   Allow the user to stop the procurement workflow manually.
-   Generate and open the final Excel comparison report.

------------------------------------------------------------------------

## ✨ Key Features

### 📧 Automated RFQ Distribution

The application creates an RFQ and sends it to configured vendors using
Microsoft Outlook.

The RFQ workflow includes:

-   Product
-   Quantity
-   Specification
-   Budget
-   Unique RFQ reference
-   Vendor-specific email distribution

------------------------------------------------------------------------

### 👥 Vendor Management

Vendors can be maintained directly from the desktop application.

The application stores details such as:

-   Vendor name
-   Vendor email address

The GUI also provides options to add vendors and clear the vendor list.

------------------------------------------------------------------------

### 📥 Outlook Inbox Monitoring

The application monitors Microsoft Outlook for emails associated with an
RFQ.

The Outlook monitor:

-   Checks recent inbox messages.
-   Identifies RFQ-related replies.
-   Processes unread quotation emails.
-   Handles vendor email identification.
-   Downloads supported quotation attachments.
-   Extracts prices from quotation emails.
-   Marks processed messages as read.

Microsoft Outlook integration is implemented through `win32com` /
`pywin32`.

------------------------------------------------------------------------

### 💬 Email Body Price Extraction

The application can detect quotation prices directly from vendor email
bodies.

Examples of supported formats include:

``` text
Unit Price: 198000
Quoted Price: 198000
Final Price: 198000
Price: ₹198,000
Rs. 198000
INR 198000
```

Regular expressions are used to identify supported price patterns.

------------------------------------------------------------------------

### 🧹 Reply-History Cleaning

Before extracting a price from an email body, the application removes
common reply-history sections.

This helps reduce the chance of an older price from a previous email in
the conversation being treated as the latest quotation.

------------------------------------------------------------------------

### 📎 Quotation Attachment Processing

The workflow supports quotation attachments including:

-   PDF
-   XLS
-   XLSX

Downloaded quotations are stored in the local `quotations` directory for
processing.

------------------------------------------------------------------------

### 📊 Automatic Quotation Ranking

Valid quotations are sorted by price.

Example:

  Rank   Vendor       Unit Price
  ------ ---------- ------------
  L1     Vendor C       ₹198,000
  L2     Vendor B       ₹199,000
  L3     Vendor A       ₹200,000

The quotation with the lowest valid price becomes the current **L1**.

------------------------------------------------------------------------

## 💰 Budget-Based Procurement Logic

After the initial quotation comparison, the application compares the
current lowest price with the budget entered by the user.

### Budget Already Achieved

If:

``` text
Lowest Price <= Budget
```

the application does not need to start negotiation.

It proceeds to the final reporting stage.

### Budget Not Achieved

If:

``` text
Lowest Price > Budget
```

the negotiation workflow begins.

------------------------------------------------------------------------

## 🤝 Automated Negotiation

The negotiation module reads the latest quotations and determines the
current L1 vendor.

Example:

``` text
Vendor A = ₹200,000
Vendor B = ₹199,000
Vendor C = ₹198,000
```

Current L1:

``` text
Vendor C = ₹198,000
```

The current negotiation logic skips the L1 vendor and sends negotiation
requests to the other configured vendors.

A target price is calculated below the current L1 price so that
participating vendors are requested to improve upon the best available
quotation.

------------------------------------------------------------------------

## 🔄 Revised Price Monitoring

After a negotiation request is sent, the application continues
monitoring Outlook for revised vendor quotations.

When a better price is received:

1.  The quotation data is refreshed.
2.  Vendor comparison is regenerated.
3.  The new lowest price is identified.
4.  The latest lowest price is logged.
5.  The budget condition is checked again.

This allows the application to react to revised quotations rather than
relying only on the initial vendor prices.

------------------------------------------------------------------------

## 🎯 Automatic Negotiation Stop

Negotiation can stop automatically when:

``` text
Current Lowest Price <= Budget
```

When the budget is achieved, the workflow proceeds to final report
generation.

This means the user does not have to manually stop procurement when an
acceptable price has already been received.

------------------------------------------------------------------------

## 🛑 Manual Stop

The desktop application also provides a:

``` text
Stop Procurement
```

button.

This is useful when the user decides that waiting for further
negotiation is no longer worthwhile.

The stop request ends the active monitoring/negotiation workflow after
the current operation and allows the application to proceed using the
latest available comparison.

------------------------------------------------------------------------

## 📈 Excel Comparison Report

The application generates an Excel quotation comparison report using the
latest available vendor quotations.

The report is intended to provide a concise commercial comparison
containing information such as:

-   Vendor
-   Unit price
-   Ranking / comparison information

The generated report can also be opened from the desktop application.

------------------------------------------------------------------------

## 🖥️ Desktop GUI

The application uses **Tkinter** for its graphical user interface.

Current GUI functions include:

-   Add Vendor
-   Clear Vendors
-   Enter Product
-   Enter Quantity
-   Enter Budget
-   Enter Specification
-   Start Procurement
-   Stop Procurement
-   View Live Status
-   Open Final Report

The procurement workflow runs in a background thread so the GUI can
remain available while procurement operations are running.

------------------------------------------------------------------------

## 🔁 End-to-End Workflow

``` text
┌─────────────────────────────┐
│       Start Procurement     │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│         Create RFQ          │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│    Send RFQ to Vendors      │
│    via Microsoft Outlook    │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│     Monitor Outlook Inbox   │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│    Collect Vendor Quotes    │
│ Email Body / PDF / Excel    │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│     Compare & Rank Quotes   │
└──────────────┬──────────────┘
               │
               ▼
        Is L1 <= Budget?
          /           \
        Yes            No
         │              │
         │              ▼
         │    ┌──────────────────────┐
         │    │ Start Negotiation    │
         │    └──────────┬───────────┘
         │               │
         │               ▼
         │    ┌──────────────────────┐
         │    │ Send Negotiation     │
         │    │ Mail to Eligible     │
         │    │ Vendors              │
         │    └──────────┬───────────┘
         │               │
         │               ▼
         │    ┌──────────────────────┐
         │    │ Monitor Revised      │
         │    │ Quotations           │
         │    └──────────┬───────────┘
         │               │
         │               ▼
         │        Budget Achieved?
         │           /       \
         │         Yes        No
         │          │          │
         │          │          └── Continue Monitoring
         │          │
         └──────────┴───────────────┐
                                    ▼
                       ┌────────────────────────┐
                       │ Generate Final Report  │
                       └────────────┬───────────┘
                                    │
                                    ▼
                       ┌────────────────────────┐
                       │ Procurement Completed  │
                       └────────────────────────┘
```

A manual stop is also available during the active procurement workflow.

------------------------------------------------------------------------

## 🏗️ Project Structure

``` text
project_charter/
│
├── Main.py
├── procurement_workflow.py
│
├── ai_negotiation_agent.py
├── negotiation_engine.py
├── negotiation_tracker.py
│
├── rfq_manager.py
├── outlook_sender.py
├── outlook_monitor.py
│
├── quotation_reader.py
├── pdf_parser.py
├── excel_parser.py
│
├── body_quotes.py
├── body_quotes.json
├── data_manager.py
│
├── dashboard.py
├── Vendor_agent.py
├── test_outlook.py
│
├── reports/
│   ├── comparison_generator.py
│   ├── excel_report.py
│   └── pdf_report.py
│
├── data/
├── quotations/
│
└── main.spec
```

> The exact contents of runtime-generated folders may vary depending on
> the current build and execution state.

------------------------------------------------------------------------

## 🧩 Main Modules

  -----------------------------------------------------------------------
  Module                              Responsibility
  ----------------------------------- -----------------------------------
  `Main.py`                           Tkinter GUI and user controls

  `procurement_workflow.py`           End-to-end procurement
                                      orchestration

  `rfq_manager.py`                    RFQ creation

  `outlook_sender.py`                 RFQ and negotiation email sending

  `outlook_monitor.py`                Outlook inbox monitoring and
                                      quotation detection

  `quotation_reader.py`               Reads available quotation data

  `pdf_parser.py`                     Processes supported PDF quotations

  `excel_parser.py`                   Processes supported Excel
                                      quotations

  `body_quotes.py`                    Stores/manages prices extracted
                                      from email bodies

  `negotiation_engine.py`             Quote ranking and
                                      negotiation-related logic

  `ai_negotiation_agent.py`           Executes vendor negotiation
                                      workflow

  `negotiation_tracker.py`            Negotiation tracking support

  `data_manager.py`                   Vendor/application data management

  `reports/comparison_generator.py`   Generates quotation comparison data

  `reports/excel_report.py`           Generates Excel reports

  `reports/pdf_report.py`             PDF reporting support

  `main.spec`                         PyInstaller build specification
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## 🛠️ Technology Stack

  Technology            Usage
  --------------------- -------------------------------------------
  Python                Core application
  Tkinter               Desktop GUI
  Microsoft Outlook     Vendor communication
  pywin32 / win32com    Outlook COM automation
  pythoncom             COM initialization for Outlook automation
  Pandas                Quotation data processing
  OpenPyXL              Excel report generation
  Regular Expressions   Email-body price extraction
  Threading             Background procurement execution
  PyInstaller           Windows executable packaging

------------------------------------------------------------------------

## 💻 System Requirements

The current version is designed for Windows.

Recommended environment:

-   Windows 10 or Windows 11
-   Microsoft Outlook Desktop
-   A configured Outlook mailbox
-   Microsoft Excel or another compatible application for viewing
    generated `.xlsx` reports

For source-code execution:

-   Python 3.x
-   Required Python dependencies

> The current email integration depends on Microsoft Outlook COM
> automation and therefore is Windows/Outlook dependent.

------------------------------------------------------------------------

## ⚙️ Installation for Development

### 1. Clone the repository

``` bash
git clone <YOUR-GITHUB-REPOSITORY-URL>
```

### 2. Open the project directory

``` powershell
cd "<PROJECT-PATH>\project_charter"
```

### 3. Create a virtual environment

``` powershell
python -m venv .venv
```

### 4. Activate the environment

PowerShell:

``` powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

Install the packages required by your current project environment.

Core dependencies include packages such as:

``` powershell
pip install pywin32 pandas openpyxl
```

Install any additional PDF-processing dependency used by `pdf_parser.py`
if required by the current implementation.

------------------------------------------------------------------------

## ▶️ Running the Application

From the project directory:

``` powershell
python Main.py
```

The desktop application should open.

------------------------------------------------------------------------

## 🧪 Basic Usage

1.  Start Microsoft Outlook and make sure the required mailbox is
    configured.
2.  Launch the Vendor Negotiator application.
3.  Add the required vendors.
4.  Enter product, quantity, budget, and specification.
5.  Click **Start Procurement**.
6.  The application creates and sends the RFQ.
7.  It monitors Outlook for vendor quotations.
8.  Once quotations are available, the application compares prices.
9.  If the budget has already been achieved, negotiation is skipped.
10. Otherwise, negotiation begins.
11. Revised quotations are monitored.
12. The workflow stops automatically when the budget is achieved, or the
    user can select **Stop Procurement**.
13. The final Excel report is generated and can be opened from the
    application.

------------------------------------------------------------------------

## 📦 Building the Windows Application

The project can be packaged using **PyInstaller**.

Install PyInstaller:

``` powershell
pip install pyinstaller
```

A basic directory-based build can be created with:

``` powershell
pyinstaller --onedir --windowed Main.py
```

If the repository contains the configured `main.spec`, the application
can instead be built with:

``` powershell
pyinstaller main.spec
```

The resulting build will normally be available under:

``` text
dist/
```

------------------------------------------------------------------------

## 🖥️ Distribution Notes

A PyInstaller build bundles the Python runtime and required packaged
Python dependencies, so the recipient does not normally need to install
Python or manually run `pip install`.

However, the current application still relies on:

-   Windows
-   Microsoft Outlook Desktop
-   A configured Outlook mailbox
-   Access required to send and receive vendor emails

Always test the packaged application on a separate Windows machine
before production distribution.

------------------------------------------------------------------------

## ⚠️ Outlook COM & Threading

The procurement workflow runs in a background thread.

Microsoft Outlook automation through `win32com` requires COM
initialization in threads that interact with Outlook.

Functions that access Outlook should therefore initialize and release
COM appropriately, for example with:

``` python
pythoncom.CoInitialize()

try:
    # Outlook COM operations
    pass
finally:
    pythoncom.CoUninitialize()
```

This is particularly important for avoiding errors such as:

``` text
CoInitialize has not been called.
```

------------------------------------------------------------------------

## 🔒 Security & Repository Hygiene

If this repository is made public, **do not commit real procurement or
company data**.

Avoid publishing:

-   Real vendor email addresses
-   Confidential quotations
-   Commercial pricing
-   Company procurement records
-   Credentials
-   Passwords
-   API keys
-   Private email content
-   Generated reports containing business data

Use dummy/demo vendor information for screenshots and public testing.

------------------------------------------------------------------------

## 🙈 Recommended `.gitignore`

A repository for this project should normally exclude local
environments, build artifacts, runtime quotation files, and confidential
generated data.

Example:

``` gitignore
# Python
__pycache__/
*.py[cod]
*.pyo

# Virtual environments
.venv/
venv/

# PyInstaller
build/
dist/

# Runtime quotations
quotations/*
!quotations/.gitkeep

# Generated reports
reports/*.xlsx
reports/*.pdf

# Runtime / private data
body_quotes.json

# Logs
*.log
logs/

# IDE / OS
.vscode/
.idea/
.DS_Store
Thumbs.db
```

Review the ignore rules against your actual project before publishing.

------------------------------------------------------------------------

## ⚠️ Current Limitations

The current version is primarily designed as a local Windows desktop
application.

Current architectural limitations include:

-   Outlook Desktop dependency
-   Windows-specific COM integration
-   Local desktop GUI
-   Local/runtime data storage
-   Price-focused vendor comparison
-   No central multi-user database
-   No browser-based interface
-   No native cloud email integration

These are suitable areas for future versions of the project.

------------------------------------------------------------------------

## 🚀 Future Roadmap

Potential future enhancements include:

-   Persistent multi-round negotiation sessions
-   Vendor response deadlines
-   Automatic reminder emails
-   Negotiation history
-   Vendor performance analytics
-   Historical procurement price analysis
-   Advanced AI-assisted negotiation strategies
-   Executive procurement dashboard
-   SQL database integration
-   Authentication and role-based access
-   Centralized configuration
-   PDF executive reports
-   Cloud deployment
-   Web-based interface
-   API-based email integration
-   Multi-user procurement workflows
-   Containerized backend components

------------------------------------------------------------------------

## 🎯 Project Objective

The goal of this project is to demonstrate how Python automation can
reduce repetitive procurement activities and create a structured
workflow around vendor communication and quotation comparison.

The project combines:

``` text
Procurement Automation
        +
Microsoft Outlook Integration
        +
Quotation Processing
        +
Vendor Price Comparison
        +
Negotiation Automation
        +
Budget-Based Decision Logic
        +
Automated Reporting
```

into one Windows desktop application.

------------------------------------------------------------------------

## 👨‍💻 Author

**Prashant**

IT Infrastructure \| Cloud \| DevOps \| Automation \| AI/GenAI

------------------------------------------------------------------------

## 📌 Version

**v1.0**

Initial desktop release of the **AI Vendor Quotation & Negotiation
Agent**.

------------------------------------------------------------------------

## ⭐ Repository

If you find this project useful, consider starring the repository.

Contributions, suggestions, and improvement ideas are welcome.
