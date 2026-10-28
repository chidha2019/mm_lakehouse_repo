"""Versioned source contracts; shared by generation, drift detection and lineage."""
CONTRACTS = {
  "customer": ["customer_id","first_name","last_name","state","birth_date"],
  "insurance_product": ["product_id","product_name","line_of_business"],
  "policy": ["policy_id","customer_id","product_id","policy_status","effective_date","annual_premium","updated_at"],
  "coverage": ["coverage_id","policy_id","coverage_type","face_amount"],
  "advisor": ["advisor_id","advisor_name","region"],
  "wealth_account": ["account_id","customer_id","advisor_id","account_type","opened_date","account_status"],
  "holding": ["holding_id","account_id","security_symbol","quantity","market_price","as_of_date"],
  "transaction": ["transaction_id","account_id","transaction_date","transaction_type","amount"],
}
PRIMARY_KEYS = {"customer":"customer_id","insurance_product":"product_id","policy":"policy_id","coverage":"coverage_id","advisor":"advisor_id","wealth_account":"account_id","holding":"holding_id","transaction":"transaction_id"}
