# 5G Initial Setup Procedure — Video Script

---

## Phase 1: Cell Search & Synchronization (0:00–0:45)

**Animation:** Cell tower (gNB) with radio waves pulsing outward. Correlation plot builds up showing a peak. Zadoff-Chu and m-sequence equations appear.

**Narrator:**
"When a 5G device powers on, it scans NR frequency bands looking for a cell. The gNB periodically transmits SS/PBCH blocks containing PSS and SSS."

"The **Primary Synchronization Signal** uses a Zadoff-Chu sequence:"

\[
a_u(n) = \exp\!\left(-j \frac{\pi u\,n(n+1)}{N_{\text{ZC}}}\right),\quad N_{\text{ZC}} = 127
\]

"There are three possible root indices: \(u = 25, 29, 34\). The UE correlates against all three and picks the strongest peak — this gives it the **Physical Cell ID** within the cell group."

"The **Secondary Synchronization Signal** uses two length-127 m-sequences multiplied together. Together PSS and SSS give the full \(N_{\text{ID}}^{\text{cell}} = 3N_{\text{ID}}^{(1)} + N_{\text{ID}}^{(2)}\)."

"The UE achieves frame synchronization and knows where the cell's timing and frequency are."

---

## Phase 2: System Information Acquisition (0:45–1:30)

**Animation:** NR time-frequency resource grid appears. PBCH resources highlighted in purple. MIB bit fields displayed. SIB1 scheduling info shown.

**Narrator:**
"Once synchronized, the UE reads the **Master Information Block** carried on the Physical Broadcast Channel."

"The MIB contains 23 bits of critical information: system frame number (6 bits), subcarrier spacing (1 bit), SSB-to-SIB1 offset (4 bits), DMRS position (1 bit), PDCCH configuration for SIB1 (8 bits), and 3 reserved bits."

"The MIB tells the UE where to find **SIB1** on the PDSCH. SIB1 repeats every 160 ms and contains cell access parameters: the PLMN identity, tracking area code, cell barring status, and scheduling information for all other SIBs."

"The UE now knows the cell's configuration and can begin active communication."

---

## Phase 3: Random Access (RACH) (1:30–2:15)

**Animation:** PRACH preamble waveform with cyclic prefix. Timing advance equation. Four-step handshake between UE and gNB.

**Narrator:**
"The UE needs to get the network's attention via the **Random Access Channel**. The PRACH preamble is also a Zadoff-Chu sequence, length 839 in FR1 or 139 in FR2, with a cyclic shift."

"When the gNB receives the preamble, it estimates the **Timing Advance** — the round-trip delay between UE and gNB:"

\[
N_{\text{TA}} = \frac{T_{\text{Rx}} - T_{\text{Tx}}}{2},\quad T_{\text{TA}} = (N_{\text{TA}} + N_{\text{TA,offset}})\,T_c
\]

"\(T_c = 0.509\text{ ns}\) is the basic NR time unit. The TA ensures the UE's uplink transmissions arrive in the correct time window."

"The four-step handshake proceeds:"

- **MSG1:** UE sends PRACH preamble
- **MSG2:** gNB responds with Random Access Response (RAR) — TA value and uplink grant
- **MSG3:** UE sends RRC Setup Request on the allocated grant
- **MSG4:** gNB sends Contention Resolution — the UE is now uniquely identified

---

## Phase 4: RRC Connection Setup (2:15–2:45)

**Animation:** RRC state machine (IDLE → CONNECTED → INACTIVE). SRB1 message flow.

**Narrator:**
"The UE transitions from RRC_IDLE to RRC_CONNECTED. The gNB configures **Signaling Radio Bearer 1** — the dedicated control channel for NAS messages."

"The RRCSetup message carries SRB1 configuration. The UE replies with RRCSetupComplete, which piggybacks the **Registration Request** NAS PDU inside."

"The UE can also transition to RRC_INACTIVE, a power-saving state where the UE stays CM-CONNECTED but with suspended radio resources."

---

## Phase 5: Registration & Authentication (2:45–3:30)

**Animation:** Messages flowing through UE → gNB → AMF → AUSF. 5G key hierarchy with KDF arrows.

**Narrator:**
"The gNB forwards the Registration Request to the **AMF** — the Access and Mobility Management Function. The AMF requests authentication vectors from the AUSF."

"The network runs **5G AKA**: the UE proves its identity using the permanent key K stored on the USIM. The AUSF derives CK∥IK, then feeds them through a Key Derivation Function to produce the key hierarchy:"

\[
K \rightarrow \text{CK∥IK} \rightarrow K_{\text{AUSF}} \rightarrow K_{\text{SEAF}} \rightarrow K_{\text{AMF}} \rightarrow K_{\text{NAS}}
\]

"Each level is derived via KDF using the subscriber's SUPI, SN-name, and freshness parameters. The AMF establishes **NAS Security** with integrity and ciphering keys."

"A Registration Accept message is sent back through the chain, confirming the UE is registered."

---

## Phase 6: PDU Session Establishment (3:30–4:15)

**Animation:** User plane protocol stack (SDAP/PDCP/RLC/MAC/PHY). QoS flow mapped to DRB. GTP-U tunneling. IP address assignment.

**Narrator:**
"Registration is complete, but the UE needs a data connection. It sends a **PDU Session Establishment Request**."

"The user plane runs on a layered protocol stack: SDAP (QoS mapping), PDCP (ciphering + header compression), RLC (segmentation + ARQ), MAC (scheduling + HARQ), and PHY (OFDM)."

"Each QoS flow is identified by a **5QI** value and mapped to a Data Radio Bearer. The gNB matches QoS requirements to appropriate RLC modes and priority."

"On the N3 interface, data is encapsulated in **GTP-U tunnels** using a 32-bit Tunnel Endpoint Identifier (TEID):"

\[
\text{GTP header} = \text{TEID} + \text{SeqNo} + \text{N-PDU}
\]

"The UE is assigned an IP address and now has full user-plane connectivity."

---

## Phase 7: Summary (4:15–4:30)

**Animation:** Six phases listed with key math callouts. Final "Connected" message.

**Narrator:**
"Let's recap. Initial setup completes in six phases:"

1.  **Cell Search** — PSS/SSS, Zadoff-Chu correlation
2.  **System Info** — MIB (PBCH) + SIB1 (PDSCH) on the resource grid
3.  **Random Access** — 4-step RACH with timing advance
4.  **RRC Setup** — SRB1, RRC state machine transitions
5.  **Registration** — 5G AKA with KDF key hierarchy
6.  **PDU Session** — Protocol stack, QoS flows, GTP-U tunneling

"All six phases typically complete in under a second on a modern 5G network. The UE is now fully connected and ready for data transfer."

---

## Render

```bash
source .venv/bin/activate
manim -pql tutorials/5g-initial-setup/5g_initial_setup.py FiveGInitialSetup   # preview
manim -pqh tutorials/5g-initial-setup/5g_initial_setup.py FiveGInitialSetup   # final
```
