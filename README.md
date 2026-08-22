# 🎨 JankyPaint

JankyPaint is a lightweight Python-based digital painting and asset-creation application built as part of the Janky Content Creation System.

It provides basic painting tools, color controls, layers, and PNG export.

---

## 🚀 Getting Started

### Clone the Repository

```bash
git clone <repository-url>
cd JankyPaint
```

### Create a Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows:

```powershell
.venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
python main/jankyPaintApp.py
```

---

## 🤝 Collaborating

### 1. Get the Latest Changes

Before starting work:

```bash
git pull origin main
```

### 2. Create a Branch

Create a branch for your work:

```bash
git checkout -b feature/your-feature-name
```

Examples:

```bash
git checkout -b feature/layer-panel
git checkout -b feature/brush-improvements
git checkout -b fix/color-picker
```

### 3. Make Your Changes

Develop and test your changes locally.

Keep commits focused on one change where possible.

```bash
git add .
git commit -m "Add layer panel"
```

### 4. Push Your Branch

```bash
git push -u origin feature/your-feature-name
```

### 5. Open a Pull Request

Create a Pull Request from your branch into `main`.

Describe:

* What you changed
* Why you changed it
* Anything that still needs testing

After review, the branch can be merged into `main`.

---

## 🌿 Branching

Use `main` as the stable branch.

```text
main
 │
 ├── feature/layer-panel
 ├── feature/new-tool
 └── fix/color-picker
```

Avoid committing unfinished work directly to `main`.

---

## 📌 Quick Workflow

```bash
git pull origin main

git checkout -b feature/my-feature

# Make changes

git add .
git commit -m "Describe the change"

git push -u origin feature/my-feature
```

Then open a Pull Request into `main`.

---

## 📁 Project

```text
JankyPaint/
├── main/
├── src/
├── docs/
├── output/
└── README.md
```

JankyPaint is an active project, so the structure and features may change as development continues.
