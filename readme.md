# Tugas Besar Strategi Algoritma IF2211

## Implementasi Algoritma Greedy untuk Membuat Bot Permainan Etimo Diamonds

## Table of Contents

- [Table of Contents](#table-of-contents)
- [General Information](#general-information)
- [Contributor](#contributor)
- [Structure](#structure)
- [Dependencies](#dependencies)
- [How to Use](#how-to-use)
  - [Setup Game Engine](#setup-game-engine)
  - [Setup Bot](#setup-bot)
- [Video Demo](#video-demo)

## General Information

Algoritma greedy merupakan pendekatan yang populer dalam pemecahan persoalan optimasi. Persoalan optimasi bertujuan untuk mencari solusi optimal di antara sejumlah solusi yang mungkin. Algoritma greedy menyelesaikan persoalan secara langkah demi langkah, dimana pada setiap langkah, kita memilih pilihan yang tampaknya paling menguntungkan pada saat itu, tanpa mempertimbangkan konsekuensi di masa depan. Harapannya adalah dengan memilih solusi lokal yang optimal pada setiap langkah, kita akan mencapai solusi global yang optimal.

## Contributor

| Name                       | NIM      |
| -------------------------- | -------- |
| Christian Justin Hendrawan | 13522135 |
| Muhammad Fatihul Irhab     | 13522143 |
| Ikhwan Al Hakim            | 13522147 |

## Structure

```
├── doc
│   └── bingung_Revisi1.pdf
├── readme.md
├── src
    ├── decode.py
    ├── game
    │   ├── api.py
    │   ├── board_handler.py
    │   ├── bot_handler.py
    │   ├── __init__.py
    │   ├── logic
    │   │   ├── base.py
    │   │   ├── __init__.py
    │   │   ├── pulang.py
    │   │   └── random.py
    │   ├── models.py
    │   └── util.py
    ├── main.py
    ├── README.md
    ├── requirements.txt
    ├── run-bots.bat
    └── run-bots.sh
```

## Dependencies

1. Node.js
2. Docker Desktop
3. Yarn
4. Python

## How to Use

### Setup Game Engine

1. Download game engine pada link berikut
   ```
   https://github.com/haziqam/tubes1-IF2211-game-engine/releases/tag/v1.1.0
   ```
2. Extract file yang sudah di download
3. Masuk ke root directory dari project
   ```
   cd tubes1-IF2110-game-engine-1.1.0
   ```
4. Install dependencies menggunakan Yarn
   ```
   yarn
   ```
5. Setup default environment variable dengan menjalankan script berikut

   Untuk Windows

   ```
   ./scripts/copy-env.bat
   ```

   Untuk Linux / (possibly) macOS

   ```chmod +x ./scripts/copy-env.sh
   ./scripts/copy-env.sh
   ```

6. Setup local database (buka aplikasi docker desktop terlebih dahulu, lalu jalankan command berikut di terminal)

   ```
   docker compose up -d database
   ```

   Lalu jalankan script berikut. Untuk Windows

   ```
   ./scripts/setup-db-prisma.bat
   ```

   Untuk Linux / (possibly) macOS

   ```
   chmod +x ./scripts/setup-db-prisma.sh
   ./scripts/setup-db-prisma.sh
   ```

7. Lakukan build
   ```
   npm run build
   ```
8. Lakukan start
   ```
   npm run start
   ```

### Setup Bot

1. Clone repository ini
   ```
   git clone https://github.com/Nerggg/Tubes1_bingung
   ```
2. Extract file yang sudah di download
3. Masuk ke root directory dari project
   ```
   cd Tubes1_bingung
   ```
4. Install dependencies menggunakan pip
   ```
   pip install -r requirements.txt
   ```
5. Jalankan bot dengan command ini
   ```
   python main.py --logic Pulang --email=bingung@example.com --name=pulang --password=bingung --team bingung
   ```

## Video Demo

https://youtu.be/zSz0QU0fojI
