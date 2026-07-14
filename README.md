# Q-STAR (v2)

### QR-Based Student and Teacher Attendance Recorder

Q-STAR is a production-grade, offline-first desktop application designed for educational institutions operating in low-connectivity environments. Built using a modular backend architecture inspired by NestJS principles and paired with a modern Vanilla JavaScript Single Page Application (SPA), Q-STAR provides secure, high-throughput attendance logging using native hardware QR scanning.

---

## 👥 Authors & Core Contributors

* **Ray Emanuele P. Untal** — Core Backend Architect & Security Engineer
* **Raphael Khandie B. Bihag** — Data Science & Frontend Integration Engineer

---

## 🏗️ Architectural Overview

Q-STAR follows a strict separation of concerns, isolating application logic from persistent data storage. This design enables application updates without risking historical attendance records, user configurations, or audit logs.

```text
C:/QSTAR/
├── Data/                             <-- Persistent Storage (Untouched during updates)
│   ├── logs                          <-- Rotating application logs                      
│   ├── attendance.db                 <-- Normalized SQLite database
│   └── config.json                   <-- Application configuration & scrypt-hashed credentials
│
└── Application/                      <-- Application Layer (Updated when new versions are installed)
    ├── launcher.py                   <-- Update checker and bootstrapper
    ├── main.py                       <-- Primary application entry point
    ├── version.json                  <-- Semantic version tracking
    ├── core/                         <-- Shared infrastructure components
    ├── modules/                      <-- Feature-bounded domain modules
    └── web/                          <-- Vanilla JS SPA frontend
```

---

## 🚀 Key Technical Overhauls (v1.0 → v2.0)

### Framework Migration

Migrated from the legacy Eel framework to pywebview, leveraging native operating system web rendering engines while maintaining a desktop-native experience.

### Database Normalization

Transitioned from a flat-file persistence model to a fully normalized SQLite relational schema supporting centralized student, faculty, and attendance records through foreign key relationships.

### Cryptographic Authentication

Administrative credentials are secured using the scrypt key derivation algorithm rather than plaintext storage.

### Robust Error Logging

Implemented automated rotating log management using Python's `RotatingFileHandler`, preventing uncontrolled log growth while preserving historical diagnostic information.

---

## ⚙️ Core Engineering Design Patterns

### 1. Modular Backend Architecture

The backend is divided into feature-bounded domains such as:

* Attendance
* Authentication
* Dashboard
* Faculty
* Student
* User Management

Each domain follows a structured architecture:

#### Controller

Exposes application functionality through the pywebview JavaScript bridge.

#### Service

Contains business logic, validation workflows, and application rules.

#### Model

Acts as a lightweight DTO-style layer for data validation and consistency.

#### Repository

Handles transactional database operations through a centralized database context.

---

### 2. Smart Parsing Identity Engine

Q-STAR v2.0 replaces fragile regular-expression-heavy parsing with a deterministic structural validation engine.

Supported identifiers follow a structured format:

```text
XX-YY-ZZ
```

The number of characters within each segment may vary, but the dash-separated structure is required.

Classification is performed using the contents of the identifier:

* Identifiers containing only numeric values are automatically classified as Students.
* Identifiers containing one or more alphabetic characters are automatically classified as Faculty or Staff.
* Malformed, invalid, or non-conforming values are intercepted during validation and safely ignored before processing.

This approach remains reliable regardless of segment lengths while reducing false positives caused by pattern-specific parsing.

---

### 3. Asynchronous Auto-Updater (`launcher.py`)

Upon startup, the launcher performs a check against the GitHub Releases API.

If a newer semantic version is available:

1. The user is notified through a custom application modal.
2. The updated application package is downloaded.
3. The application layer is replaced while preserving the data layer.
4. The system automatically relaunches into the updated version.

This process ensures seamless upgrades without affecting attendance records, logs, or application settings.

---

### 4. Frontend Native Web Components

The user interface operates as a Single Page Application (SPA) built using native browser technologies.

Views and reusable UI segments are implemented using custom `HTMLElement` components, providing modularity without introducing heavyweight frontend frameworks.

---

## 🛠️ Local Development & Setup

### Prerequisites

* Python 3.10+
* Compatible camera device
* Windows environment (recommended for production builds)

---

### Installation

#### Clone the Repository

```bash
git clone https://github.com/HorizUntall/QSTAR.git
cd qstar-attendance
```

#### Install Dependencies

```bash
pip install -r requirements.txt
```

#### Required Native Libraries

When running or building manually, ensure the following files are present:

```text
libiconv.dll
libzbar-64.dll
```

These libraries are required for QR code decoding through pyzbar.

---

## ▶️ Running the Application

### Run the Main Application

```bash
python main.py
```

### Run Through the Update Launcher

```bash
python launcher.py
```

The launcher should be used when testing version-checking and update workflows.

---

## 📦 Production Bundling (Auto Py to Exe)

Q-STAR uses **Auto Py to Exe** as the official packaging workflow.

Two separate executables are generated:

### 1. QSTAR_Engine.exe

This executable contains the primary application runtime and is generated from:

```text
main.py
```

#### Auto Py to Exe Settings

**Script Location**

```text
main.py
```

**Packaging Mode**

```text
One Directory
```

**Console Window**

```text
Window Based (Hide Console)
```

**Optional Icon**

```text
web/assets/images/
```

**Additional Files**

```text
web/
libiconv.dll
libzbar-64.dll
version.json
```

#### Generated Output

```text
QSTAR_Engine.exe
_internal/
```

---

### 2. launcher.exe

This executable is generated from:

```text
launcher.py
```

#### Auto Py to Exe Settings

**Script Location**

```text
launcher.py
```

**Packaging Mode**

```text
One File
```

**Console Window**

```text
Window Based (Hide Console)
```

**Optional Icon**

```text
web/assets/images/
```

---

### Final Production Layout

After both executables have been built, the launcher must be placed alongside the application runtime:

```text
launcher.exe
QSTAR_Engine.exe
_internal/
```

The naming and folder structure above are required because the launcher is responsible for detecting updates and launching the application runtime correctly.

---

## 🔒 Data Persistence Strategy

One of the primary design goals of Q-STAR is update-safe persistence.

Application updates only replace executable assets and application code while preserving:

* Attendance records
* User accounts
* Faculty records
* Student records
* Configuration files
* Historical logs

This ensures institutions can deploy updates without risking operational data loss.
