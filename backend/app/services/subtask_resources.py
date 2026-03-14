"""
Sub-task resource library — real, actionable learning resources for each milestone.
Maps milestone IDs to lists of 3-6 sub-tasks with curated resources.
"""

# ─── Software Development Sub-Tasks ────────────────────────────────────────────

SOFTWARE_DEV_SUBTASKS = {
    # Phase 1: Foundation
    "milestone_1": [  # Programming Fundamentals
        {
            "task_title": "Complete Python Basics on freeCodeCamp",
            "description": "Work through the full Scientific Computing with Python curriculum covering variables, loops, functions, data structures, and OOP",
            "estimated_time": "20 hours",
            "resource_type": "course",
            "resource_title": "freeCodeCamp: Scientific Computing with Python",
            "resource_url": "https://www.freecodecamp.org/learn/scientific-computing-with-python/"
        },
        {
            "task_title": "Solve 30 Easy Problems on LeetCode",
            "description": "Practice arrays, strings, and hash maps through beginner-level coding challenges to build problem-solving confidence",
            "estimated_time": "15 hours",
            "resource_type": "practice",
            "resource_title": "LeetCode: Top Interview Easy Collection",
            "resource_url": "https://leetcode.com/explore/interview/card/top-interview-questions-easy/"
        },
        {
            "task_title": "Study Data Structures with Visualizations",
            "description": "Learn arrays, linked lists, stacks, queues, and trees using interactive visualizations and implement each from scratch",
            "estimated_time": "12 hours",
            "resource_type": "video",
            "resource_title": "CS Dojo: Data Structures & Algorithms in Python",
            "resource_url": "https://www.youtube.com/playlist?list=PLBZBJbE_rGRV8D7XZ08LK6z-4zPoWzu5H"
        },
        {
            "task_title": "Build a CLI Calculator & To-Do App",
            "description": "Apply fundamentals by building a command-line calculator with error handling and a to-do list with file persistence",
            "estimated_time": "8 hours",
            "resource_type": "project",
            "resource_title": "Real Python: Command-Line Interfaces",
            "resource_url": "https://realpython.com/python-command-line-arguments/"
        },
    ],
    "milestone_2": [  # Development Environment Setup
        {
            "task_title": "Set Up VS Code for Python Development",
            "description": "Install VS Code, configure Python extension, set up linting (pylint/flake8), formatting (black), and debugging tools",
            "estimated_time": "3 hours",
            "resource_type": "documentation",
            "resource_title": "VS Code: Python in Visual Studio Code",
            "resource_url": "https://code.visualstudio.com/docs/python/python-tutorial"
        },
        {
            "task_title": "Learn Virtual Environments & pip",
            "description": "Master Python virtual environments (venv), pip package management, and requirements.txt for dependency management",
            "estimated_time": "2 hours",
            "resource_type": "documentation",
            "resource_title": "Python Official: venv Tutorial",
            "resource_url": "https://docs.python.org/3/tutorial/venv.html"
        },
        {
            "task_title": "Install & Configure Git + GitHub",
            "description": "Install Git, create GitHub account, set up SSH keys, learn basic commands (init, add, commit, push, pull)",
            "estimated_time": "4 hours",
            "resource_type": "course",
            "resource_title": "GitHub Skills: Introduction to GitHub",
            "resource_url": "https://github.com/skills/introduction-to-github"
        },
        {
            "task_title": "Set Up Terminal & Developer Tooling",
            "description": "Configure terminal (Windows Terminal/iTerm2), learn shell basics, install Node.js, Docker Desktop, and Postman",
            "estimated_time": "3 hours",
            "resource_type": "video",
            "resource_title": "Fireship: The 50 Best Dev Tools",
            "resource_url": "https://www.youtube.com/watch?v=qIXS04agN3g"
        },
    ],
    "milestone_3": [  # Version Control & Collaboration
        {
            "task_title": "Complete Git Branching Interactive Tutorial",
            "description": "Learn branching, merging, rebasing, and cherry-picking through a gamified interactive tutorial",
            "estimated_time": "4 hours",
            "resource_type": "practice",
            "resource_title": "Learn Git Branching (Interactive)",
            "resource_url": "https://learngitbranching.js.org/"
        },
        {
            "task_title": "Practice Pull Requests & Code Review",
            "description": "Fork an open-source repo, make changes, create a pull request, and practice code review workflow",
            "estimated_time": "6 hours",
            "resource_type": "project",
            "resource_title": "First Contributions GitHub Project",
            "resource_url": "https://github.com/firstcontributions/first-contributions"
        },
        {
            "task_title": "Write Professional README & Documentation",
            "description": "Learn Markdown, write a professional README.md with badges, screenshots, installation steps, and API docs",
            "estimated_time": "3 hours",
            "resource_type": "documentation",
            "resource_title": "GitHub: About READMEs",
            "resource_url": "https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes"
        },
    ],

    # Phase 2: Core Development
    "milestone_4": [  # Web Development Basics
        {
            "task_title": "Build a Portfolio Website with HTML & CSS",
            "description": "Create a responsive personal portfolio website using semantic HTML5, CSS Grid, Flexbox, and media queries",
            "estimated_time": "15 hours",
            "resource_type": "course",
            "resource_title": "The Odin Project: Foundations",
            "resource_url": "https://www.theodinproject.com/paths/foundations/courses/foundations"
        },
        {
            "task_title": "Learn JavaScript DOM Manipulation",
            "description": "Master DOM selection, event handling, and dynamic content creation by building interactive components",
            "estimated_time": "12 hours",
            "resource_type": "course",
            "resource_title": "JavaScript.info: Document Object Model",
            "resource_url": "https://javascript.info/document"
        },
        {
            "task_title": "Build a Weather App with Fetch API",
            "description": "Create a weather application that fetches data from OpenWeatherMap API, handles errors, and displays results dynamically",
            "estimated_time": "8 hours",
            "resource_type": "project",
            "resource_title": "The Odin Project: Weather App",
            "resource_url": "https://www.theodinproject.com/lessons/node-path-javascript-weather-app"
        },
        {
            "task_title": "Learn Responsive Design with CSS Flexbox/Grid",
            "description": "Master modern CSS layout techniques through interactive games and build 3 responsive page layouts",
            "estimated_time": "6 hours",
            "resource_type": "practice",
            "resource_title": "Flexbox Froggy + CSS Grid Garden",
            "resource_url": "https://flexboxfroggy.com/"
        },
    ],
    "milestone_5": [  # Backend Development
        {
            "task_title": "Build a REST API with FastAPI",
            "description": "Learn FastAPI by building a complete CRUD API with request validation, error handling, and automatic docs",
            "estimated_time": "12 hours",
            "resource_type": "documentation",
            "resource_title": "FastAPI Official Tutorial",
            "resource_url": "https://fastapi.tiangolo.com/tutorial/"
        },
        {
            "task_title": "Learn SQL & Database Design",
            "description": "Master SQL queries (SELECT, JOIN, GROUP BY, subqueries) and normalize a database schema to 3NF",
            "estimated_time": "10 hours",
            "resource_type": "practice",
            "resource_title": "SQLBolt: Interactive SQL Lessons",
            "resource_url": "https://sqlbolt.com/"
        },
        {
            "task_title": "Implement Authentication & Authorization",
            "description": "Add JWT-based authentication to your API with password hashing, token refresh, and role-based access",
            "estimated_time": "8 hours",
            "resource_type": "video",
            "resource_title": "Tech With Tim: Python REST API Authentication",
            "resource_url": "https://www.youtube.com/watch?v=5GxQ1rLTwaU"
        },
        {
            "task_title": "Build a Blog API with SQLAlchemy ORM",
            "description": "Create a full blog backend with posts, comments, users, and tags using SQLAlchemy models and migrations",
            "estimated_time": "10 hours",
            "resource_type": "project",
            "resource_title": "Real Python: FastAPI with SQLAlchemy",
            "resource_url": "https://realpython.com/fastapi-python-web-apis/"
        },
    ],
    "milestone_6": [  # First Full-Stack Project
        {
            "task_title": "Design & Plan Your Full-Stack App",
            "description": "Create wireframes, define API endpoints, design database schema, and write user stories for a task management app",
            "estimated_time": "6 hours",
            "resource_type": "documentation",
            "resource_title": "Notion: Project Planning Template",
            "resource_url": "https://www.notion.so/templates/project-management"
        },
        {
            "task_title": "Build the Frontend with React",
            "description": "Create a React frontend with components, state management, routing, and API integration using Axios/fetch",
            "estimated_time": "20 hours",
            "resource_type": "course",
            "resource_title": "React Official: Learn React Tutorial",
            "resource_url": "https://react.dev/learn"
        },
        {
            "task_title": "Connect Frontend to Backend API",
            "description": "Integrate your React frontend with your FastAPI backend, handle CORS, loading states, and error boundaries",
            "estimated_time": "8 hours",
            "resource_type": "video",
            "resource_title": "Traversy Media: React + FastAPI Full Stack",
            "resource_url": "https://www.youtube.com/watch?v=d4Y2DkAlTGM"
        },
        {
            "task_title": "Deploy Your App to Vercel + Railway",
            "description": "Deploy frontend to Vercel and backend to Railway, configure environment variables, set up CI/CD pipeline",
            "estimated_time": "5 hours",
            "resource_type": "project",
            "resource_title": "Vercel: Deploying with Git",
            "resource_url": "https://vercel.com/docs/deployments/overview"
        },
        {
            "task_title": "Write Tests & Add Error Handling",
            "description": "Add pytest for backend API tests and React Testing Library for frontend, aim for 70%+ coverage",
            "estimated_time": "8 hours",
            "resource_type": "documentation",
            "resource_title": "Pytest Official Documentation",
            "resource_url": "https://docs.pytest.org/en/stable/getting-started.html"
        },
    ],

    # Phase 3: Advanced Skills
    "milestone_7": [  # Advanced Programming Concepts
        {
            "task_title": "Study Design Patterns with Refactoring Guru",
            "description": "Learn Singleton, Factory, Observer, Strategy, and Decorator patterns with real-world examples and implementation",
            "estimated_time": "15 hours",
            "resource_type": "documentation",
            "resource_title": "Refactoring Guru: Design Patterns",
            "resource_url": "https://refactoring.guru/design-patterns"
        },
        {
            "task_title": "Complete System Design Primer",
            "description": "Study scalability, load balancing, caching, database sharding, and microservices architecture",
            "estimated_time": "20 hours",
            "resource_type": "documentation",
            "resource_title": "System Design Primer (GitHub)",
            "resource_url": "https://github.com/donnemartin/system-design-primer"
        },
        {
            "task_title": "Implement a Design Pattern in Your Project",
            "description": "Refactor an existing project to use Repository, Service Layer, and Dependency Injection patterns",
            "estimated_time": "10 hours",
            "resource_type": "project",
            "resource_title": "Architecture Patterns with Python (Book)",
            "resource_url": "https://www.cosmicpython.com/"
        },
        {
            "task_title": "Solve 30 Medium LeetCode Problems",
            "description": "Practice dynamic programming, graph algorithms, and binary search through medium-difficulty challenges",
            "estimated_time": "25 hours",
            "resource_type": "practice",
            "resource_title": "NeetCode: Roadmap & Solutions",
            "resource_url": "https://neetcode.io/roadmap"
        },
    ],
    "milestone_8": [  # Cloud & DevOps
        {
            "task_title": "Learn Docker by Containerizing Your App",
            "description": "Write Dockerfiles, create docker-compose configs, and containerize your full-stack application",
            "estimated_time": "10 hours",
            "resource_type": "course",
            "resource_title": "Docker Official: Getting Started",
            "resource_url": "https://docs.docker.com/get-started/"
        },
        {
            "task_title": "Set Up GitHub Actions CI/CD Pipeline",
            "description": "Create automated testing, linting, and deployment workflows using GitHub Actions YAML configuration",
            "estimated_time": "6 hours",
            "resource_type": "documentation",
            "resource_title": "GitHub Actions: Quickstart",
            "resource_url": "https://docs.github.com/en/actions/quickstart"
        },
        {
            "task_title": "Deploy to AWS/GCP Free Tier",
            "description": "Deploy a containerized app to AWS EC2/ECS or GCP Cloud Run using free tier, configure networking and SSL",
            "estimated_time": "8 hours",
            "resource_type": "video",
            "resource_title": "TechWorld with Nana: AWS Tutorial for Beginners",
            "resource_url": "https://www.youtube.com/watch?v=ZB5ONbD_SMY"
        },
        {
            "task_title": "Implement Infrastructure as Code with Terraform",
            "description": "Define cloud infrastructure using Terraform HCL, manage state, and automate resource provisioning",
            "estimated_time": "8 hours",
            "resource_type": "documentation",
            "resource_title": "HashiCorp: Terraform Get Started",
            "resource_url": "https://developer.hashicorp.com/terraform/tutorials/aws-get-started"
        },
    ],
    "milestone_9": [  # Advanced Project Portfolio
        {
            "task_title": "Build a Real-Time Chat Application",
            "description": "Create a WebSocket-based chat app with rooms, typing indicators, message history, and user authentication",
            "estimated_time": "25 hours",
            "resource_type": "project",
            "resource_title": "Ania Kubow: Real-Time Chat App Tutorial",
            "resource_url": "https://www.youtube.com/watch?v=ZwFA3YMfkoc"
        },
        {
            "task_title": "Clone a Popular App (Twitter/Trello/Notion)",
            "description": "Build a simplified clone of a major application focusing on core features, database design, and UI polish",
            "estimated_time": "40 hours",
            "resource_type": "project",
            "resource_title": "JavaScript Mastery: Full-Stack Clones",
            "resource_url": "https://www.youtube.com/@javascriptmastery"
        },
        {
            "task_title": "Add Performance Monitoring & Error Tracking",
            "description": "Integrate Sentry for error tracking, add performance metrics, implement logging, and set up health checks",
            "estimated_time": "6 hours",
            "resource_type": "documentation",
            "resource_title": "Sentry: Python Setup Guide",
            "resource_url": "https://docs.sentry.io/platforms/python/"
        },
    ],

    # Phase 4: Specialization
    "milestone_10": [  # System Design & Architecture
        {
            "task_title": "Design a Scalable URL Shortener",
            "description": "Design and implement a URL shortener handling 1M+ URLs with caching, analytics, and rate limiting",
            "estimated_time": "15 hours",
            "resource_type": "practice",
            "resource_title": "Educative: Grokking System Design",
            "resource_url": "https://www.educative.io/courses/grokking-modern-system-design-interview-for-engineers-managers"
        },
        {
            "task_title": "Build a Microservices Architecture",
            "description": "Split a monolith into microservices with API gateway, service discovery, and inter-service communication",
            "estimated_time": "20 hours",
            "resource_type": "project",
            "resource_title": "Microservices.io: Patterns",
            "resource_url": "https://microservices.io/patterns/index.html"
        },
        {
            "task_title": "Study Real-World Architecture Case Studies",
            "description": "Analyze how Netflix, Uber, and Instagram handle scale — read official engineering blogs and replicate key patterns",
            "estimated_time": "10 hours",
            "resource_type": "documentation",
            "resource_title": "High Scalability Blog",
            "resource_url": "http://highscalability.com/all-time-favorites/"
        },
    ],
    "milestone_11": [  # Open Source Contribution
        {
            "task_title": "Find & Fix a Good First Issue",
            "description": "Browse 'good first issue' labels on popular repos (FastAPI, Django, React), fix a bug, and submit a PR",
            "estimated_time": "10 hours",
            "resource_type": "project",
            "resource_title": "Good First Issues (Aggregator)",
            "resource_url": "https://goodfirstissues.com/"
        },
        {
            "task_title": "Build & Publish an npm/PyPI Package",
            "description": "Create a reusable utility library, write tests and docs, and publish it to npm or PyPI",
            "estimated_time": "8 hours",
            "resource_type": "documentation",
            "resource_title": "PyPI: Publishing Your Package",
            "resource_url": "https://packaging.python.org/en/latest/tutorials/packaging-projects/"
        },
        {
            "task_title": "Write Technical Blog Posts",
            "description": "Write 3 technical articles on dev.to or Hashnode covering problems you solved and what you learned",
            "estimated_time": "12 hours",
            "resource_type": "project",
            "resource_title": "Dev.to: Write Your First Post",
            "resource_url": "https://dev.to/"
        },
    ],
    "milestone_12": [  # Industry-Ready Portfolio
        {
            "task_title": "Build a Professional Portfolio Website",
            "description": "Create a polished portfolio site showcasing 4-6 best projects with live demos, source code, and case studies",
            "estimated_time": "15 hours",
            "resource_type": "project",
            "resource_title": "Brittany Chiang Portfolio (Inspiration)",
            "resource_url": "https://brittanychiang.com/"
        },
        {
            "task_title": "Prepare for Technical Interviews",
            "description": "Practice 50+ coding problems, study behavioral questions (STAR method), and do 3 mock interviews",
            "estimated_time": "30 hours",
            "resource_type": "practice",
            "resource_title": "NeetCode 150: Interview Prep",
            "resource_url": "https://neetcode.io/practice"
        },
        {
            "task_title": "Optimize LinkedIn & Create Tech Resume",
            "description": "Craft an ATS-friendly resume using the XYZ formula, optimize LinkedIn profile with keywords and projects",
            "estimated_time": "6 hours",
            "resource_type": "documentation",
            "resource_title": "Harvard Resume Guide (PDF)",
            "resource_url": "https://hwpi.harvard.edu/files/ocs/files/hes-resume-cover-letter-guide.pdf"
        },
        {
            "task_title": "Apply to 20 Companies with Tailored Applications",
            "description": "Research companies, customize each application, write targeted cover letters, and track applications in a spreadsheet",
            "estimated_time": "15 hours",
            "resource_type": "project",
            "resource_title": "Huntr: Job Application Tracker",
            "resource_url": "https://huntr.co/"
        },
    ],
}


