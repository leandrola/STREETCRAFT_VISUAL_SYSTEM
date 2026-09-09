# MCP Adapter Guidance

MCP is an implementation option for the connector boundary, not a Streetcraft dependency.

An MCP adapter is acceptable when it can reliably provide:
1. board enumeration;
2. stable provider item identifiers or stable pin URLs;
3. image references usable by the classification runtime;
4. outbound source links when present;
5. pagination/completeness information.

The adapter should expose normalized operations equivalent to:
- list_board_items
- get_item_metadata
- get_item_image_reference
- get_source_link

It must not:
- assign SCA IDs;
- classify an item as Canon;
- decide evidence confidence;
- rewrite source identity;
- silently omit pages while claiming FULL enumeration.

If Pinterest access changes in the future, replace the adapter. Do not migrate Archive semantics.
