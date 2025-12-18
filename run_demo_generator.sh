#!/bin/bash
# Wrapper script to run demo data generator with temporary env vars

source .venv/bin/activate

export STRIPE_SECRET_KEY="sk_test_dummy_for_demo_data"
export STRIPE_PUBLISHABLE_KEY="pk_test_dummy_for_demo_data"

echo "yes" | python generate_demo_data.py
