# How to Run the Project

To start the Career Guidance Platform locally without having to manually set up everything again, simply run the provided batch script.

## On Windows

Double-click the `start.bat` file in the project's root folder from your file explorer, or run it from the command line:

```shell
.\start.bat
```

**What the script does automatically:**
1. Checks for and creates a Python virtual environment (`.venv`) if it doesn't exist.
2. Installs or upgrades all the required packages from `requirements.txt`.
3. Starts the FastAPI backend server using Uvicorn on port `8000`.

After the script finishes setting up, the application will be running and available at:
- **Main UI**: [http://localhost:8000/ui](http://localhost:8000/ui)
- **API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)

**To Stop the Server:**
Press `CTRL+C` in the terminal where the script is running.
