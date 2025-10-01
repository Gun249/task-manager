# Task Manager - AI-Powered Role-Task Matching System

An intelligent task management system that leverages AI to analyze project requirements, generate interview questions, and match suitable tasks to specific roles using semantic similarity.

## 🌟 Features

- **AI-Powered Project Analysis**: Uses Google's Generative AI to analyze project details and extract relevant information
- **Dynamic Interview Generation**: Automatically generates contextual interview questions based on project requirements
- **Role-Task Matching**: Employs a fine-tuned Siamese neural network to match tasks with appropriate roles based on semantic similarity
- **Interactive CLI Interface**: User-friendly command-line interface for seamless interaction
- **Comprehensive Task Database**: Includes a dataset of over 20,000 categorized tasks with associated skills

## 🏗️ System Architecture

The system consists of four main components:

1. **API Chatbot (`apichatbot.py`)**: Handles AI communication and project analysis
2. **Role-Task Matcher (`botcompae.py`)**: Performs semantic matching using pre-trained models
3. **Data Processing (`data.py`)**: Manages dataset operations and preprocessing
4. **Feature Engineering (`feature_engineering.py`)**: Handles data transformation and feature extraction

## 📁 Project Structure

```
task-manager/
├── main.py                     # Main application entry point
├── dataset/                    # Data files
│   ├── hr_dashboard_data.csv   # HR dashboard data
│   ├── Task Catagories.csv     # Task categories and skills mapping
│   └── updated_hr_data.csv     # Updated HR dataset
├── models/                     # Pre-trained models
│   └── role_task_siamese_v1/   # Siamese network for role-task matching
├── src/                        # Source code modules
│   ├── apichatbot.py          # AI chatbot implementation
│   ├── botcompae.py           # Role-task matching logic
│   ├── data.py                # Data handling utilities
│   ├── feature_engineering.py # Feature processing
│   └── suitabilty.py          # Suitability assessment
└── README.md                  # Project documentation
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Google Generative AI API key
- Required Python packages (see installation section)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Gun249/task-manager.git
   cd task-manager
   ```

2. **Install required dependencies**:
   ```bash
   pip install google-generativeai python-dotenv sentence-transformers torch
   ```

3. **Set up environment variables**:
   Create a `.env` file in the root directory and add your API key:
   ```
   apikey=your_google_generative_ai_api_key_here
   ```

4. **Verify model files**:
   Ensure the pre-trained Siamese model is in the `models/role_task_siamese_v1/` directory.

### Usage

1. **Run the application**:
   ```bash
   python main.py
   ```

2. **Provide project details**:
   When prompted, enter a detailed description of your project requirements.

3. **Answer interview questions**:
   The system will generate contextual questions based on your project. Answer them to help the AI better understand your needs.

4. **Review results**:
   The system will output:
   - Recommended role for your project
   - Matching tasks with similarity scores
   - Suitable tasks ranked by relevance

## 🔧 Configuration

### Model Configuration

The system uses a pre-trained Siamese neural network located in `models/role_task_siamese_v1/`. You can customize the matching behavior by adjusting:

- **Similarity Threshold**: Minimum cosine similarity score for task matching (default: 0.4)
- **Model Path**: Path to the sentence transformer model

### API Configuration

The system integrates with Google's Generative AI. Configure your API settings in the `.env` file:

```
apikey=your_api_key_here
```

## 📊 Dataset Information

The system utilizes a comprehensive dataset containing:

- **20,000+ Task Descriptions**: Categorized by role and required skills
- **Role Categories**: Backend Developer, Frontend Developer, Data Scientist, etc.
- **Skill Mappings**: Technologies and frameworks associated with each task

### Sample Data Structure

| Task Description | Category | Skill |
|-----------------|----------|-------|
| Implement user authentication | backend developer | spring boot |
| Optimize server performance | backend developer | asp.net |
| Manage database operations | backend developer | django |

## 🤖 AI Components

### Chatbot (apichatbot.py)

- Analyzes project requirements using Google's Generative AI
- Generates contextual interview questions
- Extracts roles and tasks from project descriptions
- Processes user responses to refine recommendations

### Role-Task Matcher (botcompae.py)

- Uses SentenceTransformer for semantic similarity
- Employs cosine similarity for task-role matching
- Configurable similarity thresholds
- Returns ranked task recommendations

## 🔍 Example Workflow

1. **Input**: "I need to build a web application with user authentication and data visualization"

2. **AI Analysis**: System generates questions about:
   - Technology preferences
   - Team size and structure
   - Timeline and complexity requirements

3. **Role Recommendation**: "Backend Developer"

4. **Task Matching**: 
   - Implement user authentication (Score: 0.8542)
   - Design database schema (Score: 0.7891)
   - Create API endpoints (Score: 0.7645)

## 🛠️ Development

### Adding New Features

1. **Extend the dataset**: Add new task categories in `dataset/Task Catagories.csv`
2. **Customize prompts**: Modify AI prompts in `apichatbot.py`
3. **Adjust matching logic**: Update similarity calculations in `botcompae.py`

### Testing

Run the application with sample data to verify functionality:

```bash
python main.py
```

## 🙏 Acknowledgments

- Google Generative AI for natural language processing
- Sentence Transformers library for semantic similarity
- The open-source community for various dependencies and tools

---

**Note**: This system is designed for educational and research purposes. Ensure you have proper API keys and follow the terms of service for all integrated services.