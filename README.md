# Q-STAR (v2.0.0)

### QR-Based Student and Teacher Attendance Recorder

Q-STAR is a production-grade, offline-first desktop application designed for educational institutions operating in low-connectivity environments. Built using a modular, stateless backend architecture inspired by NestJS and paired with a modern Vanilla JS Single Page Application (SPA) frontend, Q-STAR provides secure, high-throughput attendance logging using native hardware QR scanning.

---

## 👥 Authors & Core Contributors

- **Raphael Khandie B. Bihag** — Core Backend Architect & System Engineer
- **Ray Emanuele P. Untal** — DevOps, Frontend Integration & Deployment Engineer

---

## 🏗️ Architectural Overview

Q-STAR uses a strict separation of concerns, decoupling application logic from persistent data states to ensure seamless remote updates without risking historical data loss.

```text
C:/QSTAR/
├── Data/                             <-- Persistent Storage (Untouched during updates)
│   ├── logs/
│   │   └── app_errors.log            <-- Rotating automated crash logs
│   ├── attendance.db                 <-- Normalized SQLite database
│   └── config.json                   <-- App configurations & scrypt-hashed credentials
└── Application/                      <-- Application Binary (Overwritten on update)
    ├── QSTAR_Engine.exe              <-- Main Executable
    ├── version.json                  <-- Semantic version tracking
    ├── core/                         <-- Core system dependencies
    ├── modules/                      <-- Feature-bounded domain modules
    └── web/                          <-- Vanilla JS SPA Frontend Web Component Layer

    Key Technical Overhauls (v1.0 vs v2.0)

    Framework Migration: Replaced the legacy, unmaintained Eel package with pywebview utilizing native OS WebView2 (Chromium) runtimes.

    Database Normalization: Migrated from a single flat-file structure to a fully normalized Relational DB schema tracking student, faculty, and centralized attendance pools with SQL Foreign Keys.

    Cryptographic Hashing: Upgraded administrative entry authentication from plain-text storage to standard scrypt key derivation functions.

    Robust Error Logging: Implemented standard Python RotatingFileHandler logic capped at 5MB boundaries with chronological append persistence to prevent data bloat.

⚙️ Core Engineering Design Patterns
1. Backend Module Architecture

The backend is split into decoupled, feature-bounded contexts (attendance, auth, dashboard, faculty, student, user). Each domain strictly adheres to the following layout:

    Controller: Exposes endpoints directly through the pywebview JS API gateway bridge.

    Service: Handles the underlying business logic, exceptions, and state modifications.

    Model: Emulates Data Transfer Objects (DTOs) ensuring type and validation consistency.

    Repository: Controls safe, transactional database operations using a shared client context.

2. Smart Parsing Identity Engine

Instead of brittle Regex patterns that fail when string parameter order shifts, v2.0 utilizes a deterministic structural validator:

    Purely Numeric Token Configurations: Automatically identified and treated as Students.

    Alphanumeric/Alpha Token Prefixes: Automatically identified and treated as Faculty/Staff.

    Junk/Vulgar Strings: Intercepted at the validation layer and safely skipped before parsing.

3. Asynchronous Auto-Updater (launcher.py)

At boot, the system performs a non-blocking check against the public GitHub Releases API. If a higher semantic version tag is found, the user is prompted through a custom UI modal. The launcher downloads the updated .exe bundle, overwrites the /Application execution scope, and hot-reboots the app seamlessly.
4. Frontend Native Web Components

The UI runs as an isolated Single Page Application (SPA). Views and layout segments are constructed via native web browser bindings using custom HTMLElement declarations. Responsive scale ratios are handled via declarative CSS clamp() utilities to ensure uniform UI scaling across legacy and high-definition client monitors.
🛠️ Local Development & Setup
Prerequisites

    Python 3.10+

    Native camera system or external USB QR capture hardware.

Installation

    Clone the repository into your workspace:
    Bash

    git clone [https://github.com/your-username/qstar-attendance.git](https://github.com/your-username/qstar-attendance.git)
    cd qstar-attendance

    Install system requirements:
    Bash

    pip install -r requirements.txt

    Ensure structural dependencies for QR scanning (pyzbar) are positioned correctly in the application root directory if building manually on Windows:

        libiconv.dll

        libzbar-64.dll

Running the Application

To run the local engine instance directly:
Bash

python main.py

To execute the system wrapper layer featuring active version checking:
Bash

python launcher.py

📦 Production Bundling (Creating the Executable)

To freeze the application layer into a portable standalone Windows executable bundle, execute PyInstaller using the following parameters:
Bash

pyinstaller --noconfirm --onedir --windowed --add-data "web/;web/" --add-data "version.jso
```
