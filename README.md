# Python Script Execution API

A secure REST API service that executes Python scripts in isolated containers using NSJail. 
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