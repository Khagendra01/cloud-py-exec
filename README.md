# Python Script Execution API

A secure REST API service that executes Python scripts in isolated containers using NSJail. This API is designed to be deployed on Google Cloud Run and provides safe execution of user-defined Python scripts with data science libraries.

## 🚀 Quick Start

### Local Docker Run (Simplest)

```bash
# Build and run with Docker
docker build -t python-script-api .
docker run -p 8080:8080 python-script-api
```

### Test the API

```bash
# Health check
curl http://localhost:8080/health

# Execute a script
curl -X POST http://localhost:8080/execute \
  -H "Content-Type: application/json" \
  -d '{
    "script": "def main():\n    print(\"Hello from stdout!\")\n    return {\"message\": \"Hello World\"}"
  }'
```

## 🌟 Features

- **Secure Execution**: All scripts run in isolated containers using NSJail
- **Docker Ready**: Lightweight Docker image optimized for Cloud Run
- **Data Science Libraries**: Includes pandas, numpy, and scipy
- **JSON Response**: Returns both script result and stdout
- **Input Validation**: Comprehensive validation of script content
- **Resource Limits**: Configurable timeout and memory limits
- **Health Monitoring**: Built-in health check endpoint

## 📋 Requirements

- **Docker**: For local development and deployment
- **Google Cloud SDK**: For Cloud Run deployment (optional)
- **Linux**: NSJail requires Linux (use WSL on Windows)

## 🐳 Docker Deployment

### Local Development

```bash
# Using docker-compose (recommended)
docker-compose up --build

# Or using Docker directly
docker build -t python-script-api .
docker run -p 8080:8080 python-script-api
```

### Production Deployment

```bash
# Build production image
docker build -f Dockerfile.prod -t python-script-api:prod .

# Run with gunicorn
docker run -p 8080:8080 python-script-api:prod
```

## ☁️ Google Cloud Run Deployment

### Automatic Deployment

```bash
# Linux/Mac
./deploy-cloud-run.sh YOUR_PROJECT_ID

# Windows
deploy-cloud-run.bat YOUR_PROJECT_ID
```

### Manual Deployment

```bash
# Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/python-script-api

# Deploy to Cloud Run
gcloud run deploy python-script-api \
  --image gcr.io/YOUR_PROJECT_ID/python-script-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080 \
  --memory 1Gi \
  --timeout 300
```

### Test Cloud Run Deployment

Replace `YOUR_CLOUD_RUN_URL` with your actual Cloud Run URL:

```bash
# Health check
curl https://YOUR_CLOUD_RUN_URL/health

# Execute a script with pandas and numpy
curl -X POST https://YOUR_CLOUD_RUN_URL/execute \
  -H "Content-Type: application/json" \
  -d '{
    "script": "import pandas as pd\nimport numpy as np\n\ndef main():\n    print(\"Creating sample data...\")\n    data = pd.DataFrame({\n        \"x\": np.random.randn(100),\n        \"y\": np.random.randn(100)\n    })\n    print(f\"Data shape: {data.shape}\")\n    return {\n        \"mean_x\": float(data[\"x\"].mean()),\n        \"mean_y\": float(data[\"y\"].mean()),\n        \"correlation\": float(data.corr().iloc[0,1])\n    }"
  }'
```

## 📚 API Documentation

### Endpoints

#### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00",
  "nsjail_config_exists": true
}
```

#### Execute Script
```http
POST /execute
Content-Type: application/json
```

**Request Body:**
```json
{
  "script": "def main():\n    print(\"Processing...\")\n    return {\"result\": 42}",
  "timeout": 30,
  "memory": 128
}
```

**Response:**
```json
{
  "success": true,
  "result": {
    "result": 42
  },
  "stdout": "Processing...\n",
  "timestamp": "2024-01-01T12:00:00"
}
```

## 🔧 Script Requirements

### Required Structure
Scripts must contain a `main()` function that returns a JSON-serializable value:

```python
def main():
    # Your code here
    print("Processing data...")
    result = {"message": "Hello World"}
    return result
