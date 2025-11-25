1. While running the MCP server in 'stdio' mode with `mcp.run('stdio')`, we need to first initialize the server

```json
{
  "jsonrpc": "2.0",
  "method": "initialize",
  "params": {
    "protocolVersion": "0.1.0",
    "clientInfo": { "name": "TestClient", "version": "1.0" },
    "capabilities": {}
  },
  "id": 100
}
```

2. Then, to call any tool -

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": { "name": "add", "arguments": { "a": 1, "b": 2 } },
  "id": 1
}
```
