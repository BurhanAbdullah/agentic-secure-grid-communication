#!/usr/bin/env bash

DATA="attack_agent_stress.dat"
SUMMARY="attack_agent_stress_summary.txt"

TIME=100
ATTACK_START=40
ATTACK_END=70

AGENT_TRIGGER=50
JITTER_START=45
JITTER_END=49

FAIL_SECURE_THRESHOLD=18

NORMAL_LOSS=0.05
MAX_ATTACK_LOSS=0.6
MITIGATED_LOSS=0.2

BASE_COST=1.0
MITIGATION_COST=2.5

echo "#t loss_rate recv_agent cum_loss agent_state comp_cost" > "$DATA"

cum_loss=0
fail_secure=0
total_cost=0
agent_state="NORMAL"

for ((t=1; t<=TIME; t++)); do
    # --- ramp-up attack ---
    if (( t >= ATTACK_START && t <= ATTACK_END )); then
        ramp=$(awk "BEGIN {print ($t-$ATTACK_START)/($ATTACK_END-$ATTACK_START)}")
        loss_rate=$(awk "BEGIN {print $NORMAL_LOSS + $ramp*($MAX_ATTACK_LOSS-$NORMAL_LOSS)}")
    else
        loss_rate=$NORMAL_LOSS
    fi

    # --- jitter (near false positive) ---
    if (( t >= JITTER_START && t <= JITTER_END )); then
        noise=$(awk "BEGIN {srand($t); print rand()*0.1}")
        loss_rate=$(awk "BEGIN {print $loss_rate+$noise}")
    fi

    # --- agent behavior ---
    if (( fail_secure )); then
        recv=0
        agent_state="FAIL_SECURE"
        cost=$MITIGATION_COST
    elif (( t >= AGENT_TRIGGER )); then
        recv=$(awk "BEGIN {print 1-$MITIGATED_LOSS}")
        agent_state="MITIGATING"
        cost=$MITIGATION_COST
    else
        recv=$(awk "BEGIN {print 1-$loss_rate}")
        agent_state="NORMAL"
        cost=$BASE_COST
    fi

    loss_now=$(awk "BEGIN {print 1-$recv}")
    cum_loss=$(awk "BEGIN {print $cum_loss+$loss_now}")

    if (( $(awk "BEGIN {print ($cum_loss>$FAIL_SECURE_THRESHOLD)}") )); then
        fail_secure=1
    fi

    total_cost=$(awk "BEGIN {print $total_cost+$cost}")

    echo "$t $loss_rate $recv $cum_loss $agent_state $cost" >> "$DATA"
done

{
echo "=== STRESS TEST SUMMARY ==="
echo "Agent trigger time     : $AGENT_TRIGGER"
echo "Fail-secure triggered  : $fail_secure"
echo "Final cumulative loss  : $cum_loss"
echo "Total computation cost : $total_cost"
} > "$SUMMARY"