```

### Available Libraries
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **scipy**: Scientific computing
- **os**: Operating system interface
- **json**: JSON encoding/decoding
- **math**: Mathematical functions
- **datetime**: Date and time utilities

### Example Scripts

#### Data Analysis with Pandas
```python
import pandas as pd
import numpy as np

def main():
    print("Loading data...")
    
    # Create sample data
    data = pd.DataFrame({
        'id': range(1, 101),
        'value': np.random.randn(100),
        'category': np.random.choice(['A', 'B', 'C'], 100)
    })
    
    print(f"Dataset shape: {data.shape}")
    
    # Perform analysis
    summary = {
        'total_records': len(data),
        'mean_value': float(data['value'].mean()),
        'std_value': float(data['value'].std()),
        'category_counts': data['category'].value_counts().to_dict()
    }
    
    return summary
```

## 🛡️ Security Features

### NSJail Sandboxing
- **Process Isolation**: Complete isolation using Linux namespaces
- **Resource Limits**: Memory, CPU, and file system constraints
- **Network Control**: No network access by default
- **Filesystem Security**: Read-only mounts and restricted access
- **Syscall Filtering**: Seccomp-BPF policies for system call restrictions

### API Security
- **Input Validation**: Strict validation of script content
- **Resource Limits**: Configurable timeout and memory limits
- **Error Isolation**: Script errors don't affect the API server
- **Temporary Files**: Script files are cleaned up after execution

## 🧪 Testing

### Run Test Suite

```bash
# Test local Docker deployment
python test_docker.py

# Test Cloud Run deployment
python test_docker.py https://YOUR_CLOUD_RUN_URL
```

### Manual Testing

```bash
# Health check
curl http://localhost:8080/health

# Simple script
curl -X POST http://localhost:8080/execute \
  -H "Content-Type: application/json" \
  -d '{"script": "def main():\n    return {\"message\": \"test\"}"}'

# Data science script
curl -X POST http://localhost:8080/execute \
  -H "Content-Type: application/json" \
  -d '{"script": "import pandas as pd\nimport numpy as np\n\ndef main():\n    data = pd.DataFrame({\"x\": np.random.randn(10)})\n    return {\"mean\": float(data[\"x\"].mean())}"}'
```

## 📁 Project Structure

```
pythonexec/
├── api_server.py              # Main Flask API server
├── Dockerfile                 # Development Docker image
├── Dockerfile.prod           # Production Docker image
├── docker-compose.yml        # Local development setup
├── requirements.txt          # Python dependencies
├── deploy-cloud-run.sh       # Cloud Run deployment script (Linux/Mac)
├── deploy-cloud-run.bat      # Cloud Run deployment script (Windows)
├── test_docker.py            # Docker test suite
├── configs/                  # NSJail configuration files
├── scripts/                  # Temporary script storage
├── logs/                     # Execution logs
├── chroot/                   # NSJail chroot directory
└── README_DOCKER.md          # Detailed Docker documentation
```

## 🔍 Troubleshooting

### Common Issues

1. **NSJail not found**
   ```
   Error: NSJail is not available
   ```
   Solution: Ensure Docker image builds correctly with NSJail

2. **Memory limit exceeded**
   ```
   Error: Script execution failed: memory limit exceeded
   ```
   Solution: Increase memory allocation or optimize script

3. **Timeout errors**
   ```
   Error: Script execution timed out
   ```
   Solution: Increase timeout or optimize script performance

4. **Import errors**
   ```
   Error: No module named 'pandas'
   ```
   Solution: Ensure Docker image includes required libraries

### Debug Mode
For local development, you can enable debug mode:
```python
app.run(host='0.0.0.0', port=8080, debug=True)
```

## 📊 Performance

### Resource Recommendations
- **Memory**: 1GB for data science workloads
- **CPU**: 1 vCPU should be sufficient
- **Timeout**: 300 seconds maximum for Cloud Run

### Optimization Tips
- Use efficient data structures (numpy arrays over lists)
- Avoid loading large datasets into memory
- Use pandas chunking for large files
- Implement proper error handling in scripts

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🔗 Links

- [NSJail Documentation](https://github.com/google/nsjail)
- [Google Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Docker Documentation](https://docs.docker.com/)


