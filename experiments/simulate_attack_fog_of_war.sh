#!/usr/bin/env bash

DATA="attack_fog_of_war.dat"
SUMMARY="attack_fog_of_war_summary.txt"

TIME=100
FAIL_THRESHOLD=18

BASE_COST=1.0
MITIGATION_COST=2.5

CUM_LOSS=0
TOTAL_COST=0
FS=0

echo "# t entropy loss cum_loss agent_state cost spoof" > "$DATA"

for t in {1..100}; do
    SPOOF=0

    # --- Entropy model ---
    ENTROPY=$(awk "BEGIN {print 0.1 + rand()*0.1}")

    # Decoy spoofing window
    if (( t >= 10 && t <= 30 )); then
        ENTROPY=$(awk "BEGIN {print 0.7 + rand()*0.2}")
        SPOOF=1
    fi

    # Real attack window
    if (( t >= 40 && t <= 70 )); then
        ENTROPY=$(awk "BEGIN {print 0.8 + rand()*0.2}")
    fi

    # --- Loss model ---
    if (( t >= 40 && t <= 70 )); then
        LOSS=$(awk "BEGIN {print 0.05 + ($t-40)*0.03}")
    else
        LOSS=0.05
    fi

    CUM_LOSS=$(awk "BEGIN {print $CUM_LOSS + $LOSS}")

    # --- Agent logic (elastic + correlation-aware) ---
    if (( $(awk "BEGIN {print ($ENTROPY > 0.6 && $LOSS > 0.1)}") )); then
        AGENT="MITIGATING"
        COST=$MITIGATION_COST
    else
        AGENT="BASELINE"
        COST=$BASE_COST
    fi

    TOTAL_COST=$(awk "BEGIN {print $TOTAL_COST + $COST}")

    # Fail-secure
    if (( $(awk "BEGIN {print ($CUM_LOSS > $FAIL_THRESHOLD)}") )); then
        FS=1
        AGENT="FAIL_SECURE"
    fi

    echo "$t $ENTROPY $LOSS $CUM_LOSS $AGENT $COST $SPOOF" >> "$DATA"
done

echo "=== FOG OF WAR TEST SUMMARY ===" > "$SUMMARY"
echo "Final cumulative loss : $CUM_LOSS" >> "$SUMMARY"
echo "Total computation cost: $TOTAL_COST" >> "$SUMMARY"
echo "Fail-secure triggered : $FS" >> "$SUMMARY"

echo "Saved: $DATA"
echo "Saved: $SUMMARY"
