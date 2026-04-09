# 🌌 Nebula Drive

> A modern web application for managing and accessing Azure SMB File Shares through an intuitive browser-based interface.

![Azure](https://img.shields.io/badge/Azure-0078D4?style=for-the-badge&logo=microsoftazure&logoColor=white)
![SMB](https://img.shields.io/badge/SMB-File%20Share-blueviolet?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Deployed-success?style=for-the-badge)

---

## 📖 Overview

**Nebula Drive** is a web-based file management application built on top of Azure SMB File Shares. It provides users with a seamless, cloud-powered NAS experience to upload, browse, download, and manage files by simply mounting a network drive.

---

## ✨ Features

- 📁 **Browse & Navigate** — Explore your SMB Drive directory structure with ease
- ⬆️ **Upload Files** — Drag and drop or select files to upload directly to Mapped Network Drive
- ⬇️ **Download Files** — Instantly access files stored in the cloud
- 🗑️ **Delete Files & Folders** — Use just like your normal NAS Drive
- 📂 **Create Folders** — Organise your files with custom directory structures
- 🔒 **Secure Access** — Authenticated access backed by Azure credentials
- ☁️ **Azure-Powered** — Leverages Azure SMB File Share for reliable, scalable storage

---
<img width="1750" height="788" alt="image" src="https://github.com/user-attachments/assets/1d375f65-c176-459d-8939-7de742f5a620" />

<img width="1788" height="300" alt="image" src="https://github.com/user-attachments/assets/20cf3654-e29f-4e7c-8bbb-d0626645182c" />

<img width="1801" height="1057" alt="image" src="https://github.com/user-attachments/assets/30e21b4c-cade-4fa7-bba3-2d23f0d33944" />

---

## 🏗️ Architecture

```
User Browser
     │
     ▼
Nebula Drive Web App
     │
     ▼
Azure App Service / Web Server
     │
     ▼
Azure SMB File Share (Storage Account)
```

---

## 🚀 Getting Started

Visit https://nebuladrive.cloud 

---
## 🛡️ Secure & Reliable

- Uses GitHub OAuth, user credentials are stored on site
- Netork Mapped Drive is built on Azure Files technology
- 99.99% Availability with Transaction Optimized Speed
- Storage Capacity expandable to Petabyte Scale
- Global Secure Access
---

## 📦 Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python API |
| Storage | Azure SMB File Share |
| Hosting | Azure Static Web App Service |
| Auth | GitHub OAuth |

---


## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 📬 Contact

For questions or support, please open an issue in the repository or reach out via your organisation's support channels.

---

<div align="center">
  <sub>Built with ☁️ and deployed on Microsoft Azure</sub>
</div>