# ─── Data Science Sub-Tasks ─────────────────────────────────────────────────────

DATA_SCIENCE_SUBTASKS = {
    "milestone_1": [  # Mathematics & Statistics Foundation
        {
            "task_title": "Complete Khan Academy Linear Algebra Course",
            "description": "Master vectors, matrices, eigenvalues, and linear transformations through interactive exercises and quizzes",
            "estimated_time": "20 hours",
            "resource_type": "course",
            "resource_title": "Khan Academy: Linear Algebra",
            "resource_url": "https://www.khanacademy.org/math/linear-algebra"
        },
        {
            "task_title": "Learn Statistics with StatQuest YouTube Series",
            "description": "Watch and take notes on probability distributions, hypothesis testing, p-values, confidence intervals, and Bayesian stats",
            "estimated_time": "15 hours",
            "resource_type": "video",
            "resource_title": "StatQuest: Statistics Fundamentals",
            "resource_url": "https://www.youtube.com/playlist?list=PLblh5JKOoLUK0FLuzwntyYI10UQFUhsY9"
        },
        {
            "task_title": "Solve 50 Statistics Problems on Brilliant.org",
            "description": "Practice probability, distributions, and statistical inference through interactive problem sets",
            "estimated_time": "12 hours",
            "resource_type": "practice",
            "resource_title": "Brilliant: Statistics & Probability",
            "resource_url": "https://brilliant.org/courses/statistics/"
        },
        {
            "task_title": "Implement Statistical Tests in Python",
            "description": "Code t-tests, chi-square tests, ANOVA, and correlation analysis from scratch using NumPy, then verify with SciPy",
            "estimated_time": "8 hours",
            "resource_type": "project",
            "resource_title": "Towards Data Science: Statistical Tests Guide",
            "resource_url": "https://towardsdatascience.com/statistical-tests-when-to-use-which-704557554740"
        },
    ],
    "milestone_2": [  # Python for Data Science
        {
            "task_title": "Complete Kaggle Python & Pandas Micro-Courses",
            "description": "Finish the free Kaggle courses on Python basics, Pandas data manipulation, and data cleaning with hands-on exercises",
            "estimated_time": "15 hours",
            "resource_type": "course",
            "resource_title": "Kaggle Learn: Python + Pandas",
            "resource_url": "https://www.kaggle.com/learn/python"
        },
        {
            "task_title": "Master NumPy with 100 Exercises",
            "description": "Complete the famous '100 NumPy Exercises' notebook covering array operations, broadcasting, and linear algebra",
            "estimated_time": "8 hours",
            "resource_type": "practice",
            "resource_title": "100 NumPy Exercises (GitHub)",
            "resource_url": "https://github.com/rougier/numpy-100"
        },
        {
            "task_title": "Create Data Visualizations with Matplotlib & Seaborn",
            "description": "Build 10 publication-quality charts: bar, line, scatter, heatmap, violin, and pair plots using real datasets",
            "estimated_time": "10 hours",
            "resource_type": "project",
            "resource_title": "Python Graph Gallery",
            "resource_url": "https://www.python-graph-gallery.com/"
        },
        {
            "task_title": "Analyze a Real Dataset End-to-End",
            "description": "Download a dataset from Kaggle, perform EDA, handle missing values, create features, and write a summary report",
            "estimated_time": "8 hours",
            "resource_type": "project",
            "resource_title": "Kaggle: Titanic Dataset (Getting Started)",
            "resource_url": "https://www.kaggle.com/competitions/titanic"
        },
    ],
    "milestone_3": [  # Data Analysis Tools
        {
            "task_title": "Master Jupyter Notebooks & JupyterLab",
            "description": "Learn markdown cells, magic commands, extensions, and best practices for reproducible notebook workflows",
            "estimated_time": "4 hours",
            "resource_type": "documentation",
            "resource_title": "Jupyter Official: Getting Started",
            "resource_url": "https://jupyter.org/try"
        },
        {
            "task_title": "Complete SQLBolt & Practice Complex Queries",
            "description": "Master JOINs, subqueries, window functions, CTEs, and query optimization through interactive SQL lessons",
            "estimated_time": "10 hours",
            "resource_type": "practice",
            "resource_title": "SQLBolt: Interactive SQL Tutorial",
            "resource_url": "https://sqlbolt.com/"
        },
        {
            "task_title": "Build an Interactive Dashboard with Plotly/Streamlit",
            "description": "Create an interactive data dashboard with filters, charts, and KPI cards using Streamlit or Plotly Dash",
            "estimated_time": "10 hours",
            "resource_type": "project",
            "resource_title": "Streamlit Official: Create Your First App",
            "resource_url": "https://docs.streamlit.io/get-started/tutorials/create-an-app"
        },
    ],
    "milestone_4": [  # Machine Learning Fundamentals
        {
            "task_title": "Complete Andrew Ng's Machine Learning Specialization",
            "description": "Work through supervised learning, unsupervised learning, and recommender systems with hands-on labs using Python",
            "estimated_time": "40 hours",
            "resource_type": "course",
            "resource_title": "Coursera: Machine Learning Specialization (Andrew Ng)",
            "resource_url": "https://www.coursera.org/specializations/machine-learning-introduction"
        },
        {
            "task_title": "Implement 5 ML Algorithms from Scratch",
            "description": "Code linear regression, logistic regression, decision tree, k-NN, and k-means from scratch using only NumPy",
            "estimated_time": "20 hours",
            "resource_type": "project",
            "resource_title": "ML From Scratch (GitHub)",
            "resource_url": "https://github.com/eriklindernoren/ML-From-Scratch"
        },
        {
            "task_title": "Master Scikit-learn: Complete 3 Kaggle Competitions",
            "description": "Enter Titanic, House Prices, and Digit Recognizer competitions using scikit-learn pipelines and cross-validation",
            "estimated_time": "25 hours",
            "resource_type": "practice",
            "resource_title": "Kaggle: Getting Started Competitions",
            "resource_url": "https://www.kaggle.com/competitions?hostSegmentIdFilter=5"
        },
        {
            "task_title": "Build a Complete ML Pipeline Project",
            "description": "Create an end-to-end ML pipeline with data cleaning, feature engineering, model selection, hyperparameter tuning, and evaluation",
            "estimated_time": "15 hours",
            "resource_type": "project",
            "resource_title": "Scikit-learn: User Guide & Tutorials",
            "resource_url": "https://scikit-learn.org/stable/tutorial/index.html"
        },
    ],
    "milestone_5": [  # Data Visualization & Analysis
        {
            "task_title": "Study Storytelling with Data (book/course)",
            "description": "Learn visual encoding principles, chart selection, decluttering, and how to craft a data-driven narrative",
            "estimated_time": "12 hours",
            "resource_type": "course",
            "resource_title": "Storytelling with Data (YouTube Channel)",
            "resource_url": "https://www.youtube.com/@storytellingwithdata"
        },
        {
            "task_title": "Create a Comprehensive EDA Report",
            "description": "Perform exploratory data analysis on a complex dataset with 20+ features using pandas-profiling and custom charts",
            "estimated_time": "10 hours",
            "resource_type": "project",
            "resource_title": "Kaggle: EDA Notebooks (Top Voted)",
            "resource_url": "https://www.kaggle.com/code?sortBy=voteCount&language=Python&tagIds=13302"
        },
        {
            "task_title": "Build Interactive Visualizations with Plotly",
            "description": "Create animated scatter plots, choropleth maps, 3D surface plots, and interactive time series with Plotly Express",
            "estimated_time": "8 hours",
            "resource_type": "documentation",
            "resource_title": "Plotly: Python Graphing Library",
            "resource_url": "https://plotly.com/python/"
        },
    ],
    "milestone_6": [  # First Data Science Project
        {
            "task_title": "Choose & Scope a Real-World Problem",
            "description": "Select a problem (predicting house prices, customer churn, or sentiment analysis), define success metrics, and gather data",
            "estimated_time": "6 hours",
            "resource_type": "documentation",
            "resource_title": "Google: ML Problem Framing Guide",
            "resource_url": "https://developers.google.com/machine-learning/problem-framing"
        },
        {
            "task_title": "Build a Complete Data Pipeline",
            "description": "Create an ETL pipeline that ingests data, cleans it, engineers features, and stores results in a structured format",
            "estimated_time": "12 hours",
            "resource_type": "project",
            "resource_title": "Real Python: Data Cleaning with Pandas",
            "resource_url": "https://realpython.com/python-data-cleaning-numpy-pandas/"
        },
        {
            "task_title": "Train, Evaluate & Deploy Your Model",
            "description": "Train multiple models, compare with cross-validation, tune hyperparameters, and deploy the best model via Streamlit",
            "estimated_time": "15 hours",
            "resource_type": "project",
            "resource_title": "Streamlit: ML Model Deployment",
            "resource_url": "https://docs.streamlit.io/develop/tutorials/databases"
        },
        {
            "task_title": "Present Findings with a Data Story",
            "description": "Create a Jupyter notebook report or presentation with clear visualizations, methodology description, and actionable insights",
            "estimated_time": "8 hours",
            "resource_type": "project",
            "resource_title": "Kaggle: Top Notebook Examples",
            "resource_url": "https://www.kaggle.com/code?sortBy=voteCount"
        },
    ],
    "milestone_7": [  # Deep Learning & AI
        {
            "task_title": "Complete fast.ai Practical Deep Learning Course",
            "description": "Learn CNNs, RNNs, transfer learning, and NLP through top-down practical approach with PyTorch",
            "estimated_time": "40 hours",
            "resource_type": "course",
            "resource_title": "fast.ai: Practical Deep Learning for Coders",
            "resource_url": "https://course.fast.ai/"
        },
        {
            "task_title": "Build an Image Classifier with PyTorch",
            "description": "Train a CNN to classify images using transfer learning (ResNet/EfficientNet), achieve 90%+ accuracy on a custom dataset",
            "estimated_time": "15 hours",
            "resource_type": "project",
            "resource_title": "PyTorch Official: Transfer Learning Tutorial",
            "resource_url": "https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html"
        },
        {
            "task_title": "Implement a Sentiment Analysis NLP Model",
            "description": "Fine-tune a HuggingFace transformer (BERT/DistilBERT) for sentiment classification on movie reviews or tweets",
            "estimated_time": "12 hours",
            "resource_type": "project",
            "resource_title": "HuggingFace: NLP Course",
            "resource_url": "https://huggingface.co/learn/nlp-course"
        },
    ],
    "milestone_8": [  # Big Data & Cloud Platforms
        {
            "task_title": "Learn PySpark for Big Data Processing",
            "description": "Process large datasets with PySpark DataFrames, SQL, and MLlib on a local cluster or Databricks Community Edition",
            "estimated_time": "15 hours",
            "resource_type": "course",
            "resource_title": "Databricks: Free Apache Spark Training",
            "resource_url": "https://www.databricks.com/learn/training/lakehouse-fundamentals"
        },
        {
            "task_title": "Deploy a Model to Google Cloud AI Platform",
            "description": "Train a model in Google Colab, export it, deploy to Vertex AI, and create a prediction endpoint",
            "estimated_time": "8 hours",
            "resource_type": "documentation",
            "resource_title": "Google Cloud: Vertex AI Quickstart",
            "resource_url": "https://cloud.google.com/vertex-ai/docs/start/introduction-unified-platform"
        },
        {
            "task_title": "Build an Automated ML Pipeline with Airflow",
            "description": "Create a data pipeline that automatically retrains your model on new data using Apache Airflow DAGs",
            "estimated_time": "12 hours",
            "resource_type": "project",
            "resource_title": "Apache Airflow: Official Tutorial",
            "resource_url": "https://airflow.apache.org/docs/apache-airflow/stable/tutorial/index.html"
        },
    ],
    "milestone_9": [  # Advanced Data Science Portfolio
        {
            "task_title": "Create a Kaggle Competition Medal Project",
            "description": "Enter an active Kaggle competition, iterate on models for 2 weeks, aim for top 20%, and document your approach",
            "estimated_time": "30 hours",
            "resource_type": "practice",
            "resource_title": "Kaggle: Active Competitions",
            "resource_url": "https://www.kaggle.com/competitions"
        },
        {
            "task_title": "Build a Production ML Application",
            "description": "Create a full ML app (recommendation engine, chatbot, or fraud detector) with a web interface and API",
            "estimated_time": "30 hours",
            "resource_type": "project",
            "resource_title": "Made With ML: MLOps Course",
            "resource_url": "https://madewithml.com/"
        },
        {
            "task_title": "Write a Research-Style Technical Report",
            "description": "Document your best project in a LaTeX/Markdown paper format with abstract, methodology, results, and conclusions",
            "estimated_time": "10 hours",
            "resource_type": "project",
            "resource_title": "Papers With Code (Format Reference)",
            "resource_url": "https://paperswithcode.com/"
        },
    ],
    "milestone_10": [  # MLOps & Production Systems
        {
            "task_title": "Learn MLflow for Experiment Tracking",
            "description": "Track experiments, log parameters/metrics, register models, and serve predictions using MLflow",
            "estimated_time": "10 hours",
            "resource_type": "documentation",
            "resource_title": "MLflow: Official Quickstart",
            "resource_url": "https://mlflow.org/docs/latest/getting-started/index.html"
        },
        {
            "task_title": "Containerize & Deploy an ML Model with Docker",
            "description": "Package a trained model in a Docker container with FastAPI serving, health checks, and GPU support",
            "estimated_time": "8 hours",
            "resource_type": "project",
            "resource_title": "Full Stack Deep Learning: Deployment",
            "resource_url": "https://fullstackdeeplearning.com/course/2022/"
        },
        {
            "task_title": "Implement Model Monitoring & Drift Detection",
            "description": "Set up data drift detection, model performance monitoring, and automated retraining triggers",
            "estimated_time": "10 hours",
            "resource_type": "course",
            "resource_title": "Evidently AI: ML Monitoring",
            "resource_url": "https://www.evidentlyai.com/ml-in-production"
        },
    ],
    "milestone_11": [  # Research & Publications
        {
            "task_title": "Replicate a Published ML Paper",
            "description": "Choose a recent ML paper from arXiv, reproduce the key results using PyTorch, and write a blog post about your findings",
            "estimated_time": "25 hours",
            "resource_type": "project",
            "resource_title": "Papers With Code: Browse Papers",
            "resource_url": "https://paperswithcode.com/latest"
        },
        {
            "task_title": "Publish 3 Technical Articles on Medium/dev.to",
            "description": "Write in-depth technical articles covering ML concepts, project walkthroughs, or tool comparisons with code examples",
            "estimated_time": "15 hours",
            "resource_type": "project",
            "resource_title": "Towards Data Science: Writing for TDS",
            "resource_url": "https://towardsdatascience.com/write-for-us-1578ab295f9c"
        },
        {
            "task_title": "Present at a Local Meetup or Conference",
            "description": "Prepare a 15-minute talk about your ML project, submit to PyData/ML meetups, and practice public speaking",
            "estimated_time": "10 hours",
            "resource_type": "documentation",
            "resource_title": "Meetup: Data Science Events",
            "resource_url": "https://www.meetup.com/topics/data-science/"
        },
    ],
    "milestone_12": [  # Data Science Portfolio & Career Prep
        {
            "task_title": "Build a Data Science Portfolio Website",
            "description": "Create a portfolio with 4-6 projects showcasing different skills: EDA, ML, NLP, and deployment with Jupyter notebooks embedded",
            "estimated_time": "15 hours",
            "resource_type": "project",
            "resource_title": "DataSciencePortfol.io (Inspiration)",
            "resource_url": "https://www.datascienceportfol.io/"
        },
        {
            "task_title": "Master Data Science Interview Questions",
            "description": "Practice SQL, statistics, ML theory, and case study questions with mock interviews and peer review",
            "estimated_time": "25 hours",
            "resource_type": "practice",
            "resource_title": "Interview Query: DS Interview Prep",
            "resource_url": "https://www.interviewquery.com/"
        },
        {
            "task_title": "Create a Standout Resume & LinkedIn Profile",
            "description": "Highlight quantified impact, tools used, and business outcomes from projects; tailor for ATS and hiring managers",
            "estimated_time": "6 hours",
            "resource_type": "documentation",
            "resource_title": "Resume Worded: Data Science Templates",
            "resource_url": "https://resumeworded.com/data-scientist-resume-examples"
        },
    ],
}


