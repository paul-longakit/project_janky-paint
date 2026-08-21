# 🎨 JankyPaint

JankyPaint is a lightweight Python-based digital painting application built as part of my personal Janky Content Creation System.

The goal is simple: build a small painting and asset-creation tool from scratch while experimenting with clean software architecture, drawing systems, and content pipelines.

> "Janky, but built properly." 🛠️

## ✨ Current Features

- 🖌️ Brush tool
- 🧼 Eraser tool
- 🪣 Paint Bucket / Fill tool
- 🎨 Color picker
- 🌈 HSL color controls
- 🔴 RGB color values
- #️⃣ HEX color input
- 📏 Adjustable brush size
- 🗂️ Basic layer support
- 💾 PNG image export
- 🧩 Painting operations
- 🏗️ Clean Architecture-inspired project structure

## 🏗️ Architecture

JankyPaint is structured around a simple separation of responsibilities:

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