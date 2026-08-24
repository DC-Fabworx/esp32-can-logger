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
- per-sample timestamp semantics for both CAN and Techstream sources, including clock source, unit and reference epoch/origin where available;
- when recordings use separate hosts or clocks, synchronization method and the measured/derived clock offset, drift or other explicit alignment evidence used by the correlation;
- logger firmware/build identity;
- CAN interface/bus/bitrate configuration;
- arbitration ID, frame format/IDE state (11-bit standard versus 29-bit extended), direction and payload bytes;
- RTR state and CAN FD/BRS/ESI flags where the capture format supports them;
- ISO-TP/UDS reconstruction details where applicable;
- exact Techstream source/session identity;
- `info__*.json` / `info.json` `memo` and `functionId` label where present;
- exact OEM/GTS signal name/unit/source context;
- correlation method and confidence;
- source repository/commit or runtime-authority identity.

A timestamp match is not valid merely because both recordings have wall-clock times. When separate clocks are involved, preserve enough evidence to reproduce the alignment and distinguish clock offset/drift from signal lag.

Likewise, a numeric arbitration ID is incomplete without frame-format context. Preserve IDE/frame-format and other available frame-state flags so standard, extended, remote and FD frames cannot be conflated.

## Techstream scaling rule

If a comparison value comes from Techstream JSON `signalDataList[].data`, it is already display-domain. Do not apply `signalInfoList` `mul/div/offset/decPntCount` again.

If deriving a physical value directly from CAN payload bytes, that is a separate decode/binding task and must be validated independently.

## Numeric ID rule

Do not use a Techstream numeric signal ID alone as a CAN signal identity. IDs can be context dependent. Carry the source/session-local OEM name and metadata or an explicit reviewed crosswalk.

## Handoff target

Compact CAN/Techstream correlation results should be promoted to the owning authority repository (`300_Developments` for diagnostic/CAN semantic evidence; `ECU-RE-Engine` when a firmware binding is proven) rather than turning this logger repository into a second Toyota diagnostic knowledge base.