# ─── General Tech Sub-Tasks (fallback) ──────────────────────────────────────────

GENERAL_TECH_SUBTASKS = {
    "milestone_1": [
        {
            "task_title": "Complete CS50x: Introduction to Computer Science",
            "description": "Take Harvard's legendary intro CS course covering C, Python, SQL, JavaScript, and computational thinking",
            "estimated_time": "60 hours",
            "resource_type": "course",
            "resource_title": "CS50x on edX",
            "resource_url": "https://cs50.harvard.edu/x/"
        },
        {
            "task_title": "Learn Digital Literacy with Google Digital Garage",
            "description": "Complete modules on internet basics, online safety, digital tools, and cloud collaboration",
            "estimated_time": "10 hours",
            "resource_type": "course",
            "resource_title": "Google Digital Garage",
            "resource_url": "https://learndigital.withgoogle.com/digitalgarage"
        },
        {
            "task_title": "Set Up Your Digital Workspace",
            "description": "Create accounts on GitHub, LinkedIn, Stack Overflow. Set up Google Drive, Notion, and a code editor",
            "estimated_time": "3 hours",
            "resource_type": "project",
            "resource_title": "GitHub: Creating Your Account",
            "resource_url": "https://github.com/join"
        },
    ],
    "milestone_2": [
        {
            "task_title": "Develop Critical Thinking with Coursera",
            "description": "Take a course on logical reasoning, argument analysis, and evidence-based decision making",
            "estimated_time": "15 hours",
            "resource_type": "course",
            "resource_title": "Coursera: Introduction to Logic",
            "resource_url": "https://www.coursera.org/learn/logic-introduction"
        },
        {
            "task_title": "Solve Problems on Project Euler",
            "description": "Complete 20 mathematical/computational problems to build algorithmic thinking skills",
            "estimated_time": "15 hours",
            "resource_type": "practice",
            "resource_title": "Project Euler",
            "resource_url": "https://projecteuler.net/"
        },
        {
            "task_title": "Learn Research & Documentation Skills",
            "description": "Practice finding reliable sources, synthesizing information, and writing structured reports using Markdown",
            "estimated_time": "6 hours",
            "resource_type": "documentation",
            "resource_title": "Markdown Guide",
            "resource_url": "https://www.markdownguide.org/getting-started/"
        },
    ],
}


def get_subtasks_for_milestone(milestone_id: str, career_focus: str) -> list:
    """Get sub-tasks for a specific milestone based on career focus."""
    if career_focus == "software_development":
        return SOFTWARE_DEV_SUBTASKS.get(milestone_id, [])
    elif career_focus == "data_science":
        return DATA_SCIENCE_SUBTASKS.get(milestone_id, [])
    else:
        return GENERAL_TECH_SUBTASKS.get(milestone_id, [])
