# 5G Initial Setup Procedure — Video Script & Talking Points

---

## Phase 1: Cell Search & Synchronization (0:00–0:30)

**On-screen:** UE icon appears, scanning animation, SSB pulses from gNB

**Narrator:**
"When a 5G device powers on, it doesn't know where the network is. The first thing it does is scan through the available NR frequency bands, searching for a 5G cell."

"The gNodeB — the 5G base station — periodically broadcasts Synchronization Signal Blocks, or SSBs. Each SSB contains the Primary and Secondary Synchronization Signals — PSS and SSS."

"The UE locks onto these signals to achieve frame synchronization and obtain the Physical Cell Identity. This is the very first handshake between the device and the network."

---

## Phase 2: System Information Acquisition (0:30–1:00)

**On-screen:** MIB and SIB1 blocks appear above gNB, arrows flow to UE

**Narrator:**
"Once synchronized, the UE reads the Master Information Block — the MIB — carried on the Physical Broadcast Channel, or PBCH."

"The MIB tells the UE where to find SIB1 — System Information Block 1 — which is scheduled on the PDSCH."

"SIB1 contains essential cell access parameters: the cell's tracking area code, public land mobile network identity, and scheduling information for all other SIBs. The UE now knows how to talk to this cell."

---

## Phase 3: Random Access (RACH) (1:00–1:40)

**On-screen:** Four arrows animate sequentially: MSG1→MSG2→MSG3→MSG4

**Narrator:**
"Now the UE needs to get the network's attention. It initiates the four-step Random Access procedure."

"Step one — MSG1: the UE sends a PRACH preamble. This is essentially the device raising its hand and saying 'I'm here.'"

"Step two — the gNB responds with MSG2, the Random Access Response, or RAR. It grants the UE an uplink resource and provides a temporary identifier."

"Step three — MSG3: the UE sends an RRC Setup Request, now using the allocated uplink grant."

"Step four — the gNB sends MSG4, a Contention Resolution message, confirming that this particular UE is now uniquely identified on the cell."

---

## Phase 4: RRC Connection Setup (1:40–2:10)

**On-screen:** RRC messages flow between UE and gNB, SRB1 label appears

**Narrator:**
"With contention resolved, the UE and gNB establish an RRC connection. This is the radio resource control link."

"The gNB sends an RRCSetup message, configuring Signaling Radio Bearer 1 — SRB1. This dedicated channel carries all subsequent signaling messages between the UE and the network."

"The UE responds with RRCSetupComplete, which includes the initial NAS message — the registration request — piggybacked inside."

---

## Phase 5: Registration & Authentication (2:10–3:00)

**On-screen:** Four network nodes appear — UE, gNB, AMF, AUSF/UDM — messages flow between them

**Narrator:**
"The gNB forwards the registration request to the AMF — the Access and Mobility Management Function — the core network's entry point for UE signaling."

"The AMF triggers authentication with the AUSF and UDM. The network verifies the UE's identity and subscription data. This may involve a challenge-response exchange using the subscriber's permanent key stored on the USIM."

"Once authenticated, the AMF initiates a Security Mode Command procedure, establishing integrity protection and ciphering for all subsequent NAS signaling."

"Finally, the AMF sends a Registration Accept message back to the UE. The device is now registered on the network."

---

## Phase 6: PDU Session Establishment (3:00–3:40)

**On-screen:** UE, gNB, UPF, and Data Network animate with PDU session arrows

**Narrator:**
"Registration is complete, but the UE still can't send user data. It needs a PDU Session — a Protocol Data Unit session — which is the 5G equivalent of a data connection."

"The UE sends a PDU Session Establishment Request. This flows through the gNB to the AMF, which selects a UPF — the User Plane Function."

"The UPF is the anchor point for the user plane. The network establishes N4 rules between the SMF and UPF, and the UPF is connected to the external Data Network — whether that's the internet, a corporate VPN, or an edge computing platform."

"The UE is assigned an IP address, and user data can now flow through the gNB to the UPF and out to the network."

---

## Phase 7: Summary (3:40–4:00)

**On-screen:** All six steps listed vertically on screen, final "Connected" message

**Narrator:**
"Let's recap. The 5G initial setup procedure happens in six phases:"

"1.  Cell Search  — synchronizing to the gNB's SSB"
"2.  System Info  — reading MIB and SIB1 for cell parameters"
"3.  Random Access  — the four-step RACH procedure"
"4.  RRC Setup  — establishing Signaling Radio Bearer 1"
"5.  Registration  — authenticating with the core network via the AMF"
"6.  PDU Session  — creating the data path through the UPF"

"Once all six steps are complete, the UE is fully connected to the 5G network and ready for data transfer. This entire process typically completes in under a second on a modern 5G network."

---

## Render Command

```bash
manim -pql 5g_initial_setup.py FiveGInitialSetup
```

For higher quality (recommended for final video):
```bash
manim -pqh 5g_initial_setup.py FiveGInitialSetup
```
