#!/usr/bin/env python3
"""
Sovereign Enterprise System - Complete Core Meta-Builder
File: builder.py
Purpose: Reads a system blueprint JSON and builds structural production code files
         using native protocols and robust error processing.
"""

import os
import json
import sys
import time
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

def load_system_blueprint(blueprint_path: str) -> dict:
    """Loads and returns the structural architecture schema map."""
    if not os.path.exists(blueprint_path):
        print(f"[-] Error: Blueprint framework configuration missing at: {blueprint_path}")
        sys.exit(1)
    try:
        with open(blueprint_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as err:
        print(f"[-] Error: Syntax break detected within configuration format: {err}")
        sys.exit(1)

def extract_raw_source_stream(payload_text: str) -> str:
    """Cleans markdown boundaries to protect raw target system code integrity."""
    lines = payload_text.strip().split('\n')
    if lines and lines[0].startswith('```'):
        lines.pop(0)
    if lines and lines[-1].startswith('```'):
        lines.pop()
    return '\n'.join(lines).strip()

def request_code_generation(api_key: str, system_rule: str, operational_task: str) -> str:
    """
    Executes a direct, zero-bloat native HTTP POST request against the high-performance
    production engine API endpoint to retrieve full file contents.
    """
    # Target endpoint utilizing the modern generative v1beta service matrix
    endpoint_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    # Structure the payload exactly according to production payload specifications
    payload_data = {
        "contents": [
            {
                "parts": [
                    {"text": f"{system_rule}\n\nTask:\n{operational_task}"}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.1
        }
    }
    
    serialized_bytes = json.dumps(payload_data).encode('utf-8')
    
    headers = {
        "Content-Type": "application/json"
    }
    
    req = Request(endpoint_url, data=serialized_bytes, headers=headers, method="POST")
    
    try:
        with urlopen(req) as response:
            response_json = json.loads(response.read().decode('utf-8'))
            
            # Navigate the payload block structure directly
            candidates = response_json.get("candidates", [])
            if not candidates:
                raise ValueError("Payload missing processing candidate blocks.")
                
            parts = candidates[0].get("content", {}).get("parts", [])
            if not parts:
                raise ValueError("Target candidate missing text generation return keys.")
                
            return parts[0].get("text", "")
            
    except HTTPError as http_err:
        error_content = http_err.read().decode('utf-8')
        raise RuntimeError(f"Gateway HTTP Error [{http_err.code}]: {error_content}")
    except URLError as url_err:
        raise RuntimeError(f"Network Connectivity Anomaly: {url_err.reason}")

def execute_compilation_sequence():
    # 1. Look for the API token across secure environment nodes
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("[-] Error: GEMINI_API_KEY target variable missing from current environment profile.")
        print("[*] Resolve via: export GEMINI_API_KEY=\"your_key\"")
        sys.exit(1)
        
    # 2. Automatically locate active blueprint configurations matching files
    blueprint_file = "career_blueprint.json"
    if not os.path.exists(blueprint_file):
        blueprint_file = "enterprise_blueprint.json"
        if not os.path.exists(blueprint_file):
            blueprint_file = "blueprint.json"
            
    print(f"[*] Initializing native execution pipeline over target map: {blueprint_file}")
    blueprint = load_system_blueprint(blueprint_file)
    
    project_name = blueprint.get("project_name", blueprint.get("enterprise_name", "Sovereign_Output"))
    modules = blueprint.get("modules", [])
    root_output_dir = os.path.join(os.getcwd(), "output", project_name)
    
    # 3. System-level constraint parameters
    system_rule = (
        "You are an expert Principal Systems Engineer writing flawless, raw production-grade Python code. "
        "CRITICAL RULES:\n"
        "1. NO PLACEHOLDERS: Do not leave empty functions, notes, or short-circuited logic structures.\n"
        "2. NO EXPLANATIONS: Return ONLY the raw code matching the file requirements. Do not add intro text."
    )
    
    print(f"[*] Provisioning absolute system matrix tree under: {root_output_dir}")
    print(f"[*] Target modules detected: {len(modules)}")
    print("-" * 60)
    
    # 4. Iterate structurally through layout specifications
    for module in modules:
        module_name = module.get("module_name", "unnamed_module")
        files = module.get("files", [])
        
        print(f"\n[+] Compiling Architectural Module: {module_name}")
        
        for file_entry in files:
            target_rel_path = file_entry.get("path")
            target_purpose = file_entry.get("purpose")
            
            absolute_save_path = os.path.join(root_output_dir, target_rel_path)
            parent_directory = os.path.dirname(absolute_save_path)
            
            # Automatically establish path structures down to disk
            os.makedirs(parent_directory, exist_ok=True)
            
            print(f"    └─► Constructing asset: {target_rel_path}")
            
            prompt_instruction = (
                f"Write the complete, comprehensive production source code for the file: {target_rel_path}\n"
                f"Operational Context / Purpose: {target_purpose}\n\n"
                f"Implement full variables, error boundaries, and imports. Do not truncate."
            )
            
            retry_pacing = 10
            execution_completed = False
            
            while not execution_completed:
                try:
                    raw_payload = request_code_generation(api_key, system_rule, prompt_instruction)
                    cleaned_source = extract_raw_source_stream(raw_payload)
                    
                    with open(absolute_save_path, 'w', encoding='utf-8') as output_file:
                        output_file.write(cleaned_source)
                        
                    print(f"        [✓] Complete code saved safely ({len(cleaned_source)} bytes).")
                    execution_completed = True
                    
                    # Prevent API rate limitation walls through standard execution pacing
                    time.sleep(6)
                    
                except Exception as anomaly:
                    print(f"        [!] Execution challenge met: {anomaly}")
                    print(f"        [*] Engaging backoff logic block. Pausing for {retry_pacing}s...")
                    time.sleep(retry_pacing)
                    retry_pacing = min(retry_pacing * 2, 60)

    print("\n" + "="*60)
    print(f"[✓] METABUILD MATRIX COMPLETE: {project_name}")
    print(f"[✓] Code base verified and written completely to disk targets.")
    print("="*60)

if __name__ == "__main__":
    execute_compilation_sequence()
