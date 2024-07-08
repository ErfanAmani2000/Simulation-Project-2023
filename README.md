# Simulation Project 2023

## Overview

This project simulates the operations of an auto insurance center, which is open daily from 8:00 AM to 6:00 PM. The simulation models various processes, including client arrivals, service queues, and complaint handling. The project leverages historical data to represent visitor patterns influenced by weather conditions and periods accurately.

## Simulation Details

### Operating Hours

- **Opening Time**: 8:00 AM
- **Closing Time**: 6:00 PM
  - After 6:00 PM, only cars inside the center will be served until the system is empty. Queues forming outside after closing will disappear.
  - Both the plaintiff and culprit cars must be present simultaneously to proceed. If the first car enters before closing, the second car can enter after 6:00 PM.

### Visitor Arrival Patterns

- Arrival distributions vary based on weather conditions (snowfall, rain) and specific periods:
  - 8:00 AM to 10:00 AM
  - 10:00 AM to 1:00 PM
  - 1:00 PM to 3:00 PM
  - 3:00 PM to 6:00 PM
- Phase two of the project will include an Excel file with dates and probabilities of rain.

### Service Process

1. **Photo Taking**
   - Cars enter in pairs (plaintiff and culprit) and queue for photos if there is capacity.
   - Two photographers are available, each serving pairs of cars with an exponential distribution (mean = 6 minutes).
   - The photo queue can hold a maximum of 40 cars (20 pairs).
   - If the queue is full, cars wait outside until space is available.

2. **Single Car Handling**
   - 30% of clients arrive alone and wait for the second car.
   - Single cars in the photo queue inside the area are moved to the waiting parking area until paired.
   - Priority is given to paired cars over those waiting outside.
   - Waiting time for single cars follows an exponential distribution (mean = 30 minutes).

3. **File Preparation**
   - Three experts prepare files with a service time following a triangular distribution (min = 5, avg = 6, max = 7 minutes).

4. **Expert Review**
   - After file preparation, cars enter the expert queue where two experts serve with an exponential distribution (mean = 9 minutes).
   - After the review, cars either proceed to file completion or to the complaint registration.
   - 10% of clients wish to complain, based on historical data.

5. **Complaint Handling**
   - Cars with complaints go to the complaint registration section, served by one complaint expert (exponential distribution, mean = 15 minutes).
   - After registering the complaint, cars repeat the expert procedures and complete the file.
   - Priority is given to cars completing their cases over new cases.

### Assumptions

- Distances between sections are insignificant.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/YourUsername/InsuranceCenterSimulation.git
    cd InsuranceCenterSimulation
    ```

2. **Create a virtual environment (optional but recommended)**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
