#!/bin/bash
# SPDX-License-Identifier: Apache-2.0
#
# Fiduciary Duty Legal Eval - Full Evaluation Script
# Runs Frame A (Consumer) and Frame B (Business) evaluations
#
# Usage: ./run_full_evaluation.sh
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DELIVERABLE_DIR="$(dirname "$SCRIPT_DIR")"

echo "=============================================="
echo "  Fiduciary Duty Legal Eval - Full Run"
echo "  $(date)"
echo "=============================================="
echo ""

# Check for .env file
if [ ! -f "$DELIVERABLE_DIR/../../.env" ]; then
    echo "❌ ERROR: .env file not found at repo root"
    echo "   Please create .env with OPENAI_API_KEY=your_key"
    exit 1
fi

# Check for required Python packages
python3 -c "import openai, yaml, dotenv" 2>/dev/null || {
    echo "❌ ERROR: Missing required Python packages"
    echo "   Run: pip install -r requirements.txt"
    exit 1
}

echo "✅ Prerequisites check passed"
echo ""

# Run Frame A (Consumer) Evaluation
echo "=============================================="
echo "  Running Frame A (Consumer) Evaluation"
echo "=============================================="
cd "$DELIVERABLE_DIR"
python3 run_evaluation.py --pack eval_packs/fdl_frame_a_consumer.yaml

echo ""

# Run Frame B (Business) Evaluation
echo "=============================================="
echo "  Running Frame B (Business) Evaluation"
echo "=============================================="
python3 run_evaluation.py --pack eval_packs/fdl_frame_b_business.yaml

echo ""
echo "=============================================="
echo "  Evaluation Complete!"
echo "=============================================="
echo ""
echo "Reports saved to: $DELIVERABLE_DIR/reports/"
ls -la "$DELIVERABLE_DIR/reports/" | tail -6
echo ""
echo "To view the latest report:"
echo "  open reports/\$(ls -t reports/*.md | head -1)"
