# File: scripts/anomaly_detector.py
# Innovation: AI for Anomaly Detection (Future Enhancement Demo)
# Purpose: Demonstrates how the system can detect abnormal traffic patterns 
#          instead of waiting for a static CPU threshold to be hit.

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import sys

def check_for_anomaly(cpu_data):
    """
    Simulates checking a stream of CPU usage data for anomalies 
    using the Isolation Forest ML model.
    """
    print("\n--- Running AI Anomaly Detection Model ---")
    
    if not cpu_data or len(cpu_data) < 2:
        print("Not enough data for anomaly detection.")
        return 
        
    df = pd.DataFrame(cpu_data, columns=['cpu_utilization'])
    
    # Train and Predict using Isolation Forest 
    try:
        # Train on the provided mock data
        model = IsolationForest(contamination=0.1, random_state=42)
        model.fit(df[['cpu_utilization']])
        
        # Predict Anomalies: -1 means Anomaly, 1 means Normal
        df['anomaly'] = model.predict(df[['cpu_utilization']])
    except ValueError as e:
        print(f"Error during model training: {e}")
        return 

    # Check for Anomaly Alert
    if -1 in df['anomaly'].values:
        anomaly_count = len(df[df['anomaly'] == -1])
        print("******************************************")
        print(f"🚨 ANOMALY DETECTED! Found {anomaly_count} UNUSUAL DATA POINTS.")
        print("Analysis: This spike is abnormal and requires immediate security review.")
        print("Action: Proactively alert security team via Slack/PagerDuty!")
        print("******************************************")
    else:
        print("✅ Traffic is behaving normally. No anomalies detected.")

# ------------------------------------------------------------------
# MOCK DEMO EXECUTION
# ------------------------------------------------------------------

# DEMO 1: Normal Traffic (Scaling threshold might be hit, but pattern is normal)
print("DEMO 1: Normal Traffic Pattern (CPU usage is high but predictable)")
normal_metrics = [5, 6, 5, 7, 6, 8, 5, 6, 7, 10, 11, 10]
check_for_anomaly(normal_metrics)

# DEMO 2: ANOMALOUS Spike (A sudden, unnatural spike, like a bot or DDoS attack)
print("\nDEMO 2: ANOMALOUS Spike Pattern (Unnatural spike requiring PROACTIVE intervention)")
anomaly_metrics = [10, 11, 10, 12, 10, 150, 155, 160, 12, 11, 10] 
check_for_anomaly(anomaly_metrics)