import pandas as pd 
import numpy as np  
import time
import sys
import itertools 

# Anomaly Model and Service Layer

class AnomalyModelService:
    """
    Simulates the core AI/ML service layer. Learns the baseline and performs detection.
    """
    def __init__(self):
        # Data representing a window of stable, historical traffic
        self.TRAINING_DATA = [18.2, 22.5, 19.1, 21.0, 23.4, 17.8, 24.1, 25.0, 19.5, 20.8, 21.3, 22.1]
        
        # Sequenced data to show the anomaly gradually hitting the system over time
        self.ANOMALY_RAMPUP_WINDOWS = [
            [20.0, 21.5, 23.0, 22.0, 24.0, 20.5, 21.0, 23.5, 24.0, 25.0],  # T=1 (Safe)
            [25.0, 24.5, 26.0, 25.5, 27.0, 26.5, 25.5, 27.0, 28.0, 29.0],  # T=2 (Safe)
            [28.0, 29.0, 30.0, 31.0, 29.5, 30.5, 31.0, 30.5, 29.0, 32.0],  # T=3 (Safe)
            [32.0, 31.5, 33.0, 32.5, 34.0, 33.5, 32.5, 34.0, 35.0, 36.0],  # T=4 (Safe)
            [35.0, 36.0, 37.0, 38.0, 39.0, 38.5, 37.5, 39.0, 40.0, 41.0],  # T=5 (Safe)
            [41.0, 42.0, 43.0, 44.0, 45.0, 46.0, 45.0, 44.0, 43.0, 42.0],  # T=6 (Safe)
            [50.0, 60.0, 70.0, 80.0, 90.0, 100.0, 110.0, 120.0, 130.0, 140.0], # T=7 (CRITICAL SPIKE HITS)
            [150.0, 160.0, 170.0, 180.0, 190.0, 200.0, 210.0, 220.0, 230.0, 240.0]  # T=8 (MAX ALERT)
        ]
        
        # State
        self.modelStats = {'mean': 0, 'stdDev': 0, 'threshold': 0}
        self.isSpikeActive = False 
        
        self.trainModel()

    def trainModel(self):
        """Calculates the statistical baseline (simulating Isolation Forest training)."""
        data = self.TRAINING_DATA
        
        # Calculate Mean (Average CPU Load)
        mean = sum(data) / len(data)
        # Calculate Standard Deviation using numpy.sqrt
        variance = sum((x - mean) ** 2 for x in data) / len(data)
        stdDev = np.sqrt(variance)

        # Set Anomaly Threshold using the 5-Sigma rule
        threshold = mean + (5 * stdDev) 
        
        self.modelStats = {'mean': mean, 'stdDev': stdDev, 'threshold': threshold}
        
        print("\n========================================================================")
        print(" PHASE 1: AI MODEL TRAINING COMPLETE (Establishing the Safe Baseline)")
        print("========================================================================")
        print(f"| Learned Mean CPU Load:  {self.modelStats['mean']:.2f}%")
        print(f"| ALERT THRESHOLD (5-Sigma): {self.modelStats['threshold']:.2f}% CPU")
        print("-" * 75)
        print("| Model is deployed. Ready for initial verification run.")
        print("========================================================================\n")

    def activateSpike(self):
        """Activates the state that will lead to the anomaly."""
        self.isSpikeActive = True
        print("\n!!! SPIKE ACTIVATION: Anomalous traffic is now flowing into the stream.")
        print("!!! Starting real-time detection sequence now. Total 8 cycles.")
        print("------------------------------------------------------------------------\n")
        
    def runDetectionCycle(self, currentStream, cycle_num):
        """Performs the core anomaly check on the given stream window."""
        
        threshold = self.modelStats['threshold']
        anomalousPoints = 0
        maxSpike = 0

        # Core Detection Logic
        for cpu in currentStream:
            if cpu > threshold:
                anomalousPoints += 1
                if cpu > maxSpike:
                    maxSpike = cpu

        # Decision Logic: Flag alert if at least 3 points violate the boundary
        isAnomaly = anomalousPoints >= 3

        if isAnomaly:
            # We use a different print format for the CRITICAL ALERT
            print(f"\n🚨🚨 ALERT @ CYCLE {cycle_num}: ANOMALY DETECTED! (Pattern Classification: Hostile/Bug)")
            print(f"| Status: CRITICAL SPIKE. {anomalousPoints} points violated the threshold. Max CPU: {maxSpike:.1f}%")
            print(">>> ACTION: EMERGENCY SCALE-UP INITIATED & Security Queue Notified.")
            print("-" * 75)
            return True
        else:
            # Return True/False status along with the max observation for the analysis message
            return False, max(currentStream)


# --- Presentation Demo Flow with Simulation ---

def run_presentation_demo():
    """Manages the sequential flow for the live presentation."""
    
    detector = AnomalyModelService()

    # 2. FIRST RUN: Initial Check (Should be SAFE)
    print("\n--- DEMO STEP 2: VERIFICATION RUN (Expected: SAFE) ---")
    detector.runDetectionCycle(detector.TRAINING_DATA, 0) # Run on training data for verification

    # 3. USER ACTION: Simulate the user pressing the trigger button
    print("\n------------------------------------------------------------------------")
    input("| PRESS ENTER TO ACTIVATE ANOMALOUS SPIKE (Simulating Button Click): ")
    detector.activateSpike()
    
    # 4. SIMULATION LOOP (The 8-Cycle Show)
    
    # Setup for the cycling message
    animation_frames = itertools.cycle(['|', '/', '-', '\\'])
    total_cycles = len(detector.ANOMALY_RAMPUP_WINDOWS)
    
    for cycle_num in range(1, total_cycles + 1):
        
        current_window = detector.ANOMALY_RAMPUP_WINDOWS[cycle_num - 1]
        
        # --- Real-Time Analysis Message ---
        sys.stdout.write(f"\r| Cycle {cycle_num}/{total_cycles} | {next(animation_frames)} | Analyzing traffic spikes in the servers...")
        sys.stdout.flush()
        
        # Wait for 1 second (simulating one detection cycle time)
        time.sleep(1)

        # Run detection on the current ramping data window
        result = detector.runDetectionCycle(current_window, cycle_num)
        
        if result is True:
            # Anomaly Detected: Stop the loop
            break
        else:
            # Traffic is nominal, display the detailed safe status
            is_anomaly, max_cpu = result
            sys.stdout.write(f"\r| Cycle {cycle_num}/{total_cycles} | ✅ | Traffic Nominal (Max CPU: {max_cpu:.1f}%)" + " " * 20 + "\n")
            sys.stdout.flush()
            
    # Final check to ensure the terminal is clean
    print("\n\n--- SIMULATION COMPLETE ---")


if __name__ == "__main__":
    try:
        run_presentation_demo()
    except Exception as e:
        print(f"\n[ERROR] An unexpected error occurred: {e}")
