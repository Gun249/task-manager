# Task Manager - AI-Powered Role-Task Matching System

An task management system that leverages AI to analyze project requirements, generate interview questions, and match suitable tasks to specific roles using semantic similarity.

## 🌟 Features

- **AI-Powered Project Analysis**: Uses Gemini to analyze project details and extract relevant information
- **Dynamic Interview Generation**: Generates 5 simple, foundational interview questions to assess their basic understanding, learning enthusiasm, and natural inclinations toward different technical roles
- **Role-Task Matching**: Employs a fine-tuned Siamese neural network to match tasks with appropriate roles (Backend Developer, Frontend Developer, Project Manager, UX/UI Designer) based on semantic similarity
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
   pip install -r requirements.txt
   ```

3. **Download spaCy language model**:
   ```bash
   python -m spacy download en_core_web_lg
   ```

4. **Set up environment variables**:
   Create a `.env` file in the root directory and add your API key:
   ```
   apikey=your_google_generative_ai_api_key_here
   ```

5. **Verify model files**:
   Ensure the pre-trained Siamese model is in the `models/role_task_siamese_v1/` directory.

### Usage

1. **Run the application**:
   ```bash
   python main.py
   ```

2. **Provide project details**:
   When prompted, enter a detailed description of your project requirements.

3. **Answer interview questions**:
   The system will generate 5 simple, foundational questions based on your project. These questions help the AI understand your basic technical understanding, interests, and problem-solving approach without requiring deep existing knowledge.

4. **Review results**:
   The system will output:
   - Recommended role for your project
   - Matching tasks with similarity scores

## 🔧 Configuration

### Model Configuration

The system uses a pre-trained Siamese neural network located in `models/role_task_siamese_v1/`. You can customize the matching behavior by adjusting:

- **Similarity Threshold**: Minimum cosine similarity score for task matching (default: 0.4)
- **Model Path**: Path to the sentence transformer model

### API Configuration

The system integrates with Gemini. Configure your API settings in the `.env` file:

```
apikey=your_api_key_here
```

## 📊 Dataset Information

The system utilizes a comprehensive dataset containing:

- **20,000+ Task Descriptions**: Categorized by role and required skills
- **Role Categories**: Backend Developer, Frontend Developer, etc.
- **Skill Mappings**: Technologies and frameworks associated with each task

## 🤖 AI Components

### Chatbot (apichatbot.py)

- Analyzes project requirements using Gemini
- Generates 5 simple, foundational interview questions tailored 
- Creates questions designed to assess basic understanding, learning enthusiasm, and problem-solving approach
- Extracts tasks aligned with four major roles: Backend Developer, Frontend Developer, Project Manager (PM), and UX/UI Designer
- Processes user responses to determine the most suitable role

### Role-Task Matcher (botcompae.py)

- Uses SentenceTransformer for semantic similarity
- Employs cosine similarity for task-role matching
- Configurable similarity thresholds
- Returns ranked task recommendations

## 🔍 Example Workflow

1. **Input**: "I need to build a web application with user authentication and data visualization"

2. **AI Analysis**: System generates 5 simple, foundational interview questions :
   - Basic understanding and enthusiasm for learning
   - Initial technical inclinations and preferences
   - Foundational problem-solving mindset
   - Natural curiosity across Backend, Frontend, PM, and UX/UI concepts
   - How students articulate their thoughts on basic technical concepts

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