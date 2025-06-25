import boto3 
import json
import tqdm


GUARDRAIL_ID = "guardrail-id"
GUARDRAIL_VERSION = "DRAFT" # Or the version number, 1, 2, etc.

GROUND_TRUTH_PATH = "ground_truth.json"
JSON_OUTPUT_PATH = "output.json"

VERIFY_CERTS = False
GENERATE_REPORT = True

session = boto3.Session(region_name="us-east-1")
bedrock_runtime = session.client("bedrock-runtime", verify=VERIFY_CERTS)

with open(GROUND_TRUTH_PATH, "r", encoding="utf-8") as gt:
    ground_truth_data = json.load(gt)

with open(JSON_OUTPUT_PATH, "w", encoding="utf-8") as json_file:
    results = []
    inputs_processed = 0
    guardrail_filtering_hits = 0

    for input in tqdm.tqdm(ground_truth_data, desc="Processing inputs"):
        message = input["message"]
        should_filter = input["should_filter"]
       
        try:
            response = bedrock_runtime.apply_guardrail(
               guardrailIdentifier=GUARDRAIL_ID,
               guardrailVersion=GUARDRAIL_VERSION,
               source="INPUT",
               content=[{"text": message}]
            )

            action = response.get("action", "")
            filtered_by_guardrail = action in ["BLOCKED", "GUARDRAIL_INTERVENED"]
        except Exception as e:
            print(f"Error applying guardrail: {message} - {e}")
            filtered_by_guardrail = None
        
        results.append({
            "message": message,
            "should_filter": should_filter,
            "filtered_by_guardrail": filtered_by_guardrail
        })

        if filtered_by_guardrail is not None:
            inputs_processed += 1
            if filtered_by_guardrail == should_filter:
                guardrail_filtering_hits += 1

    json.dump(results, json_file, ensure_ascii=False, indent=2)

    if inputs_processed > 0:
        print(f"Total inputs processed: {inputs_processed}")
        print(f"Guardrail filtering hits: {guardrail_filtering_hits}")  
        accuracy = guardrail_filtering_hits / inputs_processed
        print(f"Guardrail filtering accuracy: {accuracy:.2%}")
    else:
        print("No inputs processed")

if GENERATE_REPORT:
    from report import generate_report
    generate_report()