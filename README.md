# FastAPI Learning Repository

A comprehensive collection of FastAPI notes, tutorials, and projects for learning and reference.

## 📚 Contents

### 📖 Tutorial
Basic FastAPI tutorial covering fundamental concepts and getting started with the framework.
- **Files**: `main.py` - Core tutorial implementation

### 🚀 Project 1
Practical FastAPI application demonstrating real-world usage patterns.
- **Files**: 
  - `main.py` - Main application file
  - `flow.ipynb` - Jupyter notebook for workflow exploration
  - `patients.json` - Sample data file

### 🔧 Project 2
Additional FastAPI project showcasing advanced features and patterns.

### 🐳 Docker
Containerization setup and deployment configurations for FastAPI applications.
- **Files**: 
  - `Dockerfile` - Docker configuration
  - `Notes/` - Docker-related documentation

### 🔍 Pydantic
Examples and notes on using Pydantic for data validation in FastAPI.

## 🛠️ Technologies Used

- **FastAPI** - Modern, fast web framework for building APIs
- **Python** (89.9%) - Primary programming language
- **Jupyter Notebook** (8.4%) - Interactive development
- **Docker** (1.7%) - Containerization
- **Pydantic** - Data validation and settings management

## 🚀 Getting Started

### Prerequisites
```bash
python >= 3.7
pip
```

### Installation

1. Clone the repository
```bash
git clone https://github.com/MohitRawat017/FastAPI.git
cd FastAPI
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install FastAPI and dependencies
```bash
pip install fastapi uvicorn[standard]
```

### Running the Projects

#### Tutorial
```bash
cd Tutorial
uvicorn main:app --reload
```

#### Project 1
```bash
cd Project1
uvicorn main:app --reload
```

Visit `http://127.0.0.1:8000/docs` for interactive API documentation (Swagger UI)

## 🐳 Docker Usage

Build and run using Docker:

```bash
cd Docker
docker build -t fastapi-app .
docker run -p 8000:8000 fastapi-app
```

## 📝 Key Concepts Covered

- ✅ FastAPI basics and routing
- ✅ Request/Response models with Pydantic
- ✅ Path parameters and query parameters
- ✅ Request body handling
- ✅ API documentation (Swagger/ReDoc)
- ✅ Docker containerization
- ✅ Project structure and organization

## 📖 Resources

- [FastAPI Official Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Uvicorn Documentation](https://www.uvicorn.org/)

## 🤝 Contributing

Feel free to fork this repository and submit pull requests for improvements!

## 📄 License

This project is open source and available for learning purposes.

---

⭐ Star this repo if you find it helpful!
