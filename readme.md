# 📘 S3 CLI Tool

A lightweight command-line interface for managing files in S3-compatible storage services (MinIO, AWS S3, etc.)

## ✨ Features

- 📤 Upload files with custom keys and prefixes
- 🔗 Generate temporary download links
- 📊 View file metadata
- 📋 List bucket contents
- 🗑️ Delete files
- ✏️ Overwrite existing files
- 🔒 Secure SSL support with insecure mode for testing

## 🚀 Quick Start

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/xoxxel/S3-Backend.git
   cd S3-Backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure your `.env` file:
   ```env
   S3_ENDPOINT=your-s3-endpoint
   S3_ACCESS_KEY=your-access-key
   S3_SECRET_KEY=your-secret-key
   S3_BUCKET=your-bucket-name
   ```

## 🛠️ Commands

### Upload Files
```bash
python s3cli.py upload <file> [--key KEY] [--prefix PREFIX]
```
- Upload local files to S3 with optional custom keys and prefixes
- Example: `python s3cli.py upload image.jpg --prefix images/`

### Generate Presigned URLs
```bash
python s3cli.py presign <key> [--expires SECONDS]
```
- Create temporary download links
- Default expiry: 300 seconds (5 minutes)
- Example: `python s3cli.py presign images/photo.jpg --expires 3600`

### View Metadata
```bash
python s3cli.py head <key>
```
- Display file metadata (size, content-type, ETag)
- Example: `python s3cli.py head images/photo.jpg`

### List Files
```bash
python s3cli.py list [--prefix PREFIX]
```
- List all files or filter by prefix
- Example: `python s3cli.py list --prefix images/`

### Delete Files
```bash
python s3cli.py delete <key>
```
- Remove files from the bucket
- Example: `python s3cli.py delete images/old-photo.jpg`

### Overwrite Files
```bash
python s3cli.py overwrite <key> <file>
```
- Replace existing S3 objects with new content
- Example: `python s3cli.py overwrite images/logo.png new-logo.png`

## 🔧 Global Options

- `--insecure`: Disable SSL verification (testing only)
  ```bash
  python s3cli.py --insecure <command>
  ```

## 📂 Project Structure
```
.
├── s3cli.py           # Main CLI application
├── requirements.txt   # Dependencies
├── .env              # Configuration
└── .env.example      # Example configuration
```

## 📝 Notes

- Always use SSL in production environments
- Store credentials securely in `.env`
- Supports any S3-compatible storage service
- Virtual folder structure using prefixes

## 🔐 Security

- Secure by default with SSL enabled
- Environment-based configuration
- Support for temporary access via presigned URLs

## 📚 Dependencies

- minio: S3 client library
- python-dotenv: Environment configuration
- Python 3.6+

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

MIT License - feel free to use and modify as needed.

## 🔗 Repository

[GitHub Repository](https://github.com/xoxxel/S3-Backend.git)
python minio_cli.py overwrite assets/logo.webp ./new-logo.webp
```
