# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Stanford Loyal Agents Initiative / Civics.com

import sys
import os
import yaml
import asyncio
import argparse
from datetime import datetime
from io import StringIO
from dotenv import load_dotenv

# Add repo root to path to import core
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(REPO_ROOT)

# ADD D2/Final_Deliverable to path so we can import local scorers
FINAL_DELIV_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.append(FINAL_DELIV_ROOT)


load_dotenv(os.path.join(REPO_ROOT, ".env"))

from core.registry import ComponentRegistry
from core.evaluation import run_evaluation_batch
from core.reporting import results_to_csv, results_to_json, generate_summary_report

# Import Local Scorers
# Note: They are in D2/Final_Deliverable/core/scoring/
# Since we added FINAL_DELIV_ROOT to path, we can import them.
# The folder structure is D2/Final_Deliverable/core/scoring
# but 'core' is also the name of the main repo module. This might cause namespace collision.
# Better to use relative import or careful path management.
# Actually, since I wrote them to D2/Final_Deliverable/core/scoring/*.py, 
# and REPO_ROOT/core is the main engine.
# I should probably have written them to a distinct package name or imported them by file path.
# But let's try importing via the path we added.

# It is safer to define a registration function here that imports them from the file system.
def register_custom_scorers():
    try:
        # We need to import the classes.
        # Check where they are: D2/Final_Deliverable/core/scoring/
        # This mirrors the main repo structure. 
        # Let's assume we can import them if we adjust sys.path or if we treat D2.Final_Deliverable...
        
        # NOTE: Because 'core' is already imported from REPO_ROOT, importing 'core.scoring.conflict_immunity_scorer' 
        # will try to find it in REPO_ROOT/core/scoring first.
        # I did NOT write them to REPO_ROOT/core/scoring, I allowed them to be in D2/...
        # So I need to be careful.
        
        # Workaround: Use spec_from_file_location or just move/copy them to fdl_scorers to avoid 'core' collision
        # OR, since I am in a script, I can just use importlib.
        
        import importlib.util
        
        scorers_dir = os.path.join(FINAL_DELIV_ROOT, "core", "scoring")
        scorer_files = {
            "conflict_immunity": "conflict_immunity_scorer.py",
            "ueta_compliance": "ueta_compliance_scorer.py",
            "llms_respect": "llms_respect_scorer.py",
            "compliance_first": "compliance_first_scorer.py",
            "dual_fiduciary": "dual_fiduciary_scorer.py",
            "fdl_disclosure": "fdl_disclosure_scorer.py",
            "fdl_alignment": "fdl_alignment_scorer.py"
        }
        
        registry = ComponentRegistry()
        
        for name, filename in scorer_files.items():
            path = os.path.join(scorers_dir, filename)
            if os.path.exists(path):
                spec = importlib.util.spec_from_file_location(f"local_scorer_{name}", path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Find the class
                # Convention: NameScorer e.g. ConflictImmunityScorer
                # Or just iterate classes inheriting from BaseScorer
                from core.scoring.base import BaseScorer
                import inspect
                
                for attr_name, attr_obj in inspect.getmembers(module):
                    if inspect.isclass(attr_obj) and issubclass(attr_obj, BaseScorer) and attr_obj is not BaseScorer:
                        # Register it
                        # Instantiate to get name? No, register_scorer takes class
                        # But wait, registry.register_scorer(name, class)
                        print(f"Registering custom scorer: {name} from {filename}")
                        registry.register_scorer(name, attr_obj)
                        break
    except Exception as e:
        print(f"Error registering custom scorers: {e}")
        import traceback
        traceback.print_exc()

def load_yaml(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

async def main():
    parser = argparse.ArgumentParser(description="Run Lake Merritt Evaluation")
    parser.add_argument("--pack", required=True, help="Path to Eval Pack YAML")
    args = parser.parse_args()

    print(f"Running Evaluation with Pack: {args.pack}")
    
    # 1. Discover builtins (standard core scorers)
    ComponentRegistry.discover_builtins()
    
    # 2. Register D2 Custom Scorers
    register_custom_scorers()
    
    try:
        pack_data = load_yaml(args.pack)
    except Exception as e:
        print(f"Failed to load pack YAML: {e}")
        return

    # Handle Ingestion Data Load
    raw_csv_data = None
    ingestion = pack_data.get('ingestion', {})
    if ingestion.get('type') == 'csv':
        cfg = ingestion.get('config', {})
        csv_path = cfg.get('path')
        if csv_path:
            pack_dir = os.path.dirname(os.path.abspath(args.pack))
            abs_csv_path = os.path.normpath(os.path.join(pack_dir, csv_path))
            print(f"Loading CSV data from: {abs_csv_path}")
            try:
                with open(abs_csv_path, 'r', encoding='utf-8') as f:
                    raw_csv_data = f.read()
            except Exception as e:
                print(f"Error loading CSV file: {e}")
                return
    
    if not raw_csv_data:
        print("Error: No raw data loaded.")
        return

    csv_io = StringIO(raw_csv_data)

    # Run
    try:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            print("WARNING: OPENAI_API_KEY not found in environment or .env file.")

        results = await run_evaluation_batch(
            pack=pack_data,
            raw_data=csv_io,
            api_keys={"openai": api_key or ""},
            user_context="Standard User Profile: Busy professional, values privacy over convenience." 
        )
        
        # --- REPORTING ---
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        reports_dir = os.path.join(os.path.dirname(__file__), "reports")
        os.makedirs(reports_dir, exist_ok=True)
        
        print(f"\n=== GENERATING REPORTS ===")
        print(f"Saving to: {reports_dir}")

        json_path = os.path.join(reports_dir, f"eval_results_{timestamp}.json")
        with open(json_path, "w") as f:
            f.write(results_to_json(results))
        print(f"✅ Saved JSON: {json_path}")

        csv_path = os.path.join(reports_dir, f"eval_results_{timestamp}.csv")
        with open(csv_path, "w") as f:
            f.write(results_to_csv(results))
        print(f"✅ Saved CSV: {csv_path}")

        md_path = os.path.join(reports_dir, f"report_{timestamp}.md")
        with open(md_path, "w") as f:
            f.write(generate_summary_report(results))
        print(f"✅ Saved Markdown Report: {md_path}")
        
    except Exception as e:
        print(f"Error during evaluation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
