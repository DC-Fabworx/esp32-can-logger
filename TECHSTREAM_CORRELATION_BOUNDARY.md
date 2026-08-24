---
Status: Active
Last Reviewed: 2026-08-24
---

# Techstream Correlation Boundary

## Repository role

`esp32-can-logger` owns CAN capture and telemetry tooling. It does not own Toyota Techstream/GTS semantic authority.

Primary Techstream/GTS source and normalized diagnostic authority:

```text
DC-Fabworx/300_Developments
```

Primary firmware/Ghidra/ROM/RAM/calibration binding authority:

```text
DC-Fabworx/ECU-RE-Engine
```

## Evidence boundary

A frame captured by this logger is transport evidence. It does not become an OEM signal definition merely because its value correlates with a Techstream channel.

For a reviewed Techstream-to-CAN correlation, preserve:

- capture file SHA-256;
- capture start/end time and timezone;
- logger firmware/build identity;
- CAN interface/bus/bitrate configuration;
- arbitration ID, direction and payload bytes;
- ISO-TP/UDS reconstruction details where applicable;
- exact Techstream source/session identity;
- `info__*.json` / `info.json` `memo` and `functionId` label where present;
- exact OEM/GTS signal name/unit/source context;
- correlation method and confidence;
- source repository/commit or runtime-authority identity.

## Techstream scaling rule

If a comparison value comes from Techstream JSON `signalDataList[].data`, it is already display-domain. Do not apply `signalInfoList` `mul/div/offset/decPntCount` again.

If deriving a physical value directly from CAN payload bytes, that is a separate decode/binding task and must be validated independently.

## Numeric ID rule

Do not use a Techstream numeric signal ID alone as a CAN signal identity. IDs can be context dependent. Carry the source/session-local OEM name and metadata or an explicit reviewed crosswalk.

## Handoff target

Compact CAN/Techstream correlation results should be promoted to the owning authority repository (`300_Developments` for diagnostic/CAN semantic evidence; `ECU-RE-Engine` when a firmware binding is proven) rather than turning this logger repository into a second Toyota diagnostic knowledge base.
