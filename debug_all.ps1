# PowerShell script to run all debugging tests

Write-Output "===== AACT Agent Debugging Suite ====="

# Test if uvx command is available
Write-Output "`n[1/3] Testing UVX command..."
python aact_agent/test_uvx_command.py

# Test JSON-RPC communication
Write-Output "`n[2/3] Testing JSON-RPC communication..."
python aact_agent/json_rpc_test.py

# Run the debug agent
Write-Output "`n[3/3] Testing Agent-MCP communication..."
python aact_agent/debug_agent.py

Write-Output "`n===== All tests completed =====" 