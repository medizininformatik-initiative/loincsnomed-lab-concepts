#!/bin/bash
echo "========================================"
echo "Running Test Suite"
echo "========================================"
echo ""

# Test 1: LOINCSNOMED Adapter (public, no auth required)
echo "[1/2] Testing LOINCSNOMED Adapter..."
python scripts/test_scripts/test_loincsnomed_adapter.py
TEST1=$?

# Test 2: OntoServer Adapter (requires MII credentials)
echo ""
echo "[2/2] Testing OntoServer Adapter (requires MII auth)..."
python scripts/test_scripts/test_ontoserver_adapter.py
TEST2=$?

echo ""
echo "========================================"
echo "Test Suite Summary"
echo "========================================"
if [ $TEST1 -eq 0 ]; then
  echo "✓ LOINCSNOMED Adapter: PASSED"
else
  echo "✗ LOINCSNOMED Adapter: FAILED"
fi

if [ $TEST2 -eq 0 ]; then
  echo "✓ OntoServer Adapter: PASSED"
else
  echo "✗ OntoServer Adapter: FAILED (may require MII credentials)"
fi

# Return non-zero if any critical test failed
if [ $TEST1 -ne 0 ]; then
  exit 1
fi
exit 0
