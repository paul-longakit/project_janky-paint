# 🎨 JankyPaint

**JankyPaint** is a lightweight Python-based digital painting and asset-creation application built as part of my personal **Janky Content Creation System**.

The goal is simple:

> Build a small painting tool from scratch while experimenting with clean software architecture, drawing systems, reusable components, and practical content pipelines.

> **"Janky, but built properly."** 🛠️

---

## ✨ Current Features

* 🖌️ **Brush Tool** — Draw directly onto the canvas
* 🧼 **Eraser Tool** — Remove painted areas
* 🪣 **Paint Bucket / Fill Tool** — Fill connected areas with color
* 🎨 **Color Picker** — Select colors directly from the canvas
* 🌈 **HSL Controls** — Adjust hue, saturation, and lightness
* 🔴 **RGB Controls** — Work with individual red, green, and blue values
* #️⃣ **HEX Input** — Enter colors using hexadecimal values
* 📏 **Adjustable Brush Size** — Control brush diameter
* 🗂️ **Layer Support** — Organize artwork using layers
* 💾 **PNG Export** — Export finished artwork as PNG images
* 🧩 **Painting Operations** — Reusable operations for modifying the canvas
* 🏗️ **Clean Architecture-Inspired Structure** — Separation between domain, application, infrastructure, and presentation concerns

---

## 🏗️ Architecture

JankyPaint is organized around a **Clean Architecture-inspired design**.

The project separates the core painting logic from UI concerns, rendering, and persistence. This makes the application easier to experiment with and allows individual parts of the painting system to evolve independently.

```text
JankyPaint
│
├── domain/
│   ├── entities/
│   └── value_objects/
│
├── application/
│   └── use_cases/
│
├── infrastructure/
│   ├── rendering/
│   └── persistence/
│
└── presentation/
    └── editor/
```

### Domain

Contains the core concepts and rules of the painting system.

This layer should remain independent from GUI frameworks and other external implementation details.

### Application

Contains the use cases that coordinate domain operations.

Examples include painting operations, editing actions, and other workflows performed by the application.

### Infrastructure

Contains implementations that interact with external systems.

This includes rendering, image handling, persistence, and other technical details.

### Presentation

Contains the user-facing editor and GUI functionality.

The presentation layer communicates with the application layer rather than owning the core painting logic.

---

## 🎯 Project Goals

JankyPaint is primarily an **engineering and learning project**.

The main goals are:

1. Build a functional painting application from scratch.
2. Experiment with software architecture in a real project.
3. Keep the core painting logic independent from the GUI.
4. Develop reusable drawing and image-processing operations.
5. Create a foundation that can eventually support a larger asset-creation pipeline.
6. Learn by actually building rather than attempting to design everything perfectly beforehand.

The project intentionally favors **small, understandable components** over unnecessary complexity.

---

## 🧩 Design Philosophy

JankyPaint follows a few simple principles:

### Keep the core independent

Painting logic should not depend directly on the GUI.

### Prefer small components

A brush, layer, fill operation, color value, or rendering component should have a focused responsibility.

### Separate "what" from "how"

The application layer describes **what the user wants to do**, while infrastructure handles **how that operation is technically performed**.

### Build incrementally

JankyPaint is not intended to be a perfect framework from day one.

Features are added as the project grows, and the architecture evolves alongside the actual needs of the application.

---

## 🚧 Project Status

JankyPaint is an **active personal project**.

The application is functional, but the architecture and feature set are still evolving.

Expect:

* Experimental components
* Refactoring
* Architecture changes
* New painting tools
* Improvements to the editor
* Occasional jankiness

That's part of the project.

---

## 🛠️ Philosophy

JankyPaint is built around one idea:

> **Don't wait until you know everything. Build the thing, learn from it, then build it better.**

It's a small painting application, but the larger goal is to use it as a practical playground for software engineering, graphics programming, architecture, and content creation.

**Janky, but built properly.** 🛠️🎨
