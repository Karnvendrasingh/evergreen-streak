<div align="center">

# 🌱 Evergreen Streak

> 🚀 Keep your GitHub streak alive — automatically!  
> This repository uses **GitHub Actions** to make a small daily commit, ensuring your contribution graph stays green 🌿

![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Enabled-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)
![Auto Commit](https://img.shields.io/badge/Auto%20Commit-Daily-success?style=for-the-badge&logo=git&logoColor=white)
![Timezone](https://img.shields.io/badge/Timezone-IST-orange?style=for-the-badge&logo=clock&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)

</div>

---

## ✨ Features

✅ **Automatic Daily Commits** – Runs every day at 8:30 AM IST (3:00 AM UTC)  
✅ **Fully Cloud-Based** – No need to keep your PC on; it's powered by GitHub Actions  
✅ **Customizable** – Change the commit schedule or file contents easily  
✅ **Lightweight & Safe** – Only updates one text file (`update.txt`) with the current date and time  

---

## 🧠 How It Works

1. A **GitHub Action** runs daily using a CRON schedule.  
2. It updates `update.txt` with the latest timestamp (in IST).  
3. The action commits and pushes the change to your repo.  
4. GitHub detects this activity → keeps your streak active ✅  

---

## 🕒 Example Output

Your `update.txt` will look like this:

```
Last updated: 2025-10-31 08:30:00 IST
```

---

## ⚙️ Workflow Setup

The workflow file is located at:

```
.github/workflows/streak.yml
```

### 💾 Full Workflow Code

```yaml
name: GitHub Streak Saver

on:
  schedule:
    - cron: '0 3 * * *'  # Runs every day at 8:30 AM IST (3:00 AM UTC)
  workflow_dispatch:

jobs:
  update-commit:
    runs-on: ubuntu-latest
    permissions:
      contents: write

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Update timestamp file
        run: |
          echo "Last updated: $(TZ='Asia/Kolkata' date '+%Y-%m-%d %H:%M:%S %Z')" > update.txt

      - name: Commit and push changes
        run: |
          git config --global user.name "Karnvendrasingh"
          git config --global user.email "karnvendrasingh@gmail.com"
          git add update.txt
          git commit -m "Daily Commit" || echo "No changes to commit"
          git push origin main
```

---

## 🔄 Run Manually

If you ever want to trigger it right away:

1. Go to your repository → **Actions**
2. Select **GitHub Streak Saver**
3. Click **Run workflow** → Run manually

---

## 🧩 Customize It

| Goal | What to Change |
|------|----------------|
| 🕒 **Change run time** | Update the `cron` line (UTC-based) |
| 🗂 **Change file name** | Replace `update.txt` with your file name |
| 🧾 **Append instead of overwrite** | Use `>>` instead of `>` in echo command |
| 🌍 **Change timezone** | Replace `Asia/Kolkata` with your own timezone |

---

## 💡 Pro Tip: Add a History Log

Want to track all your streak updates?

**Replace this line:**
```bash
echo "Last updated: $(TZ='Asia/Kolkata' date '+%Y-%m-%d %H:%M:%S %Z')" > update.txt
```

**with this:**
```bash
echo "Updated on: $(TZ='Asia/Kolkata' date '+%Y-%m-%d %H:%M:%S %Z')" >> history.txt
```

➡️ It will keep a full log of all daily commits inside `history.txt`.

---

## 🚀 Getting Started

### 1️⃣ Fork or Clone This Repository

```bash
git clone https://github.com/Karnvendrasingh/evergreen-streak.git
cd evergreen-streak
```

### 2️⃣ Enable GitHub Actions

- Go to **Settings** → **Actions** → **General**
- Under **Workflow permissions**, select:
  - ✅ **Read and write permissions**
  - ✅ **Allow GitHub Actions to create and approve pull requests**

### 3️⃣ Let It Run!

The workflow will automatically run daily at **8:30 AM IST**. You can also trigger it manually from the **Actions** tab.

---

## 🧑‍💻 Created By

**Karnvendra Singh**  
💼 [GitHub](https://github.com/Karnvendrasingh) • 🌍 [LinkedIn](https://www.linkedin.com/in/karnvendrasingh/) • 📧 [Email](mailto:karnvendrasingh@gmail.com) • 🧠 Automating Everyday Productivity

---

## ⭐ Support

If you like this project, consider giving it a ⭐ **Star** — it helps keep the streak going 😉

---

## 📜 License

This project is licensed under the **MIT License** – feel free to use and modify it!

---

<div align="center">

**Made with ❤️ and ☕ by [Karnvendra Singh](https://github.com/Karnvendrasingh)**

</div>
