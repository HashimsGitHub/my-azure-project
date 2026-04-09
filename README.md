# 🌌 Nebula Drive

> A modern web application for managing and accessing Azure SMB File Shares through an intuitive browser-based interface.

![Azure](https://img.shields.io/badge/Azure-0078D4?style=for-the-badge&logo=microsoftazure&logoColor=white)
![SMB](https://img.shields.io/badge/SMB-File%20Share-blueviolet?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Deployed-success?style=for-the-badge)

---

## 📖 Overview

**Nebula Drive** is a web-based file management application built on top of Azure SMB File Shares. It provides users with a seamless, cloud-powered experience to upload, browse, download, and manage files — all from the browser, without needing to mount a network drive.

---

## ✨ Features

- 📁 **Browse & Navigate** — Explore your Azure File Share directory structure with ease
- ⬆️ **Upload Files** — Drag and drop or select files to upload directly to Azure File Share
- ⬇️ **Download Files** — Instantly download files stored in the cloud
- 🗑️ **Delete Files & Folders** — Remove unwanted files directly from the UI
- 📂 **Create Folders** — Organise your files with custom directory structures
- 🔒 **Secure Access** — Authenticated access backed by Azure credentials
- ☁️ **Azure-Powered** — Leverages Azure SMB File Share for reliable, scalable storage

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

### Prerequisites

- [Azure Subscription](https://azure.microsoft.com/en-au/free/)
- Azure Storage Account with SMB File Share enabled
- Node.js (or relevant runtime) installed
- Azure CLI (optional, for deployment)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/nebula-drive.git
   cd nebula-drive
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Configure environment variables**

   Create a `.env` file in the root directory:
   ```env
   AZURE_STORAGE_ACCOUNT_NAME=your_storage_account_name
   AZURE_STORAGE_ACCOUNT_KEY=your_storage_account_key
   AZURE_FILE_SHARE_NAME=your_file_share_name
   PORT=3000
   ```

4. **Run the application locally**
   ```bash
   npm start
   ```

5. **Open in browser**
   ```
   http://localhost:3000
   ```

---

## ☁️ Deployment

Nebula Drive is deployed on **Azure App Service**.

### Deploy via Azure CLI

```bash
az login
az webapp up \
  --name nebula-drive \
  --resource-group your-resource-group \
  --runtime "NODE:18-lts" \
  --sku B1
```

### Deploy via GitHub Actions

Ensure the following secrets are set in your GitHub repository:

| Secret | Description |
|--------|-------------|
| `AZURE_WEBAPP_PUBLISH_PROFILE` | Azure Web App publish profile |
| `AZURE_STORAGE_ACCOUNT_NAME` | Storage account name |
| `AZURE_STORAGE_ACCOUNT_KEY` | Storage account key |
| `AZURE_FILE_SHARE_NAME` | File share name |

---

## 🔧 Configuration

| Variable | Description | Required |
|----------|-------------|----------|
| `AZURE_STORAGE_ACCOUNT_NAME` | Azure Storage Account name | ✅ |
| `AZURE_STORAGE_ACCOUNT_KEY` | Azure Storage Account access key | ✅ |
| `AZURE_FILE_SHARE_NAME` | Name of the SMB File Share | ✅ |
| `PORT` | Port to run the web server | ❌ (default: 3000) |

---

## 🛡️ Security

- All credentials are managed via environment variables — never hardcoded
- Azure Storage Account keys should be rotated regularly
- Consider using **Azure Managed Identity** for production deployments
- Enable **HTTPS only** on your Azure App Service
- Restrict access using **Azure Active Directory** or IP allowlisting if needed

---

## 📦 Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | HTML, CSS, JavaScript |
| Backend | Node.js / Express (or your framework) |
| Storage | Azure SMB File Share |
| Hosting | Azure App Service |
| Auth | Azure Storage Account Key / Managed Identity |

---

## 🤝 Contributing

Contributions are welcome! To get started:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

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
