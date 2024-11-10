# Canada Mines Dashboard

Dash app for explore mines data across Canada. It provides interactive filters and visualizations to examine the distribution of mines by location, commodity, and other parameters.


## Features
- **Interactive Map**: View mines across Canada with an interactive map, filterable by commodity, province, and mining phase.
- **Gantt Chart**: Displays mining project timelines, updated dynamically based on filters.
- **Data Filtering**: Easily filter data based on commodity, province, mine status, and phase.
- **Responsive Design**: Dashboard is fully responsive, with adjustable layouts for different screen sizes.

## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/Alfredomg7/CanadaMinesDash
    ```
2. **Navigate to the Project Directory**:
    ```bash
    cd CanadaMinesDa
    ```
3. **Install Dependencies**:
    This project requires Python 3.8+ and uses `pip` to manage dependencies.
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Load and Prepare Data**:
    ```bash
    python init_db.py
    ```
2. **Run the Application**:
    ```bash
    python app.py
    ```
3. **Access the Dashboard**: Open your web browser and go to `http://127.0.0.1:8050`.

## Project Structure
- `app.py`: Main application file that runs the Dash server.
- `callbacks.py`: Defines the callbacks for interactive components.
- `layout.py`: Builds the layout structure for the dashboard.
- `db_setup.py`: Handles data download and initialization.
- `utils.py`: Contains helper functions for data processing.
- `/components`: Custom UI components factory functions.
- `/assets`: Contains static files.
- `/data`: Contains the datasets.

## Technologies Used
- **Dash** and **Plotly**: For building interactive web applications and visualizations.
- **Polars**: For efficient data manipulation and processing.
- **Pandas**: Data manipulation (converted from Polars as needed for Plotly compatibility).
- **Bootstrap**: Responsive design elements via `dash_bootstrap_components`.

## Data Source
The mining data used in this project is sourced from [figshare - Past and Present Productive Mines of Canada, 1950-2022 dataset](https://figshare.com/articles/dataset/Principal_Productive_Mines_of_Canada/23740071?file=45011833).